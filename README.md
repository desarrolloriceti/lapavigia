# 🛡️ Lapa vigIA

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PWA](https://img.shields.io/badge/PWA-Progressive-8A2BE2.svg)](https://web.dev/progressive-web-apps/)

> Plataforma antifraude PWA (Progressive Web App) para Costa Rica. Detecta y previene fraudes en tiempo real mediante análisis de inteligencia artificial, APIs de seguridad y una base de conocimiento local con patrones conocidos.

![Lapa vigIA Banner](https://via.placeholder.com/800x400/1B4332/FFFFFF?text=Lapa+vigIA+-+Plataforma+Antifraude+Costa+Rica)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Arquitectura](#-arquitectura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Endpoints API](#-endpoints-api)
- [Configuración](#-configuración)
- [Despliegue](#-despliegue)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelo de Negocio](#-modelo-de-negocio)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

## ✨ Características

### 🎯 Análisis de Fraude
- **Texto**: Detección de patrones de fraude en mensajes y textos
- **URL**: Análisis de dominios sospechosos y malware
- **Teléfono**: Validación de números de teléfono fraudulentos
- **Imagen**: Detección de comprobantes falsos y logos alterados

### 🤖 Inteligencia Artificial
- Análisis con **Z.AI GLM-4.7-Flash** para texto
- Análisis con **Z.AI GLM-4.6V-Flash** para imágenes
- RAG (Retrieval-Augmented Generation) con patrones costarricenses

### 🌐 APIs de Seguridad
- **AbuseIPDB**: Base de datos de IPs maliciosas
- **URLScan.io**: Escaneo de URLs y malware
- **IPQualityScore**: Validación de teléfonos y fraude

### 👥 Comunidad
- Sistema de reportes comunitarios
- Base de conocimiento compartida
- Aprendizaje colaborativo

### 📱 PWA
- Funciona offline
- Instalable en dispositivos móviles
- Experiencia nativa
- Responsive design

## 🖼️ Capturas de Pantalla

![Lapa vigIA Interface](https://via.placeholder.com/800x600/1B4332/FFFFFF?text=Captura+de+Pantalla+Lapa+vigIA)

## 🏗️ Arquitectura

Lapa vigIA utiliza una arquitectura monolítica moderna con separación de responsabilidades:

- **Backend**: FastAPI con routers separados (health, analyze, community)
- **Base de Datos**: ChromaDB para búsqueda vectorial y almacenamiento de reportes
- **Frontend**: PWA con Vanilla JavaScript y CSS moderno
- **IA**: Z.AI GLM-4.7-Flash y GLM-4.6V-Flash para análisis inteligente

Ver [documentación de arquitectura](docs/architecture.md) para más detalles.

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI
- **ChromaDB**: Base de datos vectorial
- **HTTPX**: Cliente HTTP asíncrono
- **Pydantic**: Validación de datos
- **Z.AI GLM-4.7-Flash**: Análisis de texto

### Frontend
- **Vanilla JavaScript**: Sin frameworks
- **CSS Moderno**: Responsive y mobile-first
- **PWA**: Progressive Web App

### APIs Externas
- **AbuseIPDB**: Detección de IPs maliciosas
- **URLScan.io**: Escaneo de URLs
- **IPQualityScore**: Validación de fraude
- **Z.AI**: Análisis con IA

## 📥 Instalación

### Requisitos Previos
- Python 3.9+
- pip
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/lapa-vigia.git
cd lapa-vigia
```

### Paso 2: Crear Entorno Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y añade tus API keys:

```env
ABUSEIPDB_API_KEY=tu_clave_abuseipdb
URLSCAN_API_KEY=tu_clave_urlscan
IPQS_API_KEY=tu_clave_ipqs
ZAI_API_KEY=tu_clave_zai
```

### Paso 5: Iniciar el Backend

```bash
python main.py
```

El servidor iniciará en `http://localhost:8000`

### Paso 6: Iniciar el Frontend

Opción A - Servir con Python:

```bash
cd frontend
python -m http.server 3000
```

Opción B - Servir con Node.js:

```bash
cd frontend
npx http-server -p 3000
```

Luego, abre `http://localhost:3000` en tu navegador.

## 🚀 Uso

### Análisis de Texto
1. Selecciona la pestaña "Texto"
2. Pega el texto a analizar
3. Haz clic en "Analizar"
4. Revisa el resultado con nivel, color y recomendaciones

### Análisis de URL
1. Selecciona la pestaña "URL"
2. Ingresa la URL a analizar
3. Haz clic en "Analizar URL"
4. Revisa el resultado

### Análisis de Teléfono
1. Selecciona la pestaña "Teléfono"
2. Ingresa el número de teléfono
3. Haz clic en "Analizar Teléfono"
4. Revisa el resultado

### Análisis de Imagen
1. Selecciona la pestaña "Imagen"
2. Sube la imagen a analizar
3. Haz clic en "Analizar Imagen"
4. Revisa el resultado

### Reportar Fraude
1. Ve a la sección "Denuncia Comunitaria"
2. Selecciona el tipo de reporte (Teléfono, URL, Texto)
3. Ingresa el valor a reportar
4. Describe el fraude
5. Haz clic en "Reportar"
6. Recibe el ID del reporte y cantidad de reportes previos

## 🔌 Endpoints API

### Health
- `GET /api/health` - Verificar estado del sistema

### Analyze
- `POST /api/analyze/text` - Analizar texto
- `POST /api/analyze/url` - Analizar URL
- `POST /api/analyze/phone` - Analizar teléfono
- `POST /api/analyze/image` - Analizar imagen

### Community
- `POST /api/community/report` - Enviar reporte comunitario
- `GET /api/community/check/{value}` - Consultar reportes previos
- `GET /api/community/reports/{type}` - Obtener reportes por tipo

### Root
- `GET /` - Información del sistema

Ver [documentación de la API](http://localhost:8000/docs) para más detalles.

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `ABUSEIPDB_API_KEY` | API Key de AbuseIPDB | Sí |
| `URLSCAN_API_KEY` | API Key de URLScan.io | Sí |
| `IPQS_API_KEY` | API Key de IPQualityScore | Sí |
| `ZAI_API_KEY` | API Key de Z.AI | Sí |

### Niveles de Riesgo

- **0-30**: Seguro (Verde)
- **31-60**: Sospechoso (Amarillo)
- **61-80**: Probable estafa (Naranja)
- **81-100**: Estafa confirmada (Rojo)

## 🌍 Despliegue

### Backend

#### Opción 1: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

#### Opción 2: Servidor Python

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Opción 3: Systemd Service

Crea un archivo `/etc/systemd/system/lapa-vigia.service`:

```ini
[Unit]
Description=Lapa vigIA Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/lapa-vigia/backend
ExecStart=/usr/bin/python3 /path/to/lapa-vigia/backend/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activa el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lapa-vigia
sudo systemctl start lapa-vigia
```

### Frontend

#### Opción 1: Nginx

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        root /path/to/lapa-vigia/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Opción 2: Vercel/Netlify

1. Sube el contenido de la carpeta `frontend` a Vercel o Netlify
2. Configura el backend en Vercel/Netlify Functions o usa tu propio servidor

#### Opción 3: GitHub Pages

```bash
cd frontend
npm install -g serve
serve -s . -l 3000
```

## 📁 Estructura del Proyecto

```
lapa-vigia/
├── backend/
│   ├── main.py                  # Aplicación principal FastAPI
│   ├── requirements.txt         # Dependencias Python
│   ├── .env.example             # Plantilla de variables de entorno
│   ├── models/
│   │   ├── request_models.py    # Modelos de solicitud Pydantic
│   │   └── response_models.py   # Modelos de respuesta Pydantic
│   ├── routers/
│   │   ├── health.py            # Router de salud
│   │   ├── analyze.py           # Router de análisis
│   │   └── community.py         # Router de comunidad
│   └── services/
│       ├── url_service.py       # Servicio de análisis de URL
│       ├── phone_service.py     # Servicio de análisis de teléfono
│       ├── text_service.py      # Servicio de análisis de texto
│       ├── image_service.py     # Servicio de análisis de imagen
│       ├── score_calculator.py  # Calculadora de puntajes
│       ├── rag_service.py       # Servicio RAG
│       └── community_service.py # Servicio de reportes comunitarios
├── frontend/
│   ├── index.html               # Página principal PWA
│   ├── app.js                   # Lógica del frontend
│   ├── style.css                # Estilos CSS
│   ├── manifest.json            # Manifest PWA
│   └── sw.js                    # Service Worker
├── data/
│   ├── cr_patterns.json         # Patrones de fraude CR
│   └── institutions.json        # Directorio de instituciones
├── docs/
│   └── architecture.md          # Documentación de arquitectura
├── README.md                    # Este archivo
└── LICENSE                      # Licencia MIT
```

## 💰 Modelo de Negocio

Lapa vigIA es una plataforma **open-source** con el siguiente modelo de negocio:

### Modelo Actual
- **Gratis para usuarios**: Plataforma gratuita para detectar fraudes
- **APIs de pago**: Las APIs externas tienen costos que se pueden integrar

### Modelo Futuro
- **Freemium**:
  - Free: Análisis limitado por día
  - Pro: Análisis ilimitado + reportes comunitarios
- **API B2B**: Proveer API de análisis de fraude a empresas
- **Alertas Premium**: Notificaciones en tiempo real de fraudes reportados
- **Integración Bancaria**: Colaboración con bancos para prevención de fraude

### Ingresos Potenciales
1. **Suscripciones B2B**: Empresas que integran la API
2. **Análisis Premium**: Usuarios que pagan por análisis ilimitados
3. **Publicidad**: Anuncios contextuales en la plataforma
4. **Consultoría**: Implementación y optimización de sistemas de fraude

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor sigue estos pasos:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guía de Contribución

- Escribe código limpio y comentado
- Sigue las convenciones de código existentes
- Añade tests para nuevas funcionalidades
- Actualiza la documentación
- Comenta en PRs de otros

## 📞 Autor

**Ariel Molbert - Oriceti**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: contacto@lapavigia.cr
- Sitio Web: [https://lapavigia.cr](https://lapavigia.cr)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 Ariel Molbert - Oriceti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Agradecimientos

- Equipo de Z.AI por los modelos de lenguaje
- Equipo de ChromaDB por la base de datos vectorial
- Comunidad de Costa Rica por el feedback
- Open Source community por las herramientas y recursos

## 📊 Métricas del Proyecto

- **Fecha de creación**: 2024
- **Versión actual**: 1.0.0
- **Lenguajes**: Python, JavaScript, CSS
- **Licencia**: MIT
- **Estado**: Activo

## 🔗 Enlaces Útiles

- [Documentación de la API](http://localhost:8000/docs)
- [Documentación de Arquitectura](docs/architecture.md)
- [PWA Best Practices](https://web.dev/progressive-web-apps/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📝 Changelog

### Versión 1.0.0 (2024)
- ✨ Primer release de Lapa vigIA
- 🎯 Análisis de texto, URL, teléfono e imagen
- 🤖 Integración con Z.AI GLM-4.7-Flash
- 🌐 APIs de seguridad (AbuseIPDB, URLScan.io, IPQualityScore)
- 👥 Sistema de reportes comunitarios
- 📱 PWA completa
- 📚 Base de conocimiento con patrones de fraude CR

---

Hecho con ❤️ por [Ariel Molbert - Oriceti](https://github.com/tu-usuario)
