# PersonsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_association_persons_associations_post**](PersonsApi.md#create_association_persons_associations_post) | **POST** /persons/associations | Create Association
[**create_person_persons_post**](PersonsApi.md#create_person_persons_post) | **POST** /persons | Create Person
[**delete_association_persons_associations_id_delete**](PersonsApi.md#delete_association_persons_associations_id_delete) | **DELETE** /persons/associations/{id} | Delete Association
[**delete_person_persons_id_delete**](PersonsApi.md#delete_person_persons_id_delete) | **DELETE** /persons/{id} | Delete Person
[**get_association_persons_associations_id_get**](PersonsApi.md#get_association_persons_associations_id_get) | **GET** /persons/associations/{id} | Get Association
[**get_person_persons_id_get**](PersonsApi.md#get_person_persons_id_get) | **GET** /persons/{id} | Get Person
[**get_persons_persons_get**](PersonsApi.md#get_persons_persons_get) | **GET** /persons | Get Persons
[**update_association_persons_associations_id_patch**](PersonsApi.md#update_association_persons_associations_id_patch) | **PATCH** /persons/associations/{id} | Update Association
[**update_person_persons_id_patch**](PersonsApi.md#update_person_persons_id_patch) | **PATCH** /persons/{id} | Update Person


# **create_association_persons_associations_post**
> create_association_persons_associations_post(_api::PersonsApi, association::Association; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_association_persons_associations_post(_api::PersonsApi, response_stream::Channel, association::Association; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Association

Create a association

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**association** | [**Association**](Association.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_person_persons_post**
> create_person_persons_post(_api::PersonsApi, person::Person; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_person_persons_post(_api::PersonsApi, response_stream::Channel, person::Person; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Person

Create a person

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**person** | [**Person**](Person.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_association_persons_associations_id_delete**
> delete_association_persons_associations_id_delete(_api::PersonsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_association_persons_associations_id_delete(_api::PersonsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Association

Delete a association by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_person_persons_id_delete**
> delete_person_persons_id_delete(_api::PersonsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_person_persons_id_delete(_api::PersonsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Person

Delete a person by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_association_persons_associations_id_get**
> get_association_persons_associations_id_get(_api::PersonsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_association_persons_associations_id_get(_api::PersonsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Association

Get a specific association by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_person_persons_id_get**
> get_person_persons_id_get(_api::PersonsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_person_persons_id_get(_api::PersonsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Person

Get a specific person by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_persons_persons_get**
> get_persons_persons_get(_api::PersonsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_persons_persons_get(_api::PersonsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Persons

Page over persons

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 

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

# **update_association_persons_associations_id_patch**
> update_association_persons_associations_id_patch(_api::PersonsApi, id::Int64, association::Association; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_association_persons_associations_id_patch(_api::PersonsApi, response_stream::Channel, id::Int64, association::Association; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Association

Update a association by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**association** | [**Association**](Association.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_person_persons_id_patch**
> update_person_persons_id_patch(_api::PersonsApi, id::Int64, person::Person; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_person_persons_id_patch(_api::PersonsApi, response_stream::Channel, id::Int64, person::Person; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Person

Update a person by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **PersonsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**person** | [**Person**](Person.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

