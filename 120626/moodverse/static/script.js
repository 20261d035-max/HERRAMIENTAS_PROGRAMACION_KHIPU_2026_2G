document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.mood-btn');
    const body = document.body;
    const phraseEl = document.getElementById('mood-phrase');
    const authorEl = document.getElementById('mood-author');

    // 1. Manejo del Cambio de Mood vía API Fetch
    buttons.forEach(button => {
        button.addEventListener('click', async () => {
            const mood = button.getAttribute('data-mood');
            
            // Cambiar clase activa en los botones
            buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Transición suave del contenido (Fade Out)
            phraseEl.style.opacity = '0';
            authorEl.style.opacity = '0';

            // Petición asíncrona a nuestro servidor Flask
            try {
                const response = await fetch(`/api/mood/${mood}`);
                const data = await response.json();

                setTimeout(() => {
                    // Cambiar el Mood en el body (actualiza colores CSS)
                    body.className = `mood-${mood}`;
                    
                    // Actualizar textos e inyectar el Fade In
                    phraseEl.innerText = data.frase;
                    authorEl.innerText = `— ${data.autor}`;
                    phraseEl.style.opacity = '1';
                    authorEl.style.opacity = '1';
                    
                    // Actualizar el color de las partículas según el Mood
                    updateParticleColor();
                }, 300);

            } catch (error) {
                console.error("Error al obtener el mood:", error);
            }
        });
    });

    // 2. Sistema de Partículas Interactivas (HTML5 Canvas)
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    
    let particlesArray = [];
    let particleColor = '#00f3ff'; // Color inicial

    // Redimensionar el lienzo
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Obtener color activo según los estilos computados del CSS
    function updateParticleColor() {
        particleColor = getComputedStyle(body).getPropertyValue('--current-glow').trim();
    }
    updateParticleColor();

    // Clase constructora de partículas
    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.size = Math.random() * 4 + 1;
            this.speedX = (Math.random() - 0.5) * 3;
            this.speedY = (Math.random() - 0.5) * 3;
            this.color = particleColor;
            this.alpha = 1;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.size > 0.1) this.size -= 0.03; // Se desvanecen al encogerse
        }

        draw() {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.shadowBlur = 10;
            ctx.shadowColor = this.color;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }

    // Evento para generar partículas al mover el mouse en toda la pantalla
    window.addEventListener('mousemove', (e) => {
        // Añade 2 partículas por cada movimiento para evitar sobrecarga de rendimiento
        for (let i = 0; i < 2; i++) {
            particlesArray.push(new Particle(e.clientX, e.clientY));
        }
    });

    // Bucle de animación (Game Loop)
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
            
            // Eliminar partículas demasiado pequeñas
            if (particlesArray[i].size <= 0.3) {
                particlesArray.splice(i, 1);
                i--;
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
});