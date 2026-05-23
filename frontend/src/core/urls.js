export const baseUrl = '/api'

export const endpoints = {
    VALIDATE_GEOJSON_TEXT: `${baseUrl}/validate/text`,
    VALIDATE_GEOJSON_FILE: `${baseUrl}/validate/file`,
    GET_GEOJSON_CONFIG_SCHEMA: `${baseUrl}/config-schema/geojson`,
    GET_GEOMETRY_CONFIG_SCHEMA: `${baseUrl}/config-schema/geometry`,
}
