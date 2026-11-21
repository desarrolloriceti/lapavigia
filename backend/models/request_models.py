from pydantic import BaseModel, Field
from typing import Optional, List


class AnalyzeTextRequest(BaseModel):
    content: str = Field(..., description="Texto a analizar para detectar fraude")


class AnalyzeURLRequest(BaseModel):
    url: str = Field(..., description="URL a analizar")


class AnalyzePhoneRequest(BaseModel):
    phone: str = Field(..., description="Número de teléfono a analizar")


class AnalyzeImageRequest(BaseModel):
    image_base64: str = Field(..., description="Imagen en formato base64 a analizar")


class CommunityReportRequest(BaseModel):
    type: str = Field(..., description="Tipo de reporte: 'phone', 'url', 'text'")
    value: str = Field(..., description="Valor a reportar (teléfono, URL o texto)")
    description: str = Field(..., description="Descripción del reporte")
