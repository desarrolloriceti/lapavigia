// Configuración
const BASE_URL = 'http://localhost:8000';

// Estado
let currentTab = 'text';
let currentScore = 0;
let currentLevel = '';
let currentColor = '';

// Elementos DOM
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const resultContainer = document.getElementById('result-container');
const scoreCircle = document.getElementById('score-circle');
const scoreNumber = document.getElementById('score-number');
const levelBadge = document.getElementById('level-badge');
const resultExplanation = document.getElementById('result-explanation');
const recommendationsList = document.getElementById('recommendations-list');
const sourcesList = document.getElementById('sources-list');

// Inicializar tabs
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        switchTab(tab.dataset.tab);
    });
});

function switchTab(tabName) {
    currentTab = tabName;

    // Actualizar tabs
    tabs.forEach(t => t.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Actualizar contenido
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Ocultar resultados anteriores
    resultContainer.style.display = 'none';
}

// Analizar contenido
async function analyzeContent(content, type) {
    try {
        const response = await fetch(`${BASE_URL}/api/analyze/${type}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ [type]: content })
        });

        if (!response.ok) {
            throw new Error('Error al analizar el contenido');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error en analyzeContent:', error);
        alert('Error al analizar el contenido. Por favor, intenta de nuevo.');
        throw error;
    }
}

// Mostrar resultados
function renderScore(result) {
    currentScore = result.score;
    currentLevel = result.level;
    currentColor = result.color;

    // Actualizar círculo de puntuación
    scoreCircle.style.background = `conic-gradient(${currentColor} ${currentScore}%, #E5E7EB ${currentScore}%)`;
    scoreNumber.textContent = currentScore;

    // Actualizar badge de nivel
    levelBadge.textContent = currentLevel;
    levelBadge.className = 'level-badge ' + getLevelClass(currentLevel);

    // Actualizar explicación
    resultExplanation.textContent = result.explanation;

    // Actualizar recomendaciones
    recommendationsList.innerHTML = '';
    result.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });

    // Actualizar fuentes
    sourcesList.innerHTML = '';
    result.sources.forEach(source => {
        const li = document.createElement('li');
        li.textContent = source;
        sourcesList.appendChild(li);
    });

    // Mostrar resultados
    resultContainer.style.display = 'block';
}

function getLevelClass(level) {
    switch (level) {
        case 'Seguro':
            return 'seguro';
        case 'Sospechoso':
            return 'sospechoso';
        case 'Probable estafa':
            return 'probable';
        case 'Estafa confirmada':
            return 'confirmada';
        default:
            return '';
    }
}

// Event Listeners - Text
document.getElementById('analyze-btn').addEventListener('click', async () => {
    const textInput = document.getElementById('text-input').value.trim();

    if (!textInput) {
        alert('Por favor, ingresa un texto para analizar');
        return;
    }

    try {
        const result = await analyzeContent(textInput, 'text');
        renderScore(result);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Event Listeners - URL
document.getElementById('analyze-btn-url').addEventListener('click', async () => {
    const urlInput = document.getElementById('url-input').value.trim();

    if (!urlInput) {
        alert('Por favor, ingresa una URL para analizar');
        return;
    }

    try {
        const result = await analyzeContent(urlInput, 'url');
        renderScore(result);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Event Listeners - Phone
document.getElementById('analyze-btn-phone').addEventListener('click', async () => {
    const phoneInput = document.getElementById('phone-input').value.trim();

    if (!phoneInput) {
        alert('Por favor, ingresa un número de teléfono para analizar');
        return;
    }

    try {
        const result = await analyzeContent(phoneInput, 'phone');
        renderScore(result);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Event Listeners - Image
document.getElementById('analyze-btn-image').addEventListener('click', async () => {
    const imageInput = document.getElementById('image-input').files[0];

    if (!imageInput) {
        alert('Por favor, selecciona una imagen para analizar');
        return;
    }

    try {
        // Convertir imagen a base64
        const reader = new FileReader();
        reader.onload = async (e) => {
            const base64Image = e.target.result;

            try {
                const result = await analyzeContent(base64Image, 'image');
                renderScore(result);
            } catch (error) {
                console.error('Error:', error);
            }
        };
        reader.readAsDataURL(imageInput);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Submit Report
document.getElementById('submit-report-btn').addEventListener('click', async () => {
    const reportType = document.getElementById('report-type').value;
    const reportValue = document.getElementById('report-value').value.trim();
    const reportDescription = document.getElementById('report-description').value.trim();

    if (!reportValue || !reportDescription) {
        alert('Por favor, completa todos los campos del reporte');
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/api/community/report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: reportType,
                value: reportValue,
                description: reportDescription
            })
        });

        if (!response.ok) {
            throw new Error('Error al enviar el reporte');
        }

        const result = await response.json();

        alert('Reporte enviado exitosamente! ID: ' + result.id);
        alert('Este valor ha sido reportado ' + result.count + ' veces en total.');

        // Limpiar formulario
        document.getElementById('report-value').value = '';
        document.getElementById('report-description').value = '';
    } catch (error) {
        console.error('Error al enviar reporte:', error);
        alert('Error al enviar el reporte. Por favor, intenta de nuevo.');
    }
});

// Check Reports
async function checkReport(value) {
    try {
        const response = await fetch(`${BASE_URL}/api/community/check/${encodeURIComponent(value)}`);

        if (!response.ok) {
            throw new Error('Error al consultar reportes');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error al consultar reportes:', error);
        return { has_reports: false, report_count: 0 };
    }
}

// Verificar reportes al cambiar tab
tabs.forEach(tab => {
    tab.addEventListener('click', async () => {
        const tabName = tab.dataset.tab;
        const valueInput = document.getElementById(`${tabName}-input`).value;

        if (valueInput) {
            try {
                const result = await checkReport(valueInput);
                if (result.has_reports) {
                    console.log(`Valor "${valueInput}" tiene ${result.report_count} reportes previos`);
                }
            } catch (error) {
                console.error('Error al verificar reportes:', error);
            }
        }
    });
});

// Inicialización
console.log('Lapa vigIA - Plataforma Antifraude Costa Rica');
console.log('Versión 1.0.0');
