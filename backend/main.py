from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from configuration.geojson.validation import GeoJSONValidationConfig
from configuration.geometry import GeometryConfig
from core.parser import ParserHandler
from models.io import InputGeoJSONBody
from orchestrator import Orchestrator
from registry import PipelineRegistry
from settings import Settings
from utils.workflow import generate_frontend_schema

settings = Settings()

app = FastAPI()

if settings.node_env == "development":
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/api/validate/file")
async def upload_file(file: UploadFile):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file is uploaded.")

    if not file.filename.lower().endswith((".json", ".geojson")):
        raise HTTPException(
            status_code=400, detail="Only json or geojson files are allowed."
        )

    content = await file.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as err:
        raise HTTPException(status_code=400, detail="File must be UTF-8 text.") from err

    return {"raw_geojson": text}


@app.post("/api/validate/text")
async def validate_text(input_body: InputGeoJSONBody):
    orch = Orchestrator(
        pipeline_registry=PipelineRegistry(),
        parser=ParserHandler(),
        config=input_body.config,
    )
    res = orch.execute(data=input_body.geojson, operation="validation")
    return res


@app.get("/api/config-schema/geojson")
async def get_geojson_config_schema():
    geojson_validation_config = GeoJSONValidationConfig()
    return generate_frontend_schema(geojson_validation_config, exclude=["geometry"])


@app.get("/api/config-schema/geometry")
async def get_geometry_config_schema():
    return generate_frontend_schema(GeometryConfig)


if settings.node_env != "development":
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
