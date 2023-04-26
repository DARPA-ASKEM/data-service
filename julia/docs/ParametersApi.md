# ParametersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_parameters_parameters_post**](ParametersApi.md#create_parameters_parameters_post) | **POST** /parameters | Create Parameters
[**get_parameters_parameters_get**](ParametersApi.md#get_parameters_parameters_get) | **GET** /parameters | Get Parameters


# **create_parameters_parameters_post**
> create_parameters_parameters_post(_api::ParametersApi, independent_parameter::Vector{IndependentParameter}; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_parameters_parameters_post(_api::ParametersApi, response_stream::Channel, independent_parameter::Vector{IndependentParameter}; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Parameters

Create parameters from a list

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ParametersApi** | API context | 
**independent_parameter** | [**Vector{IndependentParameter}**](IndependentParameter.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_parameters_parameters_get**
> get_parameters_parameters_get(_api::ParametersApi; page=nothing, page_size=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_parameters_parameters_get(_api::ParametersApi, response_stream::Channel; page=nothing, page_size=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Parameters

Retrieve parameters

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ParametersApi** | API context | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **Int64**|  | [default to 0]
 **page_size** | **Int64**|  | [default to 100]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

