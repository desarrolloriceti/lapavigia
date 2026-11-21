import chromadb
from chromadb.config import Settings
from typing import Dict, List
import json
import os


# Configurar ChromaDB
client = chromadb.PersistentClient(path="./data/chroma_db")
rag_collection = client.get_or_create_collection(name="cr_fraud_patterns")


def load_patterns():
    """
    Carga los patrones de fraude de Costa Rica desde cr_patterns.json
    """
    patterns_file = os.path.join(os.path.dirname(__file__), "../../data/cr_patterns.json")

    if os.path.exists(patterns_file):
        try:
            with open(patterns_file, "r", encoding="utf-8") as f:
                patterns = json.load(f)

            # Insertar en ChromaDB
            if patterns:
                rag_collection.delete()  # Limpiar colección existente

                for pattern in patterns:
                    rag_collection.add(
                        documents=[pattern["description"]],
                        metadatas=[{
                            "id": pattern["id"],
                            "type": pattern["type"],
                            "risk_level": pattern["risk_level"],
                            "keywords": ",".join(pattern["keywords"])
                        }],
                        ids=[f"pattern_{pattern['id']}"]
                    )

                print(f"Cargados {len(patterns)} patrones de fraude costarricense en ChromaDB")
        except Exception as e:
            print(f"Error cargando patrones: {e}")


def query_patterns(content: str) -> Dict:
    """
    Consulta patrones de fraude relevantes en el contenido
    """
    results = rag_collection.query(
        query_texts=[content],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    if results["documents"] and results["documents"][0]:
        # Si hay coincidencias, retornar True con detalles
        matches = []
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]
            matches.append({
                "description": doc,
                "type": metadata["type"],
                "risk_level": metadata["risk_level"],
                "keywords": metadata["keywords"]
            })

        return {
            "match": True,
            "matches": matches
        }
    else:
        return {
            "match": False,
            "matches": []
        }
