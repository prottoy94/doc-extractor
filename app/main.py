from fastapi import FastAPI

from app import config

app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION,
)

@app.get("/")
def home():
    return {
        "message": "Document Field Extractor is running.",
        "documentation": "Open /docs to see and test every route.",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/info")
def app_info():
    return {
        "app_name": config.APP_NAME,
        "version": config.APP_VERSION,
        "allowed_image_types": config.ALLOWED_CONTENT_TYPES,
        "max_upload_megabytes": config.MAX_UPLOAD_MEGABYTES,
        "form_fields": config.FORM_FIELD_NAMES,
    }
