from pydantic import BaseModel, Field
from typing import List


class ScoreResult(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Puntuación de riesgo 0-100")
    level: str = Field(..., description="Nivel de riesgo: seguro, sospechoso, probable estafa, estafa confirmada")
    color: str = Field(..., description="Color representativo del nivel de riesgo")
    explanation: str = Field(..., description="Explicación detallada del análisis")
    recommendations: List[str] = Field(default_factory=list, description="Recomendaciones de seguridad")
    sources: List[str] = Field(default_factory=list, description="Fuentes consultadas para el análisis")


class CommunityReport(BaseModel):
    id: str = Field(..., description="ID único del reporte")
    type: str = Field(..., description="Tipo de reporte: 'phone', 'url', 'text'")
    value: str = Field(..., description="Valor reportado")
    description: str = Field(..., description="Descripción del reporte")
    timestamp: str = Field(..., description="Fecha y hora del reporte")
    count: int = Field(..., description="Número de reportes previos para este valor")
