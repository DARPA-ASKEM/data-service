# DatasetsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dataset_datasets_post**](DatasetsApi.md#create_dataset_datasets_post) | **POST** /datasets | Create Dataset
[**create_feature_datasets_features_post**](DatasetsApi.md#create_feature_datasets_features_post) | **POST** /datasets/features | Create Feature
[**create_qualifier_datasets_qualifiers_post**](DatasetsApi.md#create_qualifier_datasets_qualifiers_post) | **POST** /datasets/qualifiers | Create Qualifier
[**delete_dataset_datasets_id_delete**](DatasetsApi.md#delete_dataset_datasets_id_delete) | **DELETE** /datasets/{id} | Delete Dataset
[**delete_feature_datasets_features_id_delete**](DatasetsApi.md#delete_feature_datasets_features_id_delete) | **DELETE** /datasets/features/{id} | Delete Feature
[**delete_qualifier_datasets_qualifiers_id_delete**](DatasetsApi.md#delete_qualifier_datasets_qualifiers_id_delete) | **DELETE** /datasets/qualifiers/{id} | Delete Qualifier
[**deprecate_dataset_datasets_deprecate_id_post**](DatasetsApi.md#deprecate_dataset_datasets_deprecate_id_post) | **POST** /datasets/deprecate/{id} | Deprecate Dataset
[**get_csv_from_dataset_datasets_id_file_get**](DatasetsApi.md#get_csv_from_dataset_datasets_id_file_get) | **GET** /datasets/{id}/file | Get Csv From Dataset
[**get_csv_from_dataset_depr_datasets_id_download_rawfile_get**](DatasetsApi.md#get_csv_from_dataset_depr_datasets_id_download_rawfile_get) | **GET** /datasets/{id}/download/rawfile | Get Csv From Dataset Depr
[**get_dataset_datasets_id_get**](DatasetsApi.md#get_dataset_datasets_id_get) | **GET** /datasets/{id} | Get Dataset
[**get_datasets_datasets_get**](DatasetsApi.md#get_datasets_datasets_get) | **GET** /datasets | Get Datasets
[**get_feature_datasets_features_id_get**](DatasetsApi.md#get_feature_datasets_features_id_get) | **GET** /datasets/features/{id} | Get Feature
[**get_features_datasets_features_get**](DatasetsApi.md#get_features_datasets_features_get) | **GET** /datasets/features | Get Features
[**get_qualifier_datasets_qualifiers_id_get**](DatasetsApi.md#get_qualifier_datasets_qualifiers_id_get) | **GET** /datasets/qualifiers/{id} | Get Qualifier
[**get_qualifiers_datasets_qualifiers_get**](DatasetsApi.md#get_qualifiers_datasets_qualifiers_get) | **GET** /datasets/qualifiers | Get Qualifiers
[**search_feature_datasets_id_features_get**](DatasetsApi.md#search_feature_datasets_id_features_get) | **GET** /datasets/{id}/features | Search Feature
[**update_dataset_datasets_id_patch**](DatasetsApi.md#update_dataset_datasets_id_patch) | **PATCH** /datasets/{id} | Update Dataset
[**update_feature_datasets_features_id_patch**](DatasetsApi.md#update_feature_datasets_features_id_patch) | **PATCH** /datasets/features/{id} | Update Feature
[**update_qualifier_datasets_qualifiers_id_patch**](DatasetsApi.md#update_qualifier_datasets_qualifiers_id_patch) | **PATCH** /datasets/qualifiers/{id} | Update Qualifier
[**upload_file_datasets_id_file_post**](DatasetsApi.md#upload_file_datasets_id_file_post) | **POST** /datasets/{id}/file | Upload File
[**upload_file_depr_datasets_id_upload_file_post**](DatasetsApi.md#upload_file_depr_datasets_id_upload_file_post) | **POST** /datasets/{id}/upload/file | Upload File Depr


# **create_dataset_datasets_post**
> create_dataset_datasets_post(_api::DatasetsApi, dataset::Dataset; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_dataset_datasets_post(_api::DatasetsApi, response_stream::Channel, dataset::Dataset; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Dataset

Create a dataset

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**dataset** | [**Dataset**](Dataset.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_feature_datasets_features_post**
> create_feature_datasets_features_post(_api::DatasetsApi, feature::Feature; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_feature_datasets_features_post(_api::DatasetsApi, response_stream::Channel, feature::Feature; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Feature

Create a feature

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**feature** | [**Feature**](Feature.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **create_qualifier_datasets_qualifiers_post**
> create_qualifier_datasets_qualifiers_post(_api::DatasetsApi, body_create_qualifier_datasets_qualifiers_post::BodyCreateQualifierDatasetsQualifiersPost; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_qualifier_datasets_qualifiers_post(_api::DatasetsApi, response_stream::Channel, body_create_qualifier_datasets_qualifiers_post::BodyCreateQualifierDatasetsQualifiersPost; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Qualifier

Create a qualifier

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**body_create_qualifier_datasets_qualifiers_post** | [**BodyCreateQualifierDatasetsQualifiersPost**](BodyCreateQualifierDatasetsQualifiersPost.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_dataset_datasets_id_delete**
> delete_dataset_datasets_id_delete(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_dataset_datasets_id_delete(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Dataset

Delete a dataset by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_feature_datasets_features_id_delete**
> delete_feature_datasets_features_id_delete(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_feature_datasets_features_id_delete(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Feature

Delete a feature by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_qualifier_datasets_qualifiers_id_delete**
> delete_qualifier_datasets_qualifiers_id_delete(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_qualifier_datasets_qualifiers_id_delete(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Qualifier

Delete a qualifier by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **deprecate_dataset_datasets_deprecate_id_post**
> deprecate_dataset_datasets_deprecate_id_post(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> deprecate_dataset_datasets_deprecate_id_post(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Deprecate Dataset

Toggle a dataset's deprecated status by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_csv_from_dataset_datasets_id_file_get**
> get_csv_from_dataset_datasets_id_file_get(_api::DatasetsApi, id::Int64; wide_format=nothing, row_limit=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_csv_from_dataset_datasets_id_file_get(_api::DatasetsApi, response_stream::Channel, id::Int64; wide_format=nothing, row_limit=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Csv From Dataset

Gets the csv of an annotated dataset that is registered via the data-annotation tool.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wide_format** | **Bool**|  | [default to false]
 **row_limit** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_csv_from_dataset_depr_datasets_id_download_rawfile_get**
> get_csv_from_dataset_depr_datasets_id_download_rawfile_get(_api::DatasetsApi, id::Int64; wide_format=nothing, row_limit=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_csv_from_dataset_depr_datasets_id_download_rawfile_get(_api::DatasetsApi, response_stream::Channel, id::Int64; wide_format=nothing, row_limit=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Csv From Dataset Depr

Gets the csv of an annotated dataset that is registered via the data-annotation tool.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wide_format** | **Bool**|  | [default to false]
 **row_limit** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_dataset_datasets_id_get**
> get_dataset_datasets_id_get(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_dataset_datasets_id_get(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Dataset

Get a specific dataset by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_datasets_datasets_get**
> get_datasets_datasets_get(_api::DatasetsApi; page_size=nothing, page=nothing, is_sim_run=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_datasets_datasets_get(_api::DatasetsApi, response_stream::Channel; page_size=nothing, page=nothing, is_sim_run=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Datasets

Get a specific number of datasets

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **Int64**|  | [default to 100]
 **page** | **Int64**|  | [default to 0]
 **is_sim_run** | **Bool**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_feature_datasets_features_id_get**
> get_feature_datasets_features_id_get(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_feature_datasets_features_id_get(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Feature

Get a specific feature by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_features_datasets_features_get**
> get_features_datasets_features_get(_api::DatasetsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_features_datasets_features_get(_api::DatasetsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Features

Get a specified number of features

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 

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

# **get_qualifier_datasets_qualifiers_id_get**
> get_qualifier_datasets_qualifiers_id_get(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_qualifier_datasets_qualifiers_id_get(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Qualifier

Get a specific qualifier by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_qualifiers_datasets_qualifiers_get**
> get_qualifiers_datasets_qualifiers_get(_api::DatasetsApi; page_size=nothing, page=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_qualifiers_datasets_qualifiers_get(_api::DatasetsApi, response_stream::Channel; page_size=nothing, page=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Qualifiers

Get a specific number of qualifiers

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 

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

# **search_feature_datasets_id_features_get**
> search_feature_datasets_id_features_get(_api::DatasetsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> search_feature_datasets_id_features_get(_api::DatasetsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Search Feature

Search features by dataset id and/or name

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_dataset_datasets_id_patch**
> update_dataset_datasets_id_patch(_api::DatasetsApi, id::Int64, dataset::Dataset; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_dataset_datasets_id_patch(_api::DatasetsApi, response_stream::Channel, id::Int64, dataset::Dataset; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Dataset

Update a dataset by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**dataset** | [**Dataset**](Dataset.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_feature_datasets_features_id_patch**
> update_feature_datasets_features_id_patch(_api::DatasetsApi, id::Int64, feature::Feature; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_feature_datasets_features_id_patch(_api::DatasetsApi, response_stream::Channel, id::Int64, feature::Feature; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Feature

Update a feature by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**feature** | [**Feature**](Feature.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_qualifier_datasets_qualifiers_id_patch**
> update_qualifier_datasets_qualifiers_id_patch(_api::DatasetsApi, id::Int64, qualifier::Qualifier; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_qualifier_datasets_qualifiers_id_patch(_api::DatasetsApi, response_stream::Channel, id::Int64, qualifier::Qualifier; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Qualifier

Update a qualifier by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**qualifier** | [**Qualifier**](Qualifier.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **upload_file_datasets_id_file_post**
> upload_file_datasets_id_file_post(_api::DatasetsApi, id::Int64, file::String; filename=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> upload_file_datasets_id_file_post(_api::DatasetsApi, response_stream::Channel, id::Int64, file::String; filename=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Upload File

Upload a file to the DATASET_BASE_STORAGE_URL  Args:     id (int): Dataset ID.     file (UploadFile, optional): Upload of file-like object.     filename (Optional[str], optional): Allows the specification of     a particular filename at upload. Defaults to None.  Returns:     Reponse: FastAPI Response object containing     information about the uploaded file.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**file** | **String****String**|  | [default to nothing]

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **upload_file_depr_datasets_id_upload_file_post**
> upload_file_depr_datasets_id_upload_file_post(_api::DatasetsApi, id::Int64, file::String; filename=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> upload_file_depr_datasets_id_upload_file_post(_api::DatasetsApi, response_stream::Channel, id::Int64, file::String; filename=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Upload File Depr

Upload a file to the DATASET_BASE_STORAGE_URL  Args:     id (int): Dataset ID.     file (UploadFile, optional): Upload of file-like object.     filename (Optional[str], optional): Allows the specification of     a particular filename at upload. Defaults to None.  Returns:     Reponse: FastAPI Response object containing     information about the uploaded file.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **DatasetsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**file** | **String****String**|  | [default to nothing]

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

