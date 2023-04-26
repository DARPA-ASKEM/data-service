# ProvenanceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_provenance_provenance_post**](ProvenanceApi.md#create_provenance_provenance_post) | **POST** /provenance | Create Provenance
[**delete_hanging_nodes_provenance_hanging_nodes_delete**](ProvenanceApi.md#delete_hanging_nodes_provenance_hanging_nodes_delete) | **DELETE** /provenance/hanging_nodes | Delete Hanging Nodes
[**delete_provenance_provenance_id_delete**](ProvenanceApi.md#delete_provenance_provenance_id_delete) | **DELETE** /provenance/{id} | Delete Provenance
[**get_provenance_provenance_get**](ProvenanceApi.md#get_provenance_provenance_get) | **GET** /provenance | Get Provenance
[**search_provenance_provenance_search_post**](ProvenanceApi.md#search_provenance_provenance_search_post) | **POST** /provenance/search | Search Provenance


# **create_provenance_provenance_post**
> create_provenance_provenance_post(_api::ProvenanceApi, provenance::Provenance; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_provenance_provenance_post(_api::ProvenanceApi, response_stream::Channel, provenance::Provenance; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Provenance

Create provenance relationship

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProvenanceApi** | API context | 
**provenance** | [**Provenance**](Provenance.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_hanging_nodes_provenance_hanging_nodes_delete**
> delete_hanging_nodes_provenance_hanging_nodes_delete(_api::ProvenanceApi; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_hanging_nodes_provenance_hanging_nodes_delete(_api::ProvenanceApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Hanging Nodes

Prunes nodes that have 0 edges

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

# **delete_provenance_provenance_id_delete**
> delete_provenance_provenance_id_delete(_api::ProvenanceApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_provenance_provenance_id_delete(_api::ProvenanceApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Provenance

Delete provenance metadata

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProvenanceApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_provenance_provenance_get**
> get_provenance_provenance_get(_api::ProvenanceApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_provenance_provenance_get(_api::ProvenanceApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Provenance

Searches for a provenance entry in TDS

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProvenanceApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **search_provenance_provenance_search_post**
> search_provenance_provenance_search_post(_api::ProvenanceApi, provenance_payload::ProvenancePayload; search_type=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> search_provenance_provenance_search_post(_api::ProvenanceApi, response_stream::Channel, provenance_payload::ProvenancePayload; search_type=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Search Provenance

Search provenance of for all artifacts that helped derive this artifact.  ## Types of searches:  **artifacts_created_by_user** - Return all artifacts created by a user. * Requirements: “user_id”  **model_to_primitive** - Return all models and the intermediates  they are derived from. * Requirements: None  **child_nodes** - Returns all child nodes of this artifact. (In other words artifacts created after this artifact  that were dependent/derived from the root artifact). * Requirements: “root_type”, “root_id”   **parent_nodes** - Return all parent nodes of this artifact. (Artifacts created before this artifact that help derive/create this root artifact). * Requirements: “root_type”, “root_id”  **connected_nodes** - Return all parent and child nodes  of this artifact. * Requirements: “root_type”, “root_id”   **derived_models** - Return all models that were derived     from a publication or intermediate. * Requirements: “root_type”, “root_id” * Allowed root _types are Publication and Intermediate   **parent_model_revisions** - Returns the model revisions that helped create the model that was used to create the root artifact. * Requirements: “root_type”, “root_id” * Allowed root _types are Model, Plan, SimulationRun, and Dataset   **parent_models** - Returns the models that helped create  the model that was used to create the root artifact. * Requirements: “root_type”, “root_id” * Allowed root _types are Model *will be expanded.  ## Payload format  The payload for searching needs to match the schema below.  Provenance Types are : Dataset, Model, ModelParameter, Plan, PlanParameter, ModelRevision, Intermediate, Publication, SimulationRun, Project, Concept.   ***edges*** set to true: edges will be returned if found  ***nodes*** set to true: nodes will not be returned if found  ***types*** filters node types you want returned.  ***hops*** limits the number of relationships away from the root node the search will traverse.  ***limit*** will limit the number of nodes returned for relationship and nodes.   The closest n number of nodes to the root node will be returned. There might   not be the exact the number of nodes returned as requested due to filtering   out node types.  ***versions*** set to true will return model revisions in edges. Versions set to  false will squash all model revisions to the  Model node they are associated with along with all the relationships connected  to model revisions      {         \"root_id\": 1,         \"root_type\": \"Publication\",         \"curie\": \"string\",         \"edges\": false,         \"nodes\": true,         \"types\": [             \"Dataset\",             \"Intermediate\",             \"Model\",             \"ModelParameter\",             \"Plan\",             \"PlanParameter\",             \"Publication\",             \"SimulationRun\"         ],         \"hops\": 15,         \"limit\": 1000,         \"versions\": false     }

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ProvenanceApi** | API context | 
**provenance_payload** | [**ProvenancePayload**](ProvenancePayload.md)|  | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_type** | [**ProvenanceSearchTypes**](.md)|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

