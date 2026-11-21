from typing import Dict, List
from models.response_models import ScoreResult


def calculate_score(signals: Dict) -> ScoreResult:
    """
    Calcula el puntaje de riesgo combinando múltiples señales
    Ponderación:
    - ai_analysis_score: 35%
    - abuse_score: 25%
    - ipqs_fraud_score: 20%
    - urlscan_malicious: 10%
    - rag_match: 5%
    - community_reports: 5%

    Niveles:
    - 0-30: Seguro (verde)
    - 31-60: Sospechoso (amarillo)
    - 61-80: Probable estafa (naranja)
    - 81-100: Estafa confirmada (rojo)
    """
    # Obtener valores de señales
    ai_score = signals.get("ai_analysis_score", 0)
    abuse_score = signals.get("abuse_score", 0)
    ipqs_score = signals.get("ipqs_fraud_score", 0)
    urlscan_malicious = signals.get("urlscan_malicious", False)
    rag_match = signals.get("rag_match", False)
    community_reports = signals.get("community_reports", 0)

    # Convertir booleanos a puntajes
    urlscan_score = 100 if urlscan_malicious else 0

    # Calcular puntaje ponderado
    weighted_score = (
        (ai_score * 0.35) +
        (abuse_score * 0.25) +
        (ipqs_score * 0.20) +
        (urlscan_score * 0.10) +
        (100 if rag_match else 0) * 0.05 +
        min(community_reports, 10) * 10 * 0.05
    )

    # Redondear a entero
    final_score = round(weighted_score)

    # Determinar nivel y color
    if final_score <= 30:
        level = "Seguro"
        color = "#10B981"  # Verde
        explanation = "El análisis indica que el contenido es seguro. No se detectaron patrones de fraude sospechosos."
    elif final_score <= 60:
        level = "Sospechoso"
        color = "#F59E0B"  # Amarillo
        explanation = "El análisis indica posibles señales de fraude. Se recomienda verificar cuidadosamente antes de interactuar."
    elif final_score <= 80:
        level = "Probable estafa"
        color = "#F97316"  # Naranja
        explanation = "El análisis indica alto riesgo de fraude. Se recomienda extremar precauciones y no realizar transacciones."
    else:
        level = "Estafa confirmada"
        color = "#EF4444"  # Rojo
        explanation = "El análisis indica fraude confirmado. No interactúes con este contenido."

    # Generar recomendaciones
    recommendations = generate_recommendations(
        final_score, ai_score, abuse_score, ipqs_score,
        urlscan_malicious, rag_match, community_reports
    )

    # Generar fuentes consultadas
    sources = generate_sources(
        ai_score, abuse_score, ipqs_score, urlscan_malicious, rag_match, community_reports
    )

    return ScoreResult(
        score=final_score,
        level=level,
        color=color,
        explanation=explanation,
        recommendations=recommendations,
        sources=sources
    )


def generate_recommendations(
    score: int,
    ai_score: int,
    abuse_score: int,
    ipqs_score: int,
    urlscan_malicious: bool,
    rag_match: bool,
    community_reports: int
) -> List[str]:
    """Genera recomendaciones basadas en el puntaje"""
    recommendations = []

    if score <= 30:
        recommendations.append("El contenido parece seguro. Sin embargo, siempre verifica la información de fuentes oficiales.")
    elif score <= 60:
        recommendations.append("Verifica el remitente y el origen de la información antes de actuar.")
        recommendations.append("No compartas información personal o financiera sin confirmar.")
    elif score <= 80:
        recommendations.append("¡ALERTA: Alto riesgo de fraude detectado!")
        recommendations.append("No realices transacciones o compartas información personal.")
        recommendations.append("Verifica la identidad de las instituciones involucradas.")
        recommendations.append("Contacta a las instituciones oficiales directamente para confirmar.")
    else:
        recommendations.append("¡PELIGRO: Fraude confirmado!")
        recommendations.append("NO interactúes con este contenido.")
        recommendations.append("Reporta este caso a las autoridades.")
        recommendations.append("No compartas información personal ni realices pagos.")

    if community_reports > 0:
        recommendations.append(f"Este valor ha sido reportado {community_reports} veces por otros usuarios.")

    if rag_match:
        recommendations.append("Este patrón coincide con uno conocido de fraude en Costa Rica.")

    if urlscan_malicious:
        recommendations.append("Este dominio ha sido marcado como sospechoso en URLScan.io.")

    if abuse_score and abuse_score > 70:
        recommendations.append("Esta dirección IP tiene historial de actividad maliciosa.")

    if ipqs_score and ipqs_score > 70:
        recommendations.append("Este número de teléfono tiene alto riesgo de fraude según IPQualityScore.")

    return recommendations


def generate_sources(
    ai_score: int,
    abuse_score: int,
    ipqs_score: int,
    urlscan_malicious: bool,
    rag_match: bool,
    community_reports: int
) -> List[str]:
    """Genera lista de fuentes consultadas"""
    sources = []

    if ai_score > 0:
        sources.append("Análisis de IA - GLM-4.7-Flash")

    if abuse_score is not None:
        sources.append("AbuseIPDB")

    if ipqs_score is not None:
        sources.append("IPQualityScore")

    if urlscan_malicious:
        sources.append("URLScan.io")

    if rag_match:
        sources.append("Base de patrones CR - RAG")

    if community_reports > 0:
        sources.append("Reportes comunitarios")

    return sources
