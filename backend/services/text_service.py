import os
import httpx
import json
from typing import Dict


async def analyze_text(content: str) -> Dict:
    signals = {
        "ai_analysis_score": 0,
    }

    try:
        zai_api_key = os.getenv("ZAI_API_KEY")
        print(f"Key ZAI encontrada: {bool(zai_api_key)}")
        print(f"Key primeros 10 chars: {zai_api_key[:10] if zai_api_key else 'NONE'}")

        async with httpx.AsyncClient(timeout=30) as client:
            print("Llamando a Z.AI...")
            response = await client.post(
                "https://api.z.ai/api/paas/v4/chat/completions",
                headers={
                    "Authorization": f"Bearer {zai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "glm-4.7-flash",
                    "messages": [
                        {"role": "user", "content": f"Este texto es fraude? responde solo con JSON: {{\"risk_score\": 0-100}}. Texto: {content}"}
                    ]
                }
            )
            print(f"Status Z.AI: {response.status_code}")
            print(f"Respuesta Z.AI: {response.text[:300]}")

            if response.status_code == 200:
                result = response.json()
                text = result["choices"][0]["message"]["content"]
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end > start:
                    analysis_data = json.loads(text[start:end])
                    signals["ai_analysis_score"] = analysis_data.get("risk_score", 0)

    except Exception as e:
        print(f"ERROR Z.AI: {e}")
        import traceback
        traceback.print_exc()

    return signals