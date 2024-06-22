from typing import List
from fastapi import APIRouter, Request, HTTPException, Query
from app.core.logger import LoggerConfig
from app.models.pydantic.dashboard_model import LineChartRequest, LineChartResponse, CardValuesResponse
from app.services.dashboard_service import DashboardService

logger = LoggerConfig(__name__).get_logger()
dashboard_service = DashboardService()

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get('/card_values', response_model=List[CardValuesResponse])
async def get_card_list(
    request: Request,
):
    try:
        logger.info(f"{request.url.path} Get card values")
        return await dashboard_service.get_card_values()
    except HTTPException as e:
        logger.error(f"An error occured at {request.url.path} {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"An error occured at {request.url.path} {str(e)}")
        raise HTTPException(detail=str(e), status_code=500)

@router.get('/line_chart_values', response_model=List[LineChartResponse])
async def get_line_chart_values(
    request: Request,
    filter_type: LineChartRequest = Query(..., description="Filter type")
):
    try:
        logger.info(f"{request.url.path} Get line chart values")
        return await dashboard_service.get_line_chart_values(filter_type.value)
    except HTTPException as e:
        logger.error(f"An error occured at {request.url.path} {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"An error occured at {request.url.path} {str(e)}")
        raise HTTPException(detail=str(e), status_code=500)
