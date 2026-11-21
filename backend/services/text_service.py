import os
import httpx
from typing import Dict


async def analyze_text(content: str) -> Dict:
    """
    Analiza texto usando Z.AI GLM-4.7-Flash para detectar patrones de fraude costarricense
    """
    signals = {
        "ai_analysis_score": 0,
    }

    try:
        zai_api_key = os.getenv("ZAI_API_KEY")
        if not zai_api_key:
            return signals

        # Prompt en español para detectar patrones de fraude en Costa Rica
        prompt = f"""Analiza el siguiente texto para detectar posibles patrones de fraude costarricense:

Texto: {content}

Responde en formato JSON con:
- "analysis": breve explicación del análisis
- "risk_score": 0-100 (0 = seguro, 100 = estafa confirmada)
- "fraud_indicators": lista de indicadores de fraude encontrados
- "recommendations": lista de recomendaciones de seguridad

Patrones de fraude costarricense a considerar:
- Suplantación de BAC, BCR, BN, Coopeande
- Mensajes de SINPE falsos
- Premios falsos del ICE
- Estafas de marketplace
- Phishing de CCSS
- Pedidos de pagos urgentes a cuentas bancarias
- Números de teléfono sospechosos en Costa Rica (506)

Responde SOLO con el JSON, sin texto adicional."""

        async with httpx.AsyncClient(timeout=30) as client:
            headers = {
                "Authorization": f"Bearer {zai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "glm-4-flash",
                "messages": [
                    {"role": "system", "content": "Eres un experto en detección de fraude en Costa Rica. Responde siempre en formato JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }

            response = await client.post(
                "https://api.z.ai/api/paas/v4/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Intentar extraer el JSON
                import json
                try:
                    # Buscar el primer { y el último }
                    start = content.find("{")
                    end = content.rfind("}") + 1
                    if start != -1 and end > start:
                        analysis_data = json.loads(content[start:end])
                        signals["ai_analysis_score"] = analysis_data.get("risk_score", 0)
                except json.JSONDecodeError:
                    print("Error al parsear respuesta JSON del modelo")

    except Exception as e:
        print(f"Error en text_service: {e}")

    return signals
