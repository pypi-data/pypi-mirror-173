from airflow.exceptions import AirflowException
try:
    from airflow.providers.http.hooks.http import HttpHook
except ImportError:
    from airflow.hooks.http_hook import HttpHook
from typing import Optional, Dict, Any


class QuickpathPlatformServiceHook(HttpHook):
    def __init__(
        self,
        quickpath_group_connection_id: str = "QPP-GROUP",
    ):
        self.quickpath_group_connection_id = quickpath_group_connection_id
        super().__init__(http_conn_id=quickpath_group_connection_id)

    def execute_blueprint(
        self,
        environment_name: str,
        blueprint_endpoint: str,
        blueprint_version: str = None,
        request_object: Optional[Dict[str, Any]] = None,
    ):
        conn = self.get_connection(self.quickpath_group_connection_id)
        api_key = conn.password

        endpoint = "/"
        if conn.host.endswith("/"):
            endpoint = ""

        endpoint += f"api/service/{blueprint_endpoint}/{environment_name}"
        if blueprint_version:
            endpoint += f"/{blueprint_version}"

        user_agent = "AirflowQuickpathPlatformOperator"
        headers = {
            "accept": "application/json",
            "API-Key": api_key,
            "User-Agent": user_agent,
        }
        self.log.info(f"Request Object: {request_object}")
        try:
            self.method = "post"
            response = self.run(
                endpoint=endpoint,
                json=request_object,
                headers=headers,
            )
            response = response.json()
        except AirflowException as e:
            self.log.error(f"Blueprint Execution Failed: {e}")

        self.log.info(f"Blueprint Execution Response: {response}")
        return response