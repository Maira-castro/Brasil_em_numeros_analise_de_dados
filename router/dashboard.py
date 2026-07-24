from fastapi import APIRouter, Depends
from dependencies import get_dashboard

dashboard_router = APIRouter()

@dashboard_router.get("/dashboard")
def dashboard(
    dados = Depends(get_dashboard)
):
    return dados
