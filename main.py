from fastapi import FastAPI
from contextlib import asynccontextmanager
from seed import executar_seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    executar_seed()   # só irá inserir se a tabela estiver vazia
    yield



# Execute no terminal: python -m uvicorn main:app --reload
app = FastAPI(lifespan=lifespan)

from router.dashboard import dashboard_router

app.include_router(dashboard_router)


