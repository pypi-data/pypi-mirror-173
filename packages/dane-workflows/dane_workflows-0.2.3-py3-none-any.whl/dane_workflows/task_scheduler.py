import sys
import logging
from typing import List, Type, Tuple, Optional
from dane_workflows.util import base_util
from dane_workflows.data_provider import DataProvider, ProcessingStatus
from dane_workflows.data_processing import DataProcessingEnvironment, ProcessingResult
from dane_workflows.exporter import Exporter
from dane_workflows.status import StatusHandler, StatusRow
from dane_workflows.status_monitor import StatusMonitor


"""
The TaskScheduler is the main process that interprets & runs a workflow comprised of:
- implementation of a DataProvider
- implementation of a ProcessingEnvironment
- implementation of an Exporter
- implementation of a StatusHandler
- Optional: implementation of a StatusMonitor

The constructor takes a config and a class type for each of the aforementioned components
to be able to instantiate the correct implementions. The config should make sure to provide
these implementations with the specific parameters they require.
"""


logger = logging.getLogger(__name__)


class TaskScheduler(object):
    def __init__(
        self,
        config: dict,
        status_handler: Type[StatusHandler],
        data_provider: Type[DataProvider],
        data_processing_env: Type[DataProcessingEnvironment],
        exporter: Type[Exporter],
        status_monitor: Type[StatusMonitor] = None,
        unit_test: bool = False,
    ):
        self.config = config

        if not self._validate_config():
            logger.critical("Malconfigured, quitting...")
            sys.exit()
            return  # in unit tests, sys.exit is mocked, so return

        self.BATCH_SIZE = config["TASK_SCHEDULER"]["BATCH_SIZE"]

        self.BATCH_LIMIT = (
            config["TASK_SCHEDULER"]["BATCH_LIMIT"]
            if "BATCH_LIMIT" in config["TASK_SCHEDULER"]
            else -1
        )  # to limit the amout of batches

        # to keep track of the batches
        self.MONITOR_FREQ = (
            config["TASK_SCHEDULER"]["MONITOR_FREQ"]
            if "MONITOR_FREQ" in config["TASK_SCHEDULER"]
            else -1
        )  # optional monitoring frequency

        # first initialize the status handler and pass it to the data provider and processing env
        self.status_handler: StatusHandler = status_handler(config)
        self.data_provider = data_provider(
            config, self.status_handler, unit_test
        )  # instantiate the DataProvider
        self.data_processing_env = data_processing_env(
            config, self.status_handler, unit_test
        )  # instantiate the DataProcessingEnvironment
        self.exporter = exporter(config, self.status_handler, unit_test)

        self.status_monitor = None
        if status_monitor:
            self.status_monitor = status_monitor(
                config, self.status_handler
            )  # optional monitoring

    def _validate_config(self):
        try:
            # check settings for this class
            assert "TASK_SCHEDULER" in self.config, "TASK_SCHEDULER"
            assert all(
                [x in self.config["TASK_SCHEDULER"] for x in ["BATCH_SIZE"]]
            ), "TASK_SCHEDULER.keys"
            assert base_util.check_setting(
                self.config["TASK_SCHEDULER"]["BATCH_SIZE"], int
            ), "TASK_SCHEDULER.BATCH_SIZE"

            # check optional parameter types
            if "BATCH_LIMIT" in self.config["TASK_SCHEDULER"]:
                assert base_util.check_setting(
                    self.config["TASK_SCHEDULER"]["BATCH_LIMIT"], int
                ), "TASK_SCHEDULER.BATCH_LIMIT"
            if "MONITOR_FREQ" in self.config["TASK_SCHEDULER"]:
                assert base_util.check_setting(
                    self.config["TASK_SCHEDULER"]["MONITOR_FREQ"], int
                ), "TASK_SCHEDULER.MONITOR_FREQ"
        except AssertionError as e:
            logger.error(f"Configuration error: {str(e)}")
            return False

        return True

    # Calls the StatusHandler to load the status_handler.cur_source_batch into memory.
    #
    # Subsequently the StatusHandler is called to recover the last proc_batch.
    #
    # Based on the last ProcessingStatus in this proc_batch the number of steps to skip
    # within _run_proc_batch() is determined to resume processing from
    def _recover(self) -> Tuple[Optional[List[StatusRow]], int, int]:
        source_batch_recovered, last_proc_batch = self.status_handler.recover(
            self.data_provider
        )
        if source_batch_recovered is False:
            logger.warning(
                "Could not recover source_batch, so either the work was done or something is wrong with the DataProvider, quitting"
            )
            sys.exit()

        last_proc_batch_id = 0
        skip_steps = 0

        if last_proc_batch:
            last_proc_batch_id = self.status_handler.get_last_proc_batch_id()
            logger.info("Synchronizing last proc_batch with ProcessingEnvironment")

            # determine where to resume processing by looking at the highest step in the chain
            # TODO maybe it's better to use the LOWEST step of the batch
            highest_proc_stat = 0
            num_errors_in_last_proc_batch = 0
            for row in last_proc_batch:
                if row.status == ProcessingStatus.ERROR:  # skip errors
                    num_errors_in_last_proc_batch += 1
                    continue
                if row.status.value > highest_proc_stat:
                    highest_proc_stat = row.status.value

            # ALL items of the last proc_batch failed
            if num_errors_in_last_proc_batch == len(last_proc_batch):
                logger.warning(
                    "The last proc_batch failed completely, starting at the next batch"
                )
                return (
                    None,
                    last_proc_batch_id + 1,  # continue on from the NEXT proc_batch
                    0,
                )

            # ProcessingStatus values are ordered, so we can simply subtract to find the steps to skip
            skip_steps = highest_proc_stat - 2

        return last_proc_batch, last_proc_batch_id, skip_steps

    # Before starting the endless loop of processing everything the DataProvider has to offer,
    # _recover() is called to make sure:
    #
    # 1. The StatusHandler has loaded cur_source_batch in memory
    # 2. The last proc_batch is retrieved (representing the batch last fed to the ProcessingEnvironment)
    # 3. The last successful step within this batch is retrieved we know how many steps to
    #    skip within _run_proc_batch()
    def run(self):

        # always try to recover (without StatusHandler data, the first source_batch will be created)
        last_proc_batch, last_proc_batch_id, skip_steps = self._recover()

        # if a proc_batch was recovered, make sure to finish it from the last ProcessingStatus
        if last_proc_batch:
            logger.info(f"Recovered proc_batch {last_proc_batch_id}, finishing it up")

            # before doing the "recovery run", check if the batch limit was reached
            self._check_batch_limit(last_proc_batch_id)

            # run the recovered proc_batch from the highest ProcessingStatus
            if (
                self._run_proc_batch(last_proc_batch, last_proc_batch_id, skip_steps)
                is True
            ):
                last_proc_batch_id += 1  # continue on
            else:
                logger.critical("Critical error whilst processing, quitting")

        # ok now that the recovered proc_batch has completed, continue on from this proc_batch_id
        proc_batch_id = last_proc_batch_id

        # continue until all is finished or something breaks
        while True:
            # first check if the BATCH_LIMIT was reached
            self._check_batch_limit(proc_batch_id)

            # then get the next proc_batch from the DataProvider
            status_rows = self._get_next_proc_batch(proc_batch_id, self.BATCH_SIZE)
            if status_rows is None:
                logger.info("No source_batch remaining, all done, quitting...")
                break

            # now that we have a new proc_batch, pass it on to the ProcessingEnvironment
            # and eventually the Exporter
            if self._run_proc_batch(status_rows, proc_batch_id) is False:
                logger.critical("Critical error whilst processing, quitting")
                break

            # update the proc_batch_id and continue on to the next
            proc_batch_id += 1

            # optionally, monitor the status
            if self.status_monitor:
                logger.info(
                    f"check wether or not to monitor to slack: proc_batch_id: {proc_batch_id}, monitor_freq:{self.MONITOR_FREQ}, monitor: {proc_batch_id % self.MONITOR_FREQ}"
                )
                if proc_batch_id % self.MONITOR_FREQ == 0:
                    logger.info("monitoring_status")
                    self.status_monitor.monitor_status()

    # asks the DataProvider for a new proc_batch
    def _get_next_proc_batch(
        self, proc_batch_id: int, batch_size: int
    ) -> Optional[List[StatusRow]]:
        logger.info(
            f"asking DataProvider for next batch: {proc_batch_id} ({batch_size})"
        )
        return self.data_provider.get_next_batch(proc_batch_id, batch_size)

    def _check_batch_limit(self, proc_batch_id: int):
        logger.info(
            f"Checking if the BATCH_LIMIT {self.BATCH_LIMIT} was reached for {proc_batch_id}"
        )
        # proc_batch_id starts at 0, BATCH_LIMIT starts at 1 (1 means "run 1 batch")
        if self.BATCH_LIMIT > -1:
            if proc_batch_id > self.BATCH_LIMIT - 1:
                logger.warning(
                    "Limit of {} batches reached, quitting after finishing proc_batch_id: {}".format(
                        self.BATCH_LIMIT, proc_batch_id
                    )
                )
                sys.exit()
        logger.info("BATCH_LIMIT not reached, continuing...")

    # The proc_batch (list of StatusRow objects) is processed in 5 steps:
    #
    # 1. Register the batch in the ProcessingEnvironment
    # 2. Tell the ProcessingEnvironment to start processing the batch
    # 3. Monitor the ProcessingEnvironment's progress until it's done
    # 4. Retrieve the output from the ProcessingEnvironment
    # 5. Feed the output to the Exporter, so results are put in a happy place
    def _run_proc_batch(
        self, status_rows: List[StatusRow], proc_batch_id: int, skip_steps: int = 0
    ) -> bool:
        logger.info(
            f"Processing proc_batch {proc_batch_id}, skipping {skip_steps} steps"
        )
        if skip_steps >= 5:
            logger.warning(
                f"Warning: why are you skipping so many (i.e. {skip_steps}) steps?"
            )
            return True

        if skip_steps == 0:  # first register the batch in the proc env
            if not self._register_proc_batch(proc_batch_id, status_rows):
                return False

        if skip_steps < 2:  # Alright let's ask the proc env to start processing
            if not self._process_proc_batch(proc_batch_id):
                return False

        if skip_steps < 3:  # monitor the processing, until it returns the results
            if not self._monitor_proc_batch(proc_batch_id):
                return False

        if skip_steps < 5:
            # TODO before fetching the results, implement a call that updates the status
            # of ALL items within the proc_batch, regardless of success/failure

            # now fetch the results from the ProcessingEnvironment
            # even if this was already done, it's required again for the unfinished export
            processing_results = self._fetch_proc_batch_output(proc_batch_id)

            if processing_results and self._export_proc_batch_output(
                proc_batch_id, processing_results
            ):
                return True
            else:
                return False

        return True

    # calls the ProcessingEnvironment to register the supplied proc_batch
    def _register_proc_batch(
        self, proc_batch_id: int, proc_batch: List[StatusRow]
    ) -> bool:
        logger.info(f"Registering batch: {proc_batch_id}")
        status_rows = self.data_processing_env.register_batch(proc_batch_id, proc_batch)
        if status_rows is None:
            logger.error(f"Could not register batch {proc_batch_id}, quitting")
            return False
        logger.info(f"Successfully registered batch: {proc_batch_id}")
        return True

    # calls the ProcessingEnvironment to start processing the proc_batch
    def _process_proc_batch(self, proc_batch_id: int) -> bool:
        logger.info(f"Triggering proc_batch to start processing: {proc_batch_id}")
        status_rows = self.data_processing_env.process_batch(proc_batch_id)
        if status_rows is None:
            logger.error(
                f"Could not trigger proc_batch {proc_batch_id} to start processing, quitting"
            )
            return False
        logger.info(f"Successfully triggered the process for: {proc_batch_id}")
        return True

    # calls the ProcessingEnvironment to start monitoring the progress of the proc_batch
    def _monitor_proc_batch(self, proc_batch_id: int) -> bool:
        logger.info(f"Start monitoring proc_batch until it finishes: {proc_batch_id}")
        status_rows = self.data_processing_env.monitor_batch(proc_batch_id)
        if status_rows is None:
            logger.error(
                f"Error while monitoring proc_batch: {proc_batch_id}, quitting"
            )
            return False
        logger.info(
            f"Successfully monitored proc_batch: {proc_batch_id} till it finished"
        )
        return True

    # calls the ProcessingEnvironment to fetch the results of the processed proc_batch
    def _fetch_proc_batch_output(
        self, proc_batch_id: int
    ) -> Optional[List[ProcessingResult]]:
        logger.info(f"Fetching output data for proc_batch: {proc_batch_id}")
        output = self.data_processing_env.fetch_results_of_batch(proc_batch_id)
        if output is None:
            logger.error(
                f"Did not receive any processing results for {proc_batch_id}, quitting"
            )
            return None
        logger.info(f"Successfully retrieved output for proc_batch {proc_batch_id}")
        return output

    # calls the Exporter to export the processing output of the proc_batch
    def _export_proc_batch_output(
        self, proc_batch_id: int, processing_results: List[ProcessingResult]
    ) -> bool:
        logger.info(f"Exporting proc_batch output: {proc_batch_id}")
        if not self.exporter.export_results(processing_results):
            logger.warning(f"Could not export proc_batch {proc_batch_id} output")
            return False

        logger.info(f"Successfully exported proc_batch {proc_batch_id} output")
        return True

    """ ------------ FUNCTIONS TO TRIGGER PARTS OF THE WORKFLOW (WITHOUT KEEPING STATUS) -------------- """

    # use this to fetch a single processing result of a known target_id
    def trigger_fetch_result_single_target_id(
        self, target_id: str
    ) -> Optional[ProcessingResult]:
        logger.info(f"Looking for a processing result for: {target_id}")
        processing_result = self.data_processing_env.fetch_result_of_target_id(
            target_id
        )
        logger.info(f"Found a processing result: {processing_result is not None}")
        return processing_result

    # use this to export the results of a know target_id (that should have processing results ready)
    def trigger_export_single_target_id(self, target_id: str) -> bool:
        logger.info(f"Triggering export for: {target_id}")
        processing_result = self.trigger_fetch_result_single_target_id(target_id)
        if processing_result:
            logger.info("Found processing data: passing it to the exporter...")
            return self.exporter.export_results([processing_result])
        logger.error(f"Cannot export: no processing result found for: {target_id}")
        return False

    # use this to export a certain proc_batch (that already has been processed)
    def trigger_export_proc_batch_id(self, proc_batch_id: int) -> bool:
        processing_results = self._fetch_proc_batch_output(proc_batch_id)
        if processing_results and self._export_proc_batch_output(
            proc_batch_id, processing_results
        ):
            return True
        else:
            return False
