import chromadb
from chromadb.config import Settings
from models.request_models import CommunityReportRequest
from models.response_models import CommunityReport
from typing import List
import os
import uuid
from datetime import datetime


# Configurar ChromaDB
client = chromadb.PersistentClient(path="./data/chroma_db")
community_collection = client.get_or_create_collection(name="community_reports")


def save_report(report: CommunityReportRequest) -> CommunityReport:
    """
    Guarda un reporte comunitario en ChromaDB
    """
    report_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    community_collection.add(
        documents=[report.description],
        metadatas=[{
            "id": report_id,
            "type": report.type,
            "value": report.value,
            "timestamp": timestamp
        }],
        ids=[report_id]
    )

    return CommunityReport(
        id=report_id,
        type=report.type,
        value=report.value,
        description=report.description,
        timestamp=timestamp,
        count=0  # Se actualizará con check_reports
    )


def check_reports(value: str) -> int:
    """
    Consulta la cantidad de reportes previos para un valor específico
    """
    results = community_collection.query(
        query_texts=[value],
        n_results=10,
        include=["metadatas"]
    )

    if results["metadatas"] and results["metadatas"][0]:
        return len(results["metadatas"][0])
    return 0


def get_reports_by_type(report_type: str) -> List[CommunityReport]:
    """
    Obtiene todos los reportes de un tipo específico
    """
    results = community_collection.get(
        where={"type": report_type},
        limit=100
    )

    reports = []
    for i, metadata in enumerate(results["metadatas"]):
        reports.append(CommunityReport(
            id=metadata["id"],
            type=metadata["type"],
            value=metadata["value"],
            description=results["documents"][i],
            timestamp=metadata["timestamp"],
            count=0  # Se actualizaría con una consulta adicional
        ))

    return reports
