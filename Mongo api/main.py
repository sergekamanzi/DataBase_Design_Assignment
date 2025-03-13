from fastapi import FastAPI
from routes import router

app = FastAPI(title="Bank API with MongoDB")

app.include_router(router)
