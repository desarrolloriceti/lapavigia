# Arquitectura de Lapa vigIA

## Descripción General

Lapa vigIA es una plataforma antifraude PWA (Progressive Web App) diseñada específicamente para detectar y prevenir fraudes en Costa Rica. La plataforma combina análisis de inteligencia artificial, consultas a APIs externas, y una base de conocimiento local con patrones conocidos de fraude.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend PWA                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Texto   │  │   URL    │  │ Teléfono │  │ Imagen   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       └─────────────┼─────────────┴─────────────┘         │
│                     │                                     │
│              ┌──────▼──────┐                             │
│              │   app.js    │                             │
│              └──────┬──────┘                             │
└─────────────────────┼─────────────────────────────────────┘
                      │ HTTP/REST
                      │
┌─────────────────────▼─────────────────────────────────────┐
│                     Backend FastAPI                         │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Main Application (main.py)             │   │
│  └────────────────────────────────────────────────────┘   │
│                           │                                 │
│           ┌───────────────┼───────────────┐                 │
│           │               │               │                 │
│    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐         │
│    │  Health     │ │   Analyze   │ │ Community   │         │
│    │   Router    │ │   Router    │ │   Router    │         │
│    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘         │
│           │               │               │                 │
│    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐         │
│    │  Services   │ │  Services   │ │  Services   │         │
│    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘         │
│           │               │               │                 │
│    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐         │
│    │  Score      │ │  RAG        │ │ Community   │         │
│    │ Calculator  │ │ Service     │ │ Service     │         │
│    └─────────────┘ └─────────────┘ └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                      │
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼────┐       ┌───▼────┐       ┌───▼────┐
│ APIs   │       │ ChromaDB│       │ APIs   │
│Externas│       │  Local  │       │Externas│
└────────┘       └─────────┘       └────────┘
```

## Stack Tecnológico

### Backend

#### FastAPI
**Justificación:**
- Velocidad y rendimiento excepcional
- Validación automática de datos con Pydantic
- Documentación automática de APIs (Swagger/OpenAPI)
- Soporte nativo para async/await
- Ideal para APIs RESTful modernas

#### Uvicorn
**Justificación:**
- Servidor ASGI rápido para aplicaciones FastAPI
- Soporte para recarga automática en desarrollo
- Configuración flexible de workers
- Soporte para HTTPS y WebSocket

#### ChromaDB
**Justificación:**
- Base de datos vectorial open-source
- Rendimiento superior para búsqueda semántica
- Almacenamiento local persistente
- Integración fácil con Python
- Sin necesidad de servidores externos

#### HTTPX
**Justificación:**
- Cliente HTTP asíncrono moderno
- Soporte para HTTP/1.1 y HTTP/2
- Perfecto para llamadas asíncronas a APIs externas

### Frontend

#### Vanilla JavaScript
**Justificación:**
- Sin dependencias externas
- Carga rápida
- Fácil integración con PWA
- Compatible con todos los navegadores modernos

#### CSS Moderno
**Justificación:**
- Sin frameworks (Bootstrap, Tailwind, etc.)
- Diseño responsive y mobile-first
- Rendimiento optimizado
- Código mantenible y escalable

#### PWA Features
**Justificación:**
- Funciona offline
- Instalable en dispositivos móviles
- Experiencia nativa
- Mejor retención de usuarios

### Servicios de IA

#### Z.AI GLM-4.7-Flash
**Justificación:**
- Modelos de lenguaje especializados en análisis de texto
- Análisis rápido y preciso
- Soporte para visión por computadora (GLM-4V)
- Precios competitivos
- API fácil de integrar

## Flujo de Análisis Paso a Paso

### 1. Inicialización del Sistema
```
1. Backend inicia FastAPI
2. Carga patrones de fraude de cr_patterns.json
3. Crea colección ChromaDB para patrones y reportes
4. Espera peticiones de análisis
```

### 2. Análisis de Texto
```
1. Usuario ingresa texto en el frontend
2. Frontend envía POST /api/analyze/text
3. Backend recibe AnalyzeTextRequest
4. Servicio text_service llama a Z.AI GLM-4.7-Flash
5. Servicio rag_service consulta patrones de fraude
6. Score_calculator combina todos los signals
7. Retorna ScoreResult con nivel, color y recomendaciones
8. Frontend muestra resultados al usuario
```

### 3. Análisis de URL
```
1. Usuario ingresa URL en el frontend
2. Backend envía solicitud a AbuseIPDB
3. Backend escanea URL con URLScan.io
4. Servicio rag_service consulta patrones
5. Score_calculator pondera resultados
6. Retorna ScoreResult
```

### 4. Análisis de Teléfono
```
1. Usuario ingresa número de teléfono
2. Backend consulta IPQualityScore
3. Servicio rag_service verifica patrones
4. Score_calculator calcula riesgo
5. Retorna ScoreResult
```

### 5. Análisis de Imagen
```
1. Usuario sube imagen
2. Frontend convierte a base64
3. Backend envía a Z.AI GLM-4.6V-Flash
4. Servicio rag_service verifica patrones visuales
5. Score_calculator calcula riesgo
6. Retorna ScoreResult
```

### 6. Reporte Comunitario
```
1. Usuario reporta fraude
2. Backend guarda en ChromaDB
3. Verifica reportes previos
4. Retorna ID y contador de reportes
5. Sistema aprende de la comunidad
```

## Modelo de Datos

### Backend Models

#### AnalyzeTextRequest
```python
{
    "content": str  # Texto a analizar
}
```

#### AnalyzeURLRequest
```python
{
    "url": str  # URL a analizar
}
```

#### AnalyzePhoneRequest
```python
{
    "phone": str  # Número de teléfono
}
```

#### AnalyzeImageRequest
```python
{
    "image_base64": str  # Imagen en base64
}
```

#### ScoreResult
```python
{
    "score": int,           # 0-100
    "level": str,           # "Seguro", "Sospechoso", "Probable estafa", "Estafa confirmada"
    "color": str,           # Color hex
    "explanation": str,     # Explicación detallada
    "recommendations": [],  # Lista de recomendaciones
    "sources": []           # Fuentes consultadas
}
```

#### CommunityReport
```python
{
    "id": str,              # UUID
    "type": str,            # "phone", "url", "text"
    "value": str,           # Valor reportado
    "description": str,     # Descripción
    "timestamp": str,       # ISO format
    "count": int            # Reportes previos
}
```

### Frontend Data

#### Patrones de Fraude (cr_patterns.json)
```json
{
    "id": int,
    "type": str,
    "description": str,
    "keywords": [],
    "risk_level": str
}
```

#### Instituciones (institutions.json)
```json
{
    "name": str,
    "official_domain": str,
    "official_phone": str,
    "official_whatsapp": str,
    "website": str
}
```

## Decisions de Diseño

### 1. Arquitectura Monolítica
**Decision:** Backend como monolito con routers separados
**Razón:** Simplicidad de despliegue, fácil mantenimiento, código compartido

### 2. ChromaDB Local
**Decision:** Base de datos vectorial local en lugar de servicio externo
**Razón:** Privacidad de datos, sin dependencia de servicios externos, costos reducidos

### 3. PWA sobre React
**Decision:** Vanilla JavaScript en lugar de frameworks como React
**Razón:** Menor complejidad, mejor rendimiento, menor tamaño de bundle

### 4. API RESTful
**Decision:** REST sobre GraphQL
**Razón:** Simplicidad, mejor cacheability, estándar ampliamente usado

### 5. Ponderación de Scores
**Decision:** Sistema ponderado con diferentes pesos para cada fuente
**Razón:** Más robusto que promedio simple, prioriza fuentes más confiables

### 6. Análisis Asíncrono
**Decision:** Uso de async/await para todas las operaciones
**Razón:** Mejor rendimiento, mejor experiencia de usuario

## Seguridad

### Medidas Implementadas
- CORS configurado para permitir cualquier origen en desarrollo
- Validación de datos con Pydantic
- Sanitización de entradas
- Sin almacenamiento de contraseñas
- APIs externas protegidas con claves de entorno

### Recomendaciones Futuras
- Implementar autenticación JWT
- HTTPS en producción
- Rate limiting en APIs
- Logs de auditoría
- Sanitización de salida HTML

## Escalabilidad

### Horizonte Actual
- Hasta 1000 análisis por día
- Hasta 10 reportes comunitarios por día
- Hasta 50 usuarios concurrentes

### Estrategias de Escalado
- Horizontal scaling con múltiples workers
- Caching de resultados frecuentes
- Base de datos vectorial escalable (ChromaDB soporta clustering)
- CDN para frontend

## Próximos Pasos

1. **Implementar autenticación y usuarios**
2. **Añadir más APIs de análisis**
3. **Crear dashboard de administración**
4. **Implementar alertas en tiempo real**
5. **Añadir soporte para más idiomas**
6. **Optimizar ChromaDB para mayor rendimiento**
7. **Implementar tests automatizados**
8. **Deploy en producción con HTTPS**
