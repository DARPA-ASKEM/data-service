# SimulationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_plan_simulations_plans_post**](SimulationsApi.md#create_plan_simulations_plans_post) | **POST** /simulations/plans | Create Plan
[**create_run_from_description_simulations_runs_descriptions_post**](SimulationsApi.md#create_run_from_description_simulations_runs_descriptions_post) | **POST** /simulations/runs/descriptions | Create Run From Description
[**create_run_simulations_runs_post**](SimulationsApi.md#create_run_simulations_runs_post) | **POST** /simulations/runs | Create Run
[**get_plan_simulations_plans_id_get**](SimulationsApi.md#get_plan_simulations_plans_id_get) | **GET** /simulations/plans/{id} | Get Plan
[**get_run_description_simulations_runs_id_descriptions_get**](SimulationsApi.md#get_run_description_simulations_runs_id_descriptions_get) | **GET** /simulations/runs/{id}/descriptions | Get Run Description
[**get_run_parameters_simulations_runs_id_parameters_get**](SimulationsApi.md#get_run_parameters_simulations_runs_id_parameters_get) | **GET** /simulations/runs/{id}/parameters | Get Run Parameters
[**get_run_simulations_runs_id_get**](SimulationsApi.md#get_run_simulations_runs_id_get) | **GET** /simulations/runs/{id} | Get Run
[**get_single_simulation_parameter_simulations_simulation_parameters_id_get**](SimulationsApi.md#get_single_simulation_parameter_simulations_simulation_parameters_id_get) | **GET** /simulations/simulation_parameters/{id} | Get Single Simulation Parameter
[**list_plans_simulations_plans_get**](SimulationsApi.md#list_plans_simulations_plans_get) | **GET** /simulations/plans | List Plans
[**list_run_descriptions_simulations_runs_descriptions_get**](SimulationsApi.md#list_run_descriptions_simulations_runs_descriptions_get) | **GET** /simulations/runs/descriptions | List Run Descriptions
[**update_run_parameters_simulations_runs_id_parameters_put**](SimulationsApi.md#update_run_parameters_simulations_runs_id_parameters_put) | **PUT** /simulations/runs/{id}/parameters | Update Run Parameters


# **create_plan_simulations_plans_post**
> create_plan_simulations_plans_post(_api::SimulationsApi, plan::Plan; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_plan_simulations_plans_post(_api::SimulationsApi, response_stream::Channel, plan::Plan; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Plan

Create plan and return its ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**plan** | [**Plan**](Plan.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_run_from_description_simulations_runs_descriptions_post**
> create_run_from_description_simulations_runs_descriptions_post(_api::SimulationsApi, run_description::RunDescription; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_run_from_description_simulations_runs_descriptions_post(_api::SimulationsApi, response_stream::Channel, run_description::RunDescription; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Run From Description

Create a run with no parameters initialized

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**run_description** | [**RunDescription**](RunDescription.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_run_simulations_runs_post**
> create_run_simulations_runs_post(_api::SimulationsApi, run::Run; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_run_simulations_runs_post(_api::SimulationsApi, response_stream::Channel, run::Run; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Run

Create run with parameters

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**run** | [**Run**](Run.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_plan_simulations_plans_id_get**
> get_plan_simulations_plans_id_get(_api::SimulationsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_plan_simulations_plans_id_get(_api::SimulationsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Plan

Retrieve plan

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_run_description_simulations_runs_id_descriptions_get**
> get_run_description_simulations_runs_id_descriptions_get(_api::SimulationsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_run_description_simulations_runs_id_descriptions_get(_api::SimulationsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Run Description

Retrieve run metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_run_parameters_simulations_runs_id_parameters_get**
> get_run_parameters_simulations_runs_id_parameters_get(_api::SimulationsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_run_parameters_simulations_runs_id_parameters_get(_api::SimulationsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Run Parameters

Get run parameters

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_run_simulations_runs_id_get**
> get_run_simulations_runs_id_get(_api::SimulationsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_run_simulations_runs_id_get(_api::SimulationsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Run

Retrieve full run

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_single_simulation_parameter_simulations_simulation_parameters_id_get**
> get_single_simulation_parameter_simulations_simulation_parameters_id_get(_api::SimulationsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_single_simulation_parameter_simulations_simulation_parameters_id_get(_api::SimulationsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Single Simulation Parameter

Retrieve simulation parameter

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **list_plans_simulations_plans_get**
> list_plans_simulations_plans_get(_api::SimulationsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> list_plans_simulations_plans_get(_api::SimulationsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

List Plans

Retrieve all plans

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **Int64**|  | [default to 100]
 **page** | **Int64**|  | [default to 0]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **list_run_descriptions_simulations_runs_descriptions_get**
> list_run_descriptions_simulations_runs_descriptions_get(_api::SimulationsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> list_run_descriptions_simulations_runs_descriptions_get(_api::SimulationsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

List Run Descriptions

Retrieve all simulation run for all plans

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **Int64**|  | [default to 100]
 **page** | **Int64**|  | [default to 0]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_run_parameters_simulations_runs_id_parameters_put**
> update_run_parameters_simulations_runs_id_parameters_put(_api::SimulationsApi, id::Int64, request_body::Vector{Any}; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_run_parameters_simulations_runs_id_parameters_put(_api::SimulationsApi, response_stream::Channel, id::Int64, request_body::Vector{Any}; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Run Parameters

Update the parameters for a run

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SimulationsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**request_body** | [**Vector{Any}**](Any.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

