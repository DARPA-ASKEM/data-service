# ProjectsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_asset_projects_project_id_assets_resource_type_resource_id_post**](ProjectsApi.md#create_asset_projects_project_id_assets_resource_type_resource_id_post) | **POST** /projects/{project_id}/assets/{resource_type}/{resource_id} | Create Asset
[**create_project_projects_post**](ProjectsApi.md#create_project_projects_post) | **POST** /projects | Create Project
[**deactivate_project_projects_id_delete**](ProjectsApi.md#deactivate_project_projects_id_delete) | **DELETE** /projects/{id} | Deactivate Project
[**delete_asset_projects_project_id_assets_resource_type_resource_id_delete**](ProjectsApi.md#delete_asset_projects_project_id_assets_resource_type_resource_id_delete) | **DELETE** /projects/{project_id}/assets/{resource_type}/{resource_id} | Delete Asset
[**get_project_assets_projects_id_assets_get**](ProjectsApi.md#get_project_assets_projects_id_assets_get) | **GET** /projects/{id}/assets | Get Project Assets
[**get_project_projects_id_get**](ProjectsApi.md#get_project_projects_id_get) | **GET** /projects/{id} | Get Project
[**list_projects_projects_get**](ProjectsApi.md#list_projects_projects_get) | **GET** /projects | List Projects
[**update_project_projects_id_put**](ProjectsApi.md#update_project_projects_id_put) | **PUT** /projects/{id} | Update Project


# **create_asset_projects_project_id_assets_resource_type_resource_id_post**
> create_asset_projects_project_id_assets_resource_type_resource_id_post(_api::ProjectsApi, project_id::Int64, resource_type::ResourceType, resource_id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_asset_projects_project_id_assets_resource_type_resource_id_post(_api::ProjectsApi, response_stream::Channel, project_id::Int64, resource_type::ResourceType, resource_id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Asset

Create asset and return its ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**project_id** | **Int64**|  | [default to nothing]
**resource_type** | [**ResourceType**](.md)|  | [default to nothing]
**resource_id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_project_projects_post**
> create_project_projects_post(_api::ProjectsApi, project::Project; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_project_projects_post(_api::ProjectsApi, response_stream::Channel, project::Project; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Project

Create project and return its ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**project** | [**Project**](Project.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **deactivate_project_projects_id_delete**
> deactivate_project_projects_id_delete(_api::ProjectsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> deactivate_project_projects_id_delete(_api::ProjectsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Deactivate Project

Deactivate project

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_asset_projects_project_id_assets_resource_type_resource_id_delete**
> delete_asset_projects_project_id_assets_resource_type_resource_id_delete(_api::ProjectsApi, project_id::Int64, resource_type::ResourceType, resource_id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_asset_projects_project_id_assets_resource_type_resource_id_delete(_api::ProjectsApi, response_stream::Channel, project_id::Int64, resource_type::ResourceType, resource_id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Asset

Remove asset

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**project_id** | **Int64**|  | [default to nothing]
**resource_type** | [**ResourceType**](.md)|  | [default to nothing]
**resource_id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_project_assets_projects_id_assets_get**
> get_project_assets_projects_id_assets_get(_api::ProjectsApi, id::Int64; types=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_project_assets_projects_id_assets_get(_api::ProjectsApi, response_stream::Channel, id::Int64; types=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Project Assets

Retrieve project assets

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **types** | [**Vector{ResourceType}**](ResourceType.md)|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_project_projects_id_get**
> get_project_projects_id_get(_api::ProjectsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_project_projects_id_get(_api::ProjectsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Project

Retrieve project

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **list_projects_projects_get**
> list_projects_projects_get(_api::ProjectsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> list_projects_projects_get(_api::ProjectsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

List Projects

Retrieve all projects

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **Int64**|  | [default to 50]
 **page** | **Int64**|  | [default to 0]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_project_projects_id_put**
> update_project_projects_id_put(_api::ProjectsApi, id::Int64, project::Project; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_project_projects_id_put(_api::ProjectsApi, response_stream::Channel, id::Int64, project::Project; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Project

Update project

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProjectsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**project** | [**Project**](Project.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

