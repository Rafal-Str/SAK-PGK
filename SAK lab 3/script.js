class Particle {
    constructor(x, y, vx, vy, hue) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.hue = hue;
        this.alpha = 1;
        this.decay = 0.015;
        this.active = true;
    }

    update(gravity, canvasHeight) {
        this.x += this.vx;
        this.y += this.vy;

        this.vy += gravity;

        this.vx *= 0.98;
        this.vy *= 0.98;

        this.alpha -= this.decay;

        if (this.y >= canvasHeight) {
            this.vy *= -0.6;
            this.y = canvasHeight;
        }

        if (this.alpha <= 0) {
            this.alpha = 0;
            this.active = false;
        }
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${this.hue}, 100%, 50%, ${this.alpha})`;
        ctx.fill();
    }
}


class Firework {
    constructor(startX, startY, targetX, targetY) {
        this.x = startX;
        this.y = startY;
        this.targetX = targetX;
        this.targetY = targetY;

        this.hue = Math.random() * 360;

        const speed = 8;
        const dx = targetX - startX;
        const dy = targetY - startY;
        const dist = Math.hypot(dx, dy);
        this.vx = (dx / dist) * speed;
        this.vy = (dy / dist) * speed;

        this.active = true;
        this.exploded = false;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        const dist = Math.hypot(this.targetX - this.x, this.targetY - this.y);
        if (dist < 5) {
            this.active = false;
            this.exploded = true;
        }
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = `hsl(${this.hue}, 100%, 80%)`;
        ctx.fill();
    }

    explode() {
        const particles = [];
        const count = 300;

        for (let i = 0; i < count; i++) {
            const angle = (Math.PI * 2 / count) * i;
            const speed = 2 + Math.random() * 5;
            const vx = Math.cos(angle) * speed;
            const vy = Math.sin(angle) * speed;
            const hue = this.hue + (Math.random() * 40 - 20);

            particles.push(new Particle(this.x, this.y, vx, vy, hue));
        }

        return particles;
    }
}


class FireworkShow {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');

        this.rockets = [];
        this.particles = [];
        this.gravity = 0.08;

        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;

        this.canvas.addEventListener('click', (e) => {
            const startX = this.canvas.width / 2;
            const startY = this.canvas.height;
            this.rockets.push(new Firework(startX, startY, e.clientX, e.clientY));
        });

        this.loop();
    }

    update() {
        const ctx = this.ctx;
        const H = this.canvas.height;

        ctx.clearRect(0, 0, this.canvas.width, H);

        for (const rocket of this.rockets) {
            rocket.update();
            rocket.draw(ctx);

            if (rocket.exploded) {
                const newParticles = rocket.explode();
                this.particles.push(...newParticles);
                rocket.exploded = false;
            }
        }

        for (const p of this.particles) {
            p.update(this.gravity, H);
            p.draw(ctx);
        }

        this.rockets = this.rockets.filter(r => r.active);
        this.particles = this.particles.filter(p => p.active);
    }

    loop() {
        this.update();
        requestAnimationFrame(() => this.loop());
    }
}


window.addEventListener('load', () => {
    new FireworkShow('canvas');
});