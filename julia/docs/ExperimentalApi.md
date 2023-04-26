# ExperimentalApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_to_cypher_experimental_cql_get**](ExperimentalApi.md#convert_to_cypher_experimental_cql_get) | **GET** /experimental/cql | Convert To Cypher
[**search_provenance_experimental_provenance_get**](ExperimentalApi.md#search_provenance_experimental_provenance_get) | **GET** /experimental/provenance | Search Provenance
[**set_properties_experimental_set_properties_get**](ExperimentalApi.md#set_properties_experimental_set_properties_get) | **GET** /experimental/set_properties | Set Properties


# **convert_to_cypher_experimental_cql_get**
> convert_to_cypher_experimental_cql_get(_api::ExperimentalApi, query::String; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> convert_to_cypher_experimental_cql_get(_api::ExperimentalApi, response_stream::Channel, query::String; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Convert To Cypher

Convert English to Cypher.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExperimentalApi** | API context | 
**query** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **search_provenance_experimental_provenance_get**
> search_provenance_experimental_provenance_get(_api::ExperimentalApi, query::String; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> search_provenance_experimental_provenance_get(_api::ExperimentalApi, response_stream::Channel, query::String; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Search Provenance

Convert English to Cypher.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExperimentalApi** | API context | 
**query** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **set_properties_experimental_set_properties_get**
> set_properties_experimental_set_properties_get(_api::ExperimentalApi; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> set_properties_experimental_set_properties_get(_api::ExperimentalApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Set Properties

Modify DB contents to work with Neoviz

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

