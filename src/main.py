from fastapi import FastAPI
from routes import experiment, auth, tag
from controller import DBConnection

database = DBConnection()

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
    on_startup=[database.connect],
    on_shutdown=[database.close],
)

app.include_router(router=auth.router, tags=["auth"])
app.include_router(router=experiment.router, tags=["experiments"])
app.include_router(router=tag.router, tags=["tags"])
