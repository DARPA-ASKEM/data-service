# ExternalApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_publication_external_publications_post**](ExternalApi.md#create_publication_external_publications_post) | **POST** /external/publications | Create Publication
[**create_software_external_software_post**](ExternalApi.md#create_software_external_software_post) | **POST** /external/software | Create Software
[**delete_publication_external_publications_id_delete**](ExternalApi.md#delete_publication_external_publications_id_delete) | **DELETE** /external/publications/{id} | Delete Publication
[**delete_software_external_software_id_delete**](ExternalApi.md#delete_software_external_software_id_delete) | **DELETE** /external/software/{id} | Delete Software
[**get_publication_external_publications_id_get**](ExternalApi.md#get_publication_external_publications_id_get) | **GET** /external/publications/{id} | Get Publication
[**get_software_external_software_id_get**](ExternalApi.md#get_software_external_software_id_get) | **GET** /external/software/{id} | Get Software


# **create_publication_external_publications_post**
> create_publication_external_publications_post(_api::ExternalApi, publication::Publication; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_publication_external_publications_post(_api::ExternalApi, response_stream::Channel, publication::Publication; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Publication

Create publication and return its ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExternalApi** | API context | 
**publication** | [**Publication**](Publication.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_software_external_software_post**
> create_software_external_software_post(_api::ExternalApi, software::Software; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_software_external_software_post(_api::ExternalApi, response_stream::Channel, software::Software; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Software

Create software metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExternalApi** | API context | 
**software** | [**Software**](Software.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_publication_external_publications_id_delete**
> delete_publication_external_publications_id_delete(_api::ExternalApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_publication_external_publications_id_delete(_api::ExternalApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Publication

Delete publications metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExternalApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_software_external_software_id_delete**
> delete_software_external_software_id_delete(_api::ExternalApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_software_external_software_id_delete(_api::ExternalApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Software

Delete software metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExternalApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_publication_external_publications_id_get**
> get_publication_external_publications_id_get(_api::ExternalApi, id::Id; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_publication_external_publications_id_get(_api::ExternalApi, response_stream::Channel, id::Id; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Publication

Retrieve model

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExternalApi** | API context | 
**id** | [**Id**](.md)|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_software_external_software_id_get**
> get_software_external_software_id_get(_api::ExternalApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_software_external_software_id_get(_api::ExternalApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Software

Retrieve software metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ExternalApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

