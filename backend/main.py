from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health, analyze, community
from services.rag_service import load_patterns
import uvicorn

# Crear instancia de FastAPI
app = FastAPI(
    title="Lapa vigIA",
    description="Plataforma antifraude PWA para Costa Rica",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar y montar routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(community.router, prefix="/api/community", tags=["Community"])

# Inicializar RAG al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    """Cargar patrones de fraude al iniciar la aplicación"""
    load_patterns()
    print("Sistema Lapa vigIA iniciado correctamente")


@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "name": "Lapa vigIA",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "analyze_text": "/api/analyze/text",
            "analyze_url": "/api/analyze/url",
            "analyze_phone": "/api/analyze/phone",
            "analyze_image": "/api/analyze/image",
            "submit_report": "/api/community/report",
            "check_report": "/api/community/check/{value}",
            "get_reports": "/api/community/reports/{type}"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
