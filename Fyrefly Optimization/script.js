const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Configuración
const config = {
    nFireflies: 20,
    alpha: 0.2,      // Aleatoriedad
    beta0: 1.0,      // Atracción máxima
    gamma: 0.01,     // Absorción de luz
    bounds: 200,     // Límites del espacio
    centerX: 300,    // Centro del canvas
    centerY: 300
};

let fireflies = [];
let generation = 0;
let isRunning = false;
let animationId = null;
let bestValue = Infinity;

// Función objetivo
function objectiveFunction(x, y) {
    return x * x + y * y;
}

// Brillo
function calculateBrightness(x, y) {
    const value = objectiveFunction(x, y);
    return 1 / (1 + value);
}

// Distancia
function distance(x1, y1, x2, y2) {
    return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

// Inicializar luciérnagas
function initializeFireflies() {
    fireflies = [];
    for (let i = 0; i < config.nFireflies; i++) {
        const x = Math.random() * config.bounds * 2 - config.bounds;
        const y = Math.random() * config.bounds * 2 - config.bounds;
        fireflies.push({
            x,
            y,
            brightness: calculateBrightness(x, y),
            value: objectiveFunction(x, y)
        });
    }
    generation = 0;
    bestValue = Math.min(...fireflies.map(f => f.value));
    updateStats();
}

// Actualizar posiciones
function updateFireflies() {
    for (let i = 0; i < fireflies.length; i++) {
        let fi = fireflies[i];

        for (let j = 0; j < fireflies.length; j++) {
            let fj = fireflies[j];
            if (fj.brightness > fi.brightness) {
                const r = distance(fi.x, fi.y, fj.x, fj.y);
                const beta = config.beta0 * Math.exp(-config.gamma * r * r);
                fi.x += beta * (fj.x - fi.x) + config.alpha * (Math.random() - 0.5) * 20;
                fi.y += beta * (fj.y - fi.y) + config.alpha * (Math.random() - 0.5) * 20;
                fi.x = Math.max(-config.bounds, Math.min(config.bounds, fi.x));
                fi.y = Math.max(-config.bounds, Math.min(config.bounds, fi.y));
            }
        }

        fi.brightness = calculateBrightness(fi.x, fi.y);
        fi.value = objectiveFunction(fi.x, fi.y);
    }

    bestValue = Math.min(...fireflies.map(f => f.value));
    generation++;
    config.alpha *= 0.98;
    updateStats();
}

// Dibujar
function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(config.centerX, 0);
    ctx.lineTo(config.centerX, canvas.height);
    ctx.moveTo(0, config.centerY);
    ctx.lineTo(canvas.width, config.centerY);
    ctx.stroke();

    for (let r of [50, 100, 150, 200, 250]) {
        ctx.beginPath();
        ctx.arc(config.centerX, config.centerY, r, 0, Math.PI * 2);
        ctx.stroke();
    }

    ctx.fillStyle = 'rgba(34, 197, 94, 0.5)';
    ctx.beginPath();
    ctx.arc(config.centerX, config.centerY, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#22c55e';
    ctx.beginPath();
    ctx.arc(config.centerX, config.centerY, 4, 0, Math.PI * 2);
    ctx.fill();

    fireflies.forEach(f => {
        const screenX = config.centerX + f.x;
        const screenY = config.centerY + f.y;
        const size = 3 + f.brightness * 12;
        const alpha = 0.3 + f.brightness * 0.7;

        const gradient = ctx.createRadialGradient(screenX, screenY, 0, screenX, screenY, size * 2);
        gradient.addColorStop(0, `rgba(251, 191, 36, ${alpha})`);
        gradient.addColorStop(1, 'rgba(251, 191, 36, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(screenX, screenY, size * 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = `rgba(251, 191, 36, ${alpha})`;
        ctx.beginPath();
        ctx.arc(screenX, screenY, size, 0, Math.PI * 2);
        ctx.fill();
    });
}

// Actualizar estadísticas
function updateStats() {
    document.getElementById('generation').textContent = generation;
    document.getElementById('bestValue').textContent = bestValue.toFixed(6);
    document.getElementById('fireflyCount').textContent = fireflies.length;
}

// Loop
function animate() {
    updateFireflies();
    draw();
    if (isRunning) {
        animationId = setTimeout(animate, 100);
    }
}

// Controles
function toggleSimulation() {
    isRunning = !isRunning;
    const btn = document.getElementById('startBtn');
    if (isRunning) {
        btn.textContent = '⏸ Pausar';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
        animate();
    } else {
        btn.textContent = '▶ Iniciar';
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
        if (animationId) clearTimeout(animationId);
    }
}

function resetSimulation() {
    if (isRunning) toggleSimulation();
    config.alpha = 0.2;
    initializeFireflies();
    draw();
}

function stepSimulation() {
    if (isRunning) toggleSimulation();
    updateFireflies();
    draw();
}

// Iniciar
initializeFireflies();
draw();
