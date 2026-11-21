from fastapi import APIRouter, HTTPException
from models.request_models import CommunityReportRequest
from models.response_models import CommunityReport
from services.community_service import save_report, check_reports, get_reports_by_type
from typing import List

router = APIRouter()


@router.post("/report", response_model=CommunityReport)
async def submit_community_report(request: CommunityReportRequest):
    """
    Recibe y guarda un reporte comunitario
    """
    try:
        # Verificar que el tipo sea válido
        valid_types = ["phone", "url", "text"]
        if request.type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de reporte inválido. Debe ser uno de: {', '.join(valid_types)}"
            )

        # Guardar reporte
        report = save_report(request)

        # Obtener cantidad de reportes previos
        report_count = check_reports(request.value)

        # Actualizar el reporte con la cantidad
        report.count = report_count

        return report

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar reporte: {str(e)}")


@router.get("/check/{value}")
async def check_report(value: str):
    """
    Consulta si un valor tiene reportes previos
    """
    try:
        count = check_reports(value)
        return {
            "value": value,
            "has_reports": count > 0,
            "report_count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar reportes: {str(e)}")


@router.get("/reports/{report_type}")
async def get_reports_by_type_endpoint(report_type: str, limit: int = 50):
    """
    Obtiene todos los reportes de un tipo específico
    """
    try:
        valid_types = ["phone", "url", "text"]
        if report_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de reporte inválido. Debe ser uno de: {', '.join(valid_types)}"
            )

        reports = get_reports_by_type(report_type)

        # Limitar resultados
        reports = reports[:limit]

        return reports

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener reportes: {str(e)}")
