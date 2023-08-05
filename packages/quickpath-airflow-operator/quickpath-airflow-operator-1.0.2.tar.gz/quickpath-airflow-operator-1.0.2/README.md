# Quickpath Airflow Operator
Allows from Execution of Blueprints on the Quickpath Platform from within Airflow

# Installation
`pip install quickpath-airflow-operator`

# Connections
Connections can be created as `HTTP` Type

## Service Connection (QPP-Group)
Service Connection is Required for Blueprint Execution

    Connection ID = `QPP-Group`
    Connection Type = `HTTP`
    Schema = `https`
    Host = `<Quickpath_platform_base_url>`
    Password = `<Group API Key>`

## API Connection (QPP-User)
API Connection is only required if `poll_for_results=True`

    Connection ID = `QPP-User`
    Connection Type = `HTTP`
    Schema = `https`
    Host = `<Quickpath_platform_base_url>`
    Password = `<User API Key>`


# Usage

### Import
```
from quickpath_airflow_operator import QuickpathPlatformOperator`
```
---------------

### Syncronous Execution will execute a blueprint, wait for the result, and return it
```
quickpath_execution = QuickpathPlatformOperator(
    task_id="run_blueprint",
    service_connection_id="QPP-Group",
    api_connection_id="QPP-User",
    environment_name="design",
    blueprint_endpoint="blueprint_endpoint",
    request_object={},
    synchronous=True,
)
```
Produces XCom Keys `blueprint_uuid` and `blueprint_response`

-------------

### Asyncronous Execution With Result Polling will execute a blueprint and poll for the blueprint resultsAsyncronous Execution will execute a blueprint and return the Blueprint UUID
```
quickpath_execution = QuickpathPlatformOperator(
    task_id="run_blueprint",
    service_connection_id="QPP-Group",
    api_connection_id="QPP-User",
    environment_name="design",
    blueprint_endpoint="blueprint_endpoint",
    request_object={},
    synchronous=False,
    poll_for_results=True,
    max_polls=20,
    poll_interval=5
)
```
Produces XCom Keys `blueprint_uuid`

-----------------------
### Asyncronous Execution will execute a blueprint and return the Blueprint UUID
```
quickpath_execution = QuickpathPlatformOperator(
    task_id="run_blueprint",
    service_connection_id="QPP-Group",
    api_connection_id="QPP-User",
    environment_name="design",
    blueprint_endpoint="blueprint_endpoint",
    request_object={},
    synchronous=False,
    poll_for_results=True,
)
```
Produces XCom Keys `blueprint_uuid` and `blueprint_response`
