# ConceptsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_concept_concepts_post**](ConceptsApi.md#create_concept_concepts_post) | **POST** /concepts | Create Concept
[**delete_concept_concepts_id_delete**](ConceptsApi.md#delete_concept_concepts_id_delete) | **DELETE** /concepts/{id} | Delete Concept
[**get_concept_concepts_id_get**](ConceptsApi.md#get_concept_concepts_id_get) | **GET** /concepts/{id} | Get Concept
[**get_concept_definition_concepts_definitions_curie_get**](ConceptsApi.md#get_concept_definition_concepts_definitions_curie_get) | **GET** /concepts/definitions/{curie} | Get Concept Definition
[**search_concept_concepts_get**](ConceptsApi.md#search_concept_concepts_get) | **GET** /concepts | Search Concept
[**search_concept_definitions_concepts_definitions_get**](ConceptsApi.md#search_concept_definitions_concepts_definitions_get) | **GET** /concepts/definitions | Search Concept Definitions
[**search_concept_using_facets_concepts_facets_get**](ConceptsApi.md#search_concept_using_facets_concepts_facets_get) | **GET** /concepts/facets | Search Concept Using Facets
[**update_concept_concepts_id_patch**](ConceptsApi.md#update_concept_concepts_id_patch) | **PATCH** /concepts/{id} | Update Concept


# **create_concept_concepts_post**
> create_concept_concepts_post(_api::ConceptsApi, ontology_concept::OntologyConcept; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> create_concept_concepts_post(_api::ConceptsApi, response_stream::Channel, ontology_concept::OntologyConcept; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Create Concept

Create a concept

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**ontology_concept** | [**OntologyConcept**](OntologyConcept.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **delete_concept_concepts_id_delete**
> delete_concept_concepts_id_delete(_api::ConceptsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> delete_concept_concepts_id_delete(_api::ConceptsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Delete Concept

Delete a concept by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_concept_concepts_id_get**
> get_concept_concepts_id_get(_api::ConceptsApi, id::Int64; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_concept_concepts_id_get(_api::ConceptsApi, response_stream::Channel, id::Int64; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Concept

Get a specific concept by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**id** | **Int64**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_concept_definition_concepts_definitions_curie_get**
> get_concept_definition_concepts_definitions_curie_get(_api::ConceptsApi, curie::String; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> get_concept_definition_concepts_definitions_curie_get(_api::ConceptsApi, response_stream::Channel, curie::String; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Get Concept Definition

Wraps fetch functionality from the DKG.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**curie** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **search_concept_concepts_get**
> search_concept_concepts_get(_api::ConceptsApi, curie::String; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> search_concept_concepts_get(_api::ConceptsApi, response_stream::Channel, curie::String; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Search Concept

Searches within TDS for artifacts with this concept term associated with them

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**curie** | **String**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **search_concept_definitions_concepts_definitions_get**
> search_concept_definitions_concepts_definitions_get(_api::ConceptsApi, term::String; limit=nothing, offset=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> search_concept_definitions_concepts_definitions_get(_api::ConceptsApi, response_stream::Channel, term::String; limit=nothing, offset=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Search Concept Definitions

Wraps search functionality from the DKG.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**term** | **String**|  | [default to nothing]

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **Int64**|  | [default to 100]
 **offset** | **Int64**|  | [default to 0]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **search_concept_using_facets_concepts_facets_get**
> search_concept_using_facets_concepts_facets_get(_api::ConceptsApi; types=nothing, curies=nothing, is_simulation=nothing, _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> search_concept_using_facets_concepts_facets_get(_api::ConceptsApi, response_stream::Channel; types=nothing, curies=nothing, is_simulation=nothing, _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Search Concept Using Facets

Search along type and curie facets

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 

### Optional Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **types** | [**Vector{TaggableType}**](TaggableType.md)|  | [default to nothing]
 **curies** | [**Vector{String}**](String.md)|  | [default to nothing]
 **is_simulation** | **Bool**|  | [default to nothing]

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_concept_concepts_id_patch**
> update_concept_concepts_id_patch(_api::ConceptsApi, id::Int64, ontology_concept::OntologyConcept; _mediaType=nothing) -> Any, OpenAPI.Clients.ApiResponse <br/>
> update_concept_concepts_id_patch(_api::ConceptsApi, response_stream::Channel, id::Int64, ontology_concept::OntologyConcept; _mediaType=nothing) -> Channel{ Any }, OpenAPI.Clients.ApiResponse

Update Concept

Update a concept by ID

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **ConceptsApi** | API context | 
**id** | **Int64**|  | [default to nothing]
**ontology_concept** | [**OntologyConcept**](OntologyConcept.md)|  | 

### Return type

**Any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

