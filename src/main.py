from fastapi import FastAPI

from routes import experiment

app = FastAPI(
    title="Lab Experiment CRM",
    description="",
    version="1.0",
    contact={
        "name": "don't",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(experiment.router)
