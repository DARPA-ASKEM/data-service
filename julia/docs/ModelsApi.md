# ModelsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_framework_models_frameworks_post**](ModelsApi.md#create_framework_models_frameworks_post) | **POST** /models/frameworks | Create Framework
[**create_intermediate_models_intermediates_post**](ModelsApi.md#create_intermediate_models_intermediates_post) | **POST** /models/intermediates | Create Intermediate
[**create_model_models_post**](ModelsApi.md#create_model_models_post) | **POST** /models | Create Model
[**delete_framework_models_frameworks_name_delete**](ModelsApi.md#delete_framework_models_frameworks_name_delete) | **DELETE** /models/frameworks/{name} | Delete Framework
[**delete_intermediate_models_intermediates_id_delete**](ModelsApi.md#delete_intermediate_models_intermediates_id_delete) | **DELETE** /models/intermediates/{id} | Delete Intermediate
[**get_framework_models_frameworks_name_get**](ModelsApi.md#get_framework_models_frameworks_name_get) | **GET** /models/frameworks/{name} | Get Framework
[**get_intermediate_models_intermediates_id_get**](ModelsApi.md#get_intermediate_models_intermediates_id_get) | **GET** /models/intermediates/{id} | Get Intermediate
[**get_model_description_models_id_descriptions_get**](ModelsApi.md#get_model_description_models_id_descriptions_get) | **GET** /models/{id}/descriptions | Get Model Description
[**get_model_models_id_get**](ModelsApi.md#get_model_models_id_get) | **GET** /models/{id} | Get Model
[**get_model_parameters_models_id_parameters_get**](ModelsApi.md#get_model_parameters_models_id_parameters_get) | **GET** /models/{id}/parameters | Get Model Parameters
[**get_single_model_parameter_models_model_parameters_id_get**](ModelsApi.md#get_single_model_parameter_models_model_parameters_id_get) | **GET** /models/model_parameters/{id} | Get Single Model Parameter
[**list_model_descriptions_models_descriptions_get**](ModelsApi.md#list_model_descriptions_models_descriptions_get) | **GET** /models/descriptions | List Model Descriptions
[**model_opt_models_opts_model_operation_post**](ModelsApi.md#model_opt_models_opts_model_operation_post) | **POST** /models/opts/{model_operation} | Model Opt
[**update_model_models_id_post**](ModelsApi.md#update_model_models_id_post) | **POST** /models/{id} | Update Model
[**update_model_parameters_models_id_parameters_put**](ModelsApi.md#update_model_parameters_models_id_parameters_put) | **PUT** /models/{id}/parameters | Update Model Parameters


# **create_framework_models_frameworks_post**
> create_framework_models_frameworks_post(_api::ModelsApi, model_framework::ModelFramework; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_framework_models_frameworks_post(_api::ModelsApi, response_stream::Channel, model_framework::ModelFramework; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Framework

Create framework metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**model_framework** | [**ModelFramework**](ModelFramework.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_intermediate_models_intermediates_post**
> create_intermediate_models_intermediates_post(_api::ModelsApi, intermediate::Intermediate; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_intermediate_models_intermediates_post(_api::ModelsApi, response_stream::Channel, intermediate::Intermediate; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Intermediate

Create intermediate and return its ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**intermediate** | [**Intermediate**](Intermediate.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_model_models_post**
> create_model_models_post(_api::ModelsApi, model::Model; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_model_models_post(_api::ModelsApi, response_stream::Channel, model::Model; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Model

Create model and return its ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**model** | [**Model**](Model.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_framework_models_frameworks_name_delete**
> delete_framework_models_frameworks_name_delete(_api::ModelsApi, name::String; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_framework_models_frameworks_name_delete(_api::ModelsApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Framework

Delete framework metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_intermediate_models_intermediates_id_delete**
> delete_intermediate_models_intermediates_id_delete(_api::ModelsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_intermediate_models_intermediates_id_delete(_api::ModelsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Intermediate

Delete framework metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_framework_models_frameworks_name_get**
> get_framework_models_frameworks_name_get(_api::ModelsApi, name::String; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_framework_models_frameworks_name_get(_api::ModelsApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Framework

Retrieve framework metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_intermediate_models_intermediates_id_get**
> get_intermediate_models_intermediates_id_get(_api::ModelsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_intermediate_models_intermediates_id_get(_api::ModelsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Intermediate

Retrieve model

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_model_description_models_id_descriptions_get**
> get_model_description_models_id_descriptions_get(_api::ModelsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_model_description_models_id_descriptions_get(_api::ModelsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Model Description

Retrieve model

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_model_models_id_get**
> get_model_models_id_get(_api::ModelsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_model_models_id_get(_api::ModelsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Model

Retrieve model

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_model_parameters_models_id_parameters_get**
> get_model_parameters_models_id_parameters_get(_api::ModelsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_model_parameters_models_id_parameters_get(_api::ModelsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Model Parameters

Retrieve model

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_single_model_parameter_models_model_parameters_id_get**
> get_single_model_parameter_models_model_parameters_id_get(_api::ModelsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_single_model_parameter_models_model_parameters_id_get(_api::ModelsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Single Model Parameter

Retrieve model parameter

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **list_model_descriptions_models_descriptions_get**
> list_model_descriptions_models_descriptions_get(_api::ModelsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> list_model_descriptions_models_descriptions_get(_api::ModelsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

List Model Descriptions

Retrieve all models  This will return the full list of models, even the previous ones from edit history.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 

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

# **model_opt_models_opts_model_operation_post**
> model_opt_models_opts_model_operation_post(_api::ModelsApi, model_operation::ModelOperations, model_opt_payload::ModelOptPayload; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> model_opt_models_opts_model_operation_post(_api::ModelsApi, response_stream::Channel, model_operation::ModelOperations, model_opt_payload::ModelOptPayload; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Model Opt

Make modeling operations.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**model_operation** | [**ModelOperations**](.md)|  | [default to nothing]
**model_opt_payload** | [**ModelOptPayload**](ModelOptPayload.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_model_models_id_post**
> update_model_models_id_post(_api::ModelsApi, id::Int64, model::Model; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_model_models_id_post(_api::ModelsApi, response_stream::Channel, id::Int64, model::Model; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Model

Update model content

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**model** | [**Model**](Model.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_model_parameters_models_id_parameters_put**
> update_model_parameters_models_id_parameters_put(_api::ModelsApi, id::Int64, request_body::Vector{Any}; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_model_parameters_models_id_parameters_put(_api::ModelsApi, response_stream::Channel, id::Int64, request_body::Vector{Any}; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Model Parameters

Update the parameters for a model

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ModelsApi** | API context | 
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

