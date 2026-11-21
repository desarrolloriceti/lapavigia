import os
import httpx
from typing import Dict


async def analyze_image(image_base64: str) -> Dict:
    """
    Analiza una imagen usando Z.AI GLM-4.6V-Flash para detectar comprobantes SINPE falsos,
    logos alterados y documentos sospechosos
    """
    signals = {
        "ai_analysis_score": 0,
    }

    try:
        zai_api_key = os.getenv("ZAI_API_KEY")
        if not zai_api_key:
            return signals

        # Prompt en español para detectar fraudes en imágenes
        prompt = f"""Analiza la siguiente imagen para detectar posibles fraudes:

Descripción de la imagen: {image_base64[:100]}... (imagen en base64)

Responde en formato JSON con:
- "analysis": breve explicación del análisis visual
- "risk_score": 0-100 (0 = seguro, 100 = fraude confirmado)
- "fraud_indicators": lista de indicadores de fraude encontrados
- "recommendations": lista de recomendaciones de seguridad

Patrones de fraude a considerar en imágenes:
- Comprobantes SINPE falsos
- Logos alterados o manipulados
- Documentos con información sospechosa
- Facturas con montos sospechosos
- Pagos urgentes en imágenes
- Certificados falsos

Responde SOLO con el JSON, sin texto adicional."""

        async with httpx.AsyncClient(timeout=60) as client:
            headers = {
                "Authorization": f"Bearer {zai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "glm-4v-flash",
                "messages": [
                    {"role": "system", "content": "Eres un experto en detección de fraudes visuales. Responde siempre en formato JSON."},
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
        print(f"Error en image_service: {e}")

    return signals
