from fastapi import APIRouter, HTTPException
from models.request_models import (
    AnalyzeTextRequest,
    AnalyzeURLRequest,
    AnalyzePhoneRequest,
    AnalyzeImageRequest
)
from models.response_models import ScoreResult
from services.url_service import analyze_url
from services.phone_service import analyze_phone
from services.text_service import analyze_text
from services.image_service import analyze_image
from services.score_calculator import calculate_score
from services.rag_service import query_patterns
import asyncio

router = APIRouter()


@router.post("/text", response_model=ScoreResult)
async def analyze_text_endpoint(request: AnalyzeTextRequest):
    """
    Analiza texto para detectar patrones de fraude costarricense
    """
    try:
        # Analizar con IA
        text_signals = await analyze_text(request.content)

        # Consultar patrones RAG
        rag_result = query_patterns(request.content)
        rag_match = rag_result["match"]

        # Combinar señales
        signals = {
            "ai_analysis_score": text_signals.get("ai_analysis_score", 0),
            "rag_match": rag_match
        }

        # Calcular puntaje
        result = calculate_score(signals)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar texto: {str(e)}")


@router.post("/url", response_model=ScoreResult)
async def analyze_url_endpoint(request: AnalyzeURLRequest):
    """
    Analiza una URL para detectar posibles fraudes
    """
    try:
        # Analizar URL
        url_signals = await analyze_url(request.url)

        # Consultar patrones RAG
        rag_result = query_patterns(request.url)
        rag_match = rag_result["match"]

        # Combinar señales
        signals = {
            "abuse_score": url_signals.get("abuse_score"),
            "urlscan_malicious": url_signals.get("urlscan_malicious"),
            "rag_match": rag_match
        }

        # Calcular puntaje
        result = calculate_score(signals)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar URL: {str(e)}")


@router.post("/phone", response_model=ScoreResult)
async def analyze_phone_endpoint(request: AnalyzePhoneRequest):
    """
    Analiza un número de teléfono para detectar fraude
    """
    try:
        # Analizar teléfono
        phone_signals = await analyze_phone(request.phone)

        # Consultar patrones RAG
        rag_result = query_patterns(request.phone)
        rag_match = rag_result["match"]

        # Combinar señales
        signals = {
            "ipqs_fraud_score": phone_signals.get("ipqs_fraud_score"),
            "rag_match": rag_match
        }

        # Calcular puntaje
        result = calculate_score(signals)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar teléfono: {str(e)}")


@router.post("/image", response_model=ScoreResult)
async def analyze_image_endpoint(request: AnalyzeImageRequest):
    """
    Analiza una imagen para detectar comprobantes falsos y fraudes visuales
    """
    try:
        # Analizar imagen
        image_signals = await analyze_image(request.image_base64)

        # Consultar patrones RAG
        rag_result = query_patterns(request.image_base64[:100])
        rag_match = rag_result["match"]

        # Combinar señales
        signals = {
            "ai_analysis_score": image_signals.get("ai_analysis_score", 0),
            "rag_match": rag_match
        }

        # Calcular puntaje
        result = calculate_score(signals)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar imagen: {str(e)}")
