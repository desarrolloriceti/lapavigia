import os
import httpx
from typing import Dict
import re


async def analyze_phone(phone: str) -> Dict:
    """
    Analiza un número de teléfono usando IPQS y verifica reportes comunitarios
    """
    signals = {
        "ipqs_fraud_score": None,
        "community_reports": 0,
    }

    # Limpiar el número de teléfono
    cleaned_phone = re.sub(r'\D', '', phone)

    try:
        # Consultar IPQS Phone Validation
        ipqs_api_key = os.getenv("IPQS_API_KEY")
        if ipqs_api_key:
            async with httpx.AsyncClient() as client:
                ipqs_data = {
                    "phone": cleaned_phone,
                    "strictness": 1,
                    "fast": True
                }
                ipqs_response = await client.post(
                    "https://pro.ipqualityscore.com/api/json/phone/check",
                    params={"key": ipqs_api_key},
                    json=ipqs_data,
                    timeout=10
                )

                if ipqs_response.status_code == 200:
                    ipqs_result = ipqs_response.json()
                    signals["ipqs_fraud_score"] = ipqs_result.get("fraud_score", 0)

    except Exception as e:
        print(f"Error en IPQS: {e}")

    return signals
