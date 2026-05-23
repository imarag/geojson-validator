from pydantic import BaseModel


class InputGeoJSONBody(BaseModel):
    config: dict
    geojson: str
