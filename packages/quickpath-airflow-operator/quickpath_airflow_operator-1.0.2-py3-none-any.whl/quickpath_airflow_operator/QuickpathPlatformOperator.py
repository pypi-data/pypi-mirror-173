from airflow.models.baseoperator import BaseOperator
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from . import QuickpathPlatformAPIHook
from .QuickpathPlatformServiceHook import QuickpathPlatformServiceHook
import time
from typing import Optional, Dict, Any

class QuickpathPlatformOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        service_connection_id: str,
        api_connection_id: str,
        environment_name: str,
        blueprint_endpoint: str,
        blueprint_version: str = None,
        request_object: Optional[Dict[str, Any]] = None,
        synchronous: bool = True,
        poll_for_results: bool = False,
        max_polls: int = 20,
        poll_interval: int = 5,
        **kwargs,
    ) -> None:
        """
        :param service_connection_id: The Airflow Connection ID for the Quickpath Platform Service
        :type service_connection_id: str
        :param api_connection_id: The Airflow Connection ID for the Quickpath Platform API
        :type api_connection_id: str
        :param environment_name: The Quickpath Platform Environment Name
        :type environment_name: str
        :param blueprint_endpoint: The Quickpath Platform Blueprint Endpoint
        :type blueprint_endpoint: str
        :param blueprint_version: The Quickpath Platform Blueprint Version
        :type blueprint_version: str
        :param request_object: The Quickpath Platform Blueprint Request Object
        :type request_object: Optional[Dict[str, Any]]
        :param synchronous: Whether to execute the blueprint synchronously or asynchronously
        :type synchronous: bool
        :param poll_for_results: Whether to poll for results if executing asynchronously
        :type poll_for_results: bool
        :param max_polls: The maximum number of polls to make if polling for results
        :type max_polls: int
        :param poll_interval: The number of seconds to wait between polls
        :type poll_interval: int        
        """
        super().__init__(**kwargs)
        self.service_connection_id = service_connection_id
        self.api_connection_id = api_connection_id
        self.environment_name = environment_name
        self.blueprint_endpoint = blueprint_endpoint
        self.blueprint_version = blueprint_version
        self.request_object = request_object
        self.synchronous = synchronous
        self.poll_for_results = poll_for_results
        self.max_polls = max_polls
        self.poll_interval = poll_interval

    def execute(self, context):
        """
        Execute the Quickpath Platform Blueprint
        
        If `synchronous` is True, the blueprint will be executed synchronously and the results will be returned.

        If `synchronous` is False, the blueprint will be executed asynchronously and the UUID of the execution will be returned.
        If `poll_for_results` is True, the blueprint will be polled for results until the blueprint completes or `max_polls` is reached.

        If the blueprint fails, an AirflowException will be raised
        """
        quickpath_service_hook = QuickpathPlatformServiceHook(quickpath_group_connection_id=self.service_connection_id)
        if not self.synchronous:
            self.request_object['execute_async'] = True

        response = quickpath_service_hook.execute_blueprint(
            environment_name=self.environment_name,
            blueprint_endpoint=self.blueprint_endpoint,
            blueprint_version=self.blueprint_version,
            request_object=self.request_object
        )
        blueprint_uuid = response['uuid']
        context['task_instance'].xcom_push(key="blueprint_uuid", value=blueprint_uuid)
        if self.synchronous:
            context['task_instance'].xcom_push(key="blueprint_response", value=response['result'])
        elif not self.synchronous:
            if self.poll_for_results:
                quickpath_api_hook = QuickpathPlatformAPIHook(quickpath_user_connection_id=self.api_connection_id)
                time.sleep(5)
                for x in range(1, self.max_polls):
                    self.log.info(f"Polling for results: Interval {x}")
                    response = quickpath_api_hook.get_blueprint_execution_results(
                        environment_name=self.environment_name,
                        execution_uuid=blueprint_uuid
                    )
                    if response["COMPLETED"]:
                        if response['IS_FAILURE']:
                            raise AirflowException(f"Blueprint Execution Failed: Error Message NOT IMPLEMENTED")
                        context['task_instance'].xcom_push(key="blueprint_response", value=response['RESPONSE_OBJECT'])
                        return response['RESPONSE_OBJECT']
                    else:
                        if x == self.max_polls:
                            raise AirflowException(f"Get Blueprint Execution Results Failed: Max Polls Reached before blueprint completion")
                        time.sleep(self.poll_interval)
        return response