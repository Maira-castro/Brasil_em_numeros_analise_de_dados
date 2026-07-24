from fastapi import FastAPI

# Execute no terminal: python -m uvicorn main:app --reload
app = FastAPI()

from router.dashboard import dashboard_router

app.include_router(dashboard_router)