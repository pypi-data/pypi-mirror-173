from airflow.exceptions import AirflowException
try:
    from airflow.providers.http.hooks.http import HttpHook
except ImportError:
    from airflow.hooks.http_hook import HttpHook

class QuickpathPlatformAPIHook(HttpHook):
    def __init__(
        self,
        quickpath_user_connection_id: str = "QPP-USER",
    ):
        self.quickpath_user_connection_id = quickpath_user_connection_id
        super().__init__(http_conn_id=quickpath_user_connection_id)

    
    def get_blueprint_execution_results(
        self,
        environment_name: str,
        execution_uuid: str
    ):
        conn = self.get_connection(self.quickpath_user_connection_id)
        api_key = conn.password

        endpoint = "/"
        if conn.host.endswith("/"):
            endpoint = ""
        endpoint += f"api/v2/blueprints/executions/{execution_uuid}/environments/{environment_name}/result"

        user_agent = "AirflowQuickpathPlatformOperator"
        headers = {
            "accept": "application/json",
            "API-Key": api_key,
            "User-Agent": user_agent,
        }

        try:
            self.method = "get"
            response = self.run(
                endpoint=endpoint,
                headers=headers,
            )
            response = response.json()
        except AirflowException as e:
            self.log.error(f"Get Blueprint Execution Results Failed: {e}")
            raise e

        self.log.info(f"Blueprint Execution Response: {response}")
        return response