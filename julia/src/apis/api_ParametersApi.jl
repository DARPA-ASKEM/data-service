# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

struct ParametersApi <: OpenAPI.APIClientImpl
    client::OpenAPI.Clients.Client
end

"""
The default API base path for APIs in `ParametersApi`.
This can be used to construct the `OpenAPI.Clients.Client` instance.
"""
basepath(::Type{ ParametersApi }) = "http://localhost"

const _returntypes_create_parameters_parameters_post_ParametersApi = Dict{Regex,Type}(
    Regex("^" * replace("200", "x"=>".") * "\$") => Any,
    Regex("^" * replace("201", "x"=>".") * "\$") => CreateFeatureDatasetsFeaturesPost201Response,
    Regex("^" * replace("422", "x"=>".") * "\$") => HTTPValidationError,
)

function _oacinternal_create_parameters_parameters_post(_api::ParametersApi, independent_parameter::Vector{IndependentParameter}; _mediaType=nothing)
    _ctx = OpenAPI.Clients.Ctx(_api.client, "POST", _returntypes_create_parameters_parameters_post_ParametersApi, "/parameters", [], independent_parameter)
    OpenAPI.Clients.set_header_accept(_ctx, ["application/json", ])
    OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? ["application/json", ] : [_mediaType])
    return _ctx
end

@doc raw"""Create Parameters

Create parameters from a list

Params:
- independent_parameter::Vector{IndependentParameter} (required)

Return: Any, OpenAPI.Clients.ApiResponse
"""
function create_parameters_parameters_post(_api::ParametersApi, independent_parameter::Vector{IndependentParameter}; _mediaType=nothing)
    _ctx = _oacinternal_create_parameters_parameters_post(_api, independent_parameter; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx)
end

function create_parameters_parameters_post(_api::ParametersApi, response_stream::Channel, independent_parameter::Vector{IndependentParameter}; _mediaType=nothing)
    _ctx = _oacinternal_create_parameters_parameters_post(_api, independent_parameter; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx, response_stream)
end

const _returntypes_get_parameters_parameters_get_ParametersApi = Dict{Regex,Type}(
    Regex("^" * replace("200", "x"=>".") * "\$") => Any,
    Regex("^" * replace("422", "x"=>".") * "\$") => HTTPValidationError,
)

function _oacinternal_get_parameters_parameters_get(_api::ParametersApi; page=nothing, page_size=nothing, _mediaType=nothing)
    _ctx = OpenAPI.Clients.Ctx(_api.client, "GET", _returntypes_get_parameters_parameters_get_ParametersApi, "/parameters", [])
    OpenAPI.Clients.set_param(_ctx.query, "page", page)  # type Int64
    OpenAPI.Clients.set_param(_ctx.query, "page_size", page_size)  # type Int64
    OpenAPI.Clients.set_header_accept(_ctx, ["application/json", ])
    OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? [] : [_mediaType])
    return _ctx
end

@doc raw"""Get Parameters

Retrieve parameters

Params:
- page::Int64
- page_size::Int64

Return: Any, OpenAPI.Clients.ApiResponse
"""
function get_parameters_parameters_get(_api::ParametersApi; page=nothing, page_size=nothing, _mediaType=nothing)
    _ctx = _oacinternal_get_parameters_parameters_get(_api; page=page, page_size=page_size, _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx)
end

function get_parameters_parameters_get(_api::ParametersApi, response_stream::Channel; page=nothing, page_size=nothing, _mediaType=nothing)
    _ctx = _oacinternal_get_parameters_parameters_get(_api; page=page, page_size=page_size, _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx, response_stream)
end

export create_parameters_parameters_post
export get_parameters_parameters_get
