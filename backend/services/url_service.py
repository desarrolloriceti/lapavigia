import os
import httpx
from typing import Dict


async def analyze_url(url: str) -> Dict:
    """
    Analiza una URL usando AbuseIPDB y URLScan.io
    """
    signals = {
        "abuse_score": None,
        "urlscan_malicious": None,
        "ipqs_fraud_score": None,
    }

    try:
        # Obtener la IP del dominio
        async with httpx.AsyncClient() as client:
            # Intentar resolver la IP del dominio
            try:
                response = await client.get(f"https://api.ipify.org?format=json", timeout=5)
                ip_address = response.json()["ip"]

                # Consultar AbuseIPDB
                abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")
                if abuseipdb_api_key:
                    abuse_response = await client.get(
                        f"https://api.abuseipdb.com/api/v2/check",
                        params={"ipAddress": ip_address, "maxAgeInDays": 90},
                        headers={"Key": abuseipdb_api_key, "Accept": "application/json"},
                        timeout=10
                    )
                    if abuse_response.status_code == 200:
                        abuse_data = abuse_response.json()
                        signals["abuse_score"] = abuse_data["data"]["abuseConfidenceScore"]

                # Consultar URLScan.io
                urlscan_api_key = os.getenv("URLSCAN_API_KEY")
                if urlscan_api_key:
                    scan_data = {
                        "url": url,
                        "visibility": "public",
                        "start": True
                    }
                    scan_response = await client.post(
                        "https://urlscan.io/api/v1/scan/",
                        json=scan_data,
                        headers={"API-Key": urlscan_api_key},
                        timeout=15
                    )

                    if scan_response.status_code == 201:
                        scan_result = scan_response.json()
                        scan_id = scan_result["uuid"]

                        # Esperar a que el escaneo termine
                        import asyncio
                        for _ in range(30):  # Máximo 30 intentos de 5 segundos
                            await asyncio.sleep(5)
                            result_response = await client.get(
                                f"https://urlscan.io/api/v1/result/{scan_id}",
                                headers={"API-Key": urlscan_api_key},
                                timeout=10
                            )
                            if result_response.status_code == 200:
                                result_data = result_response.json()
                                if result_data.get("verdicts", {}).get("malicious"):
                                    signals["urlscan_malicious"] = True
                                break
            except Exception as e:
                print(f"Error analizando URL: {e}")

    except Exception as e:
        print(f"Error en url_service: {e}")

    return signals
