from abc import ABC, abstractmethod
from uuid import uuid4
import logging
import sys
from typing import List, Optional
from dane_workflows.util.base_util import (
    check_setting,
    load_config_or_die,
    auto_create_dir,
)
from dane_workflows.status import StatusHandler, StatusRow, ProcessingStatus, ErrorCode
from dane_workflows.util.dane_util import DANEHandler, Task, Result, TaskType
from time import sleep
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ProcEnvResponse:
    success: bool
    status_code: int
    status_text: str


@dataclass
class ProcessingResult:
    status_row: StatusRow
    result_data: dict  # TODO: will also contain the prov info in the near future
    generator: dict  # contains information about the software generating the results


"""
This class is owned by a TaskScheduler to feed a batch of data (obtained from a DataProvider)
to an (external) data processing environment, such as DANE.

Important NOTE: for processing only a list of StatusRow objects are provided, which do only contain:
- target_id, i.e. ID of input document
- target_url, i.e. URL of content related to input document (could point to metadata)
- source_extra_info, i.e. variable text

If the actual processing environment requires textual input data, either:
- use the target_url to point to a metadata record or text resource
- call the DataProvider to fetch the textual records (TODO provide access to DataProvider in this class)
    - the DataProvider could e.g. fetch the required metadata:
        - from local storage OR simply fetch it from the source catalogue
        - as part of the StatusRow (TODO not implemented yet)
"""


class DataProcessingEnvironment(ABC):
    def __init__(self, config, status_handler: StatusHandler, unit_test: bool = False):

        self.config = (
            config["PROC_ENV"]["CONFIG"] if "CONFIG" in config["PROC_ENV"] else {}
        )
        self.status_handler = status_handler

        # enforce config validation
        if not self._validate_config():
            logger.critical("Malconfigured, quitting...")
            sys.exit()

    def _set_register_batch_failed(
        self, status_rows: List[StatusRow], proc_batch_id: int
    ):
        return self.status_handler.update_status_rows(
            status_rows,
            status=ProcessingStatus.ERROR,
            proc_status_msg=f"Could not register batch {proc_batch_id}",
            proc_error_code=ErrorCode.BATCH_REGISTER_FAILED,
        )

    def _set_by_processing_response(
        self, proc_batch_id: int, proc_env_resp: ProcEnvResponse
    ):
        status_rows = self.status_handler.get_status_rows_of_proc_batch(proc_batch_id)
        if status_rows is not None:
            return self.status_handler.update_status_rows(
                status_rows,
                status=ProcessingStatus.PROCESSING
                if proc_env_resp.success
                else ProcessingStatus.ERROR,
                proc_status_msg=proc_env_resp.status_text,
                proc_error_code=ErrorCode.BATCH_PROCESSING_NOT_STARTED
                if proc_env_resp.success is False
                else None,
            )
        return None

    def register_batch(
        self, proc_batch_id: int, batch: list
    ) -> Optional[List[StatusRow]]:
        status_rows = self._register_batch(proc_batch_id, batch)
        if status_rows is None:  # in case of an error update the status
            status_rows = self._set_register_batch_failed(batch, proc_batch_id)
        self.status_handler.persist_or_die(status_rows)
        return status_rows

    def process_batch(self, proc_batch_id: int) -> Optional[List[StatusRow]]:
        proc_env_resp = self._process_batch(proc_batch_id)
        status_rows = self._set_by_processing_response(proc_batch_id, proc_env_resp)
        self.status_handler.persist_or_die(status_rows)
        return status_rows

    def monitor_batch(self, proc_batch_id: int) -> Optional[List[StatusRow]]:
        status_rows = self._monitor_batch(proc_batch_id)
        if status_rows is None:
            logger.error(f"Monitoring of proc_batch {proc_batch_id} returned nothing")
        self.status_handler.persist_or_die(status_rows)
        return status_rows

    def fetch_results_of_batch(self, proc_batch_id: int):
        results = self._fetch_results_of_batch(proc_batch_id)
        if not results:  # empty or None is always bad
            logger.error(
                f"Error obtaining ProcessingResults for proc_batch {proc_batch_id}"
            )
            return None
        logger.info(f"Retrieved {len(results)} results for proc_batch {proc_batch_id}")
        status_rows = [
            r.status_row for r in results
        ]  # extract the status_rows from the results
        self.status_handler.persist_or_die(status_rows)
        return results

    @abstractmethod
    def fetch_result_of_target_id(self, target_id: str) -> Optional[ProcessingResult]:
        raise NotImplementedError(
            "(optional) Implement to fetch single items from your processing env"
        )

    @abstractmethod
    def _validate_config(self) -> bool:
        raise NotImplementedError("Implement to validate the config")

    @abstractmethod
    def _register_batch(
        self, proc_batch_id: int, batch: list
    ) -> Optional[List[StatusRow]]:
        raise NotImplementedError(
            "Implement to register batch to data processing environment"
        )

    @abstractmethod
    def _process_batch(self, proc_batch_id: int) -> ProcEnvResponse:
        raise NotImplementedError("Implement to start processing registered batch")

    @abstractmethod
    def _monitor_batch(
        self, proc_batch_id: int
    ) -> Optional[List[StatusRow]]:  # containing ids + statusses
        raise NotImplementedError(
            f"Implement to feed monitor batch with id {proc_batch_id}"
        )

    @abstractmethod  # TODO this method should also update al status_rows with row-level statusses
    def _fetch_results_of_batch(
        self, proc_batch_id: int
    ) -> Optional[List[ProcessingResult]]:
        raise NotImplementedError("Implement to fetch batch results")


class DANEEnvironment(DataProcessingEnvironment):
    def __init__(self, config, status_handler: StatusHandler, unit_test: bool = False):
        super().__init__(config, status_handler, unit_test)
        self.dane_handler = DANEHandler(self.config)

    def _validate_config(self):
        logger.info(f"Validating {self.__class__.__name__} config")
        try:
            assert all(
                [
                    x in self.config
                    for x in [
                        "DANE_HOST",
                        "DANE_TASK_ID",
                        "DANE_STATUS_DIR",
                        "DANE_MONITOR_INTERVAL",
                        "DANE_ES_HOST",
                        "DANE_ES_PORT",
                        "DANE_ES_INDEX",
                        "DANE_ES_QUERY_TIMEOUT",
                    ]
                ]
            ), "DANEEnvironment config incomplete"
            assert check_setting(
                self.config["DANE_TASK_ID"], str
            ), "DANEEnvironment.DANE_TASK_ID"
            try:
                TaskType(self.config["DANE_TASK_ID"])
            except ValueError:
                raise AssertionError(
                    "DANEEnvironment.DANE_TASK_ID: use a valid instance of dane_util.TaskType"
                )
            assert check_setting(
                self.config["DANE_HOST"], str
            ), "DANEEnvironment.DANE_HOST"
            assert check_setting(
                self.config["DANE_STATUS_DIR"], str
            ), "DANEEnvironment.DANE_STATUS_DIR"
            assert check_setting(
                self.config["DANE_MONITOR_INTERVAL"], int
            ), "DANEEnvironment.DANE_MONITOR_INTERVAL"
            assert check_setting(
                self.config["DANE_ES_HOST"], str
            ), "DANEEnvironment.DANE_ES_HOST"
            assert check_setting(
                self.config["DANE_ES_PORT"], int
            ), "DANEEnvironment.DANE_ES_PORT"
            assert check_setting(
                self.config["DANE_ES_INDEX"], str
            ), "DANEEnvironment.DANE_ES_INDEX"
            assert check_setting(
                self.config["DANE_ES_QUERY_TIMEOUT"], int
            ), "DANEEnvironment.DANE_ES_QUERY_TIMEOUT"

            assert (
                auto_create_dir(self.config["DANE_STATUS_DIR"]) is True
            ), f"DANE_STATUS_DIR: {self.config['DANE_STATUS_DIR']} auto creation failed"
        except AssertionError as e:
            logger.error(f"Configuration error: {str(e)}")
            return False

        return True

    # uploads batch as DANE Documents to DANE environment
    def _register_batch(
        self, proc_batch_id: int, batch: List[StatusRow]
    ) -> Optional[List[StatusRow]]:
        logger.info(f"Calling DANEHandler to register proc_batch: {proc_batch_id}")
        return self.dane_handler.register_batch(proc_batch_id, batch)

    # tells DANE to start processing Task=self.TASK_ID on registered docs
    def _process_batch(self, proc_batch_id: int) -> ProcEnvResponse:
        logger.info(
            f"Calling DANEHandler to start processing proc_batch: {proc_batch_id}"
        )
        success, status_code, response_text = self.dane_handler.process_batch(
            proc_batch_id
        )
        logger.info(f"DANE returned status: {status_code}")
        return ProcEnvResponse(success, status_code, response_text)

    # When finished returns a list of updated StatusRows
    def _monitor_batch(self, proc_batch_id: int) -> Optional[List[StatusRow]]:
        logger.info(f"Monitoring DANE batch #{proc_batch_id}")
        tasks_of_batch = self.dane_handler.monitor_batch(
            proc_batch_id, False  # no verbose output
        )
        # convert the DANE results to StatusRows and persist the status
        return self._to_status_rows(proc_batch_id, tasks_of_batch)

    # TaskScheduler calls this to fetch results of a finished batch
    def _fetch_results_of_batch(
        self, proc_batch_id: int
    ) -> Optional[List[ProcessingResult]]:
        logger.info(f"Asking DANEEnvironment for results of proc_batch {proc_batch_id}")

        # NOTE results may be empty in case the tasks were already done
        status_rows = self.status_handler.get_status_rows_of_proc_batch(proc_batch_id)
        results_of_batch = self.dane_handler.get_results_of_batch(proc_batch_id, [])
        tasks_of_batch = self.dane_handler.get_tasks_of_batch(proc_batch_id, [])

        num_status_rows = len(status_rows) if status_rows else 0
        logger.info(f"Number of status_rows found: {num_status_rows}")
        logger.info(f"Number of results found: {len(results_of_batch)}")
        logger.info(f"Number of tasks found: {len(tasks_of_batch)}")

        # generate warnings that are worth investigating. Maybe the status DB is
        # out of sync with the DANE DB (because of manual editing/testing)
        if num_status_rows > len(results_of_batch):
            logger.warning("Not all status_rows in this batch have DANE results")
        if num_status_rows > len(tasks_of_batch):
            logger.warning("Not all status_rows in this batch have DANE tasks")
        if num_status_rows < len(results_of_batch):
            logger.warning("There are more DANE results than status_rows in this batch")
        if num_status_rows < len(tasks_of_batch):
            logger.warning("There are more DANE tasks than status_rows in this batch")

        # convert the DANE Tasks and Results into ProcessingResults
        return self._to_processing_results(
            status_rows if status_rows else [], results_of_batch, tasks_of_batch
        )

    # TODO figure out how to make this work without status_rows...
    def fetch_result_of_target_id(self, target_id: str) -> Optional[ProcessingResult]:
        logger.info(f"Asking DANEEnvironment for result of target_id {target_id}")

        # NOTE results may be empty in case the tasks were already done
        status_row = self.status_handler.get_status_row_by_target_id(target_id)
        result = self.dane_handler.get_result_of_target_id(target_id)
        task = self.dane_handler.get_task_of_target_id(target_id)

        logger.info(f"StatusRow found {status_row is not None}")
        logger.info(f"Result found: {result is not None}")
        logger.info(f"Task found: {task is not None}")

        # convert the DANE Tasks and Results into ProcessingResults
        processing_results = self._to_processing_results(
            [status_row] if status_row else [],
            [result] if result else [],
            [task] if task else [],
        )
        return processing_results[0] if processing_results else None

    # Converts lists of matching StatusRows/Results/Tasks into ProcessingResults
    def _to_processing_results(
        self,
        status_rows_of_batch: List[StatusRow],
        results_of_batch: List[Result],
        tasks_of_batch: List[Task],
    ) -> Optional[List[ProcessingResult]]:

        if not status_rows_of_batch:
            logger.error("No status_rows provided, returning")
            return None

        if not results_of_batch:
            logger.error("No results provided, returning")
            return None

        if not tasks_of_batch:
            logger.error("No tasks found, returning")
            return None

        # First assign the doc_id, i.e. proc_id, to each processing result via the list of tasks
        task_id_to_doc_id = {task.id: task.doc_id for task in tasks_of_batch}
        for result in results_of_batch:
            result.doc_id = task_id_to_doc_id[result.task_id]

        # now convert the Result objects to ProcessingResult objects
        processing_results = []
        proc_id_to_result = {result.doc_id: result for result in results_of_batch}
        for row in status_rows_of_batch:
            row.status = ProcessingStatus.RESULTS_FETCHED  # update the status
            if row.proc_id in proc_id_to_result:
                processing_results.append(  # and add a processing result
                    ProcessingResult(
                        row,
                        proc_id_to_result[row.proc_id].payload,
                        proc_id_to_result[row.proc_id].generator,
                    )
                )
            else:
                logger.warning(
                    f"{row.proc_id} not found in DANE results, perhaps the task {result.task_id} could not finished because of failed dependencies"
                )
        return processing_results

    # Converts list of Task objects into StatusRows
    def _to_status_rows(self, proc_batch_id: int, tasks_of_batch: List[Task]):
        status_rows = self.status_handler.get_status_rows_of_proc_batch(proc_batch_id)
        if status_rows is None or tasks_of_batch is None or len(tasks_of_batch) == 0:
            logger.warning(
                f"Empty tasks_of_batch({tasks_of_batch}) or status_rows({status_rows})"
            )
            return None
        # Task.doc_id is used for more generic proc_id
        proc_id_to_task = {task.doc_id: task for task in tasks_of_batch}
        for row in status_rows:
            row.status = (
                ProcessingStatus.PROCESSED
                if proc_id_to_task[row.proc_id].state == 200
                else ProcessingStatus.ERROR
            )
        return status_rows


class ExampleDataProcessingEnvironment(DataProcessingEnvironment):
    def __init__(self, config, status_handler: StatusHandler, unit_test: bool = False):
        super().__init__(config, status_handler, unit_test)

    def _validate_config(self):
        return True

    # simulates receiving a successful registration of the batch in an external processing system
    def _register_batch(
        self, proc_batch_id: int, batch: List[StatusRow]
    ) -> Optional[List[StatusRow]]:
        logger.info(f"Registering (example) proc_batch: {proc_batch_id}")
        for row in batch:
            row.proc_id = str(uuid4())  # processing ID in processing env
            row.status = ProcessingStatus.BATCH_REGISTERED
        return batch

    # normally calls an external system to start processing, now just returns it's all good
    def _process_batch(self, proc_batch_id: int) -> ProcEnvResponse:
        logger.info(f"Processing (example) proc_batch: {proc_batch_id}")
        return ProcEnvResponse(True, 200, "All fine n dandy")

    # pretends that within 3 seconds the whole batch was successfully processed
    def _monitor_batch(self, proc_batch_id: int) -> Optional[List[StatusRow]]:
        logger.info(f"Monitoring (example) batch: {proc_batch_id}")
        status_rows = self.status_handler.get_status_rows_of_proc_batch(proc_batch_id)
        if status_rows is not None:
            for row in status_rows:
                row.status = ProcessingStatus.PROCESSED  # processing completed
            sleep(3)
        else:
            logger.warning(f"Processing Batch {proc_batch_id} failed")
        return status_rows

    def _fetch_results_of_batch(
        self, proc_batch_id: int
    ) -> Optional[List[ProcessingResult]]:
        logger.info(
            f"Asking (example) proc env for results of proc_batch {proc_batch_id}"
        )
        # just fetch the StatusRows, update their statusses and convert them into ProcessingResults
        status_rows = self.status_handler.get_status_rows_of_proc_batch(proc_batch_id)
        if status_rows is None:
            logger.warning(f"Could not retrieve data for proc_batch {proc_batch_id}")
            return None
        for row in status_rows:
            row.status = ProcessingStatus.RESULTS_FETCHED

        return [ProcessingResult(row, {}, {}) for row in status_rows]

    def fetch_result_of_target_id(self, target_id: str) -> Optional[ProcessingResult]:
        return None  # TODO implement


# Test your DataProcessingEnvironment in isolation
if __name__ == "__main__":
    from dane_workflows.status import SQLiteStatusHandler

    config = load_config_or_die("../config-example.yml")
    status_handler = SQLiteStatusHandler(config)
    dpe = DANEEnvironment(config, status_handler)
