class Hand {
    constructor(length, width, color) {
        this.length = length;
        this.width = width;
        this.color = color;
    }

    draw(ctx, angle) {
        ctx.save();

        ctx.rotate(angle);

        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(0, -this.length);
        ctx.lineWidth = this.width;
        ctx.strokeStyle = this.color;
        ctx.stroke();

        ctx.restore();
    }
}

class Clock {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");

        this.width = canvas.width;
        this.height = canvas.height;
        this.radius = Math.min(this.width, this.height) / 2 - 20;

        this.isPaused = false;

        // wskazówki
        this.hourHand = new Hand(this.radius * 0.5, 6, "black");
        this.minuteHand = new Hand(this.radius * 0.75, 4, "black");
        this.secondHand = new Hand(this.radius * 0.9, 2, "red");

        this.initEvents();
        this.animate();
    }

    initEvents() {
        window.addEventListener("keydown", (e) => {
            if (e.code === "Space") {
                this.isPaused = !this.isPaused;
            }
        });
    }

    drawFace() {
        const ctx = this.ctx;

        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 4;
        ctx.stroke();

        // kreseczki godzinowe
        for (let i = 0; i < 12; i++) {
            ctx.save();
            ctx.rotate((i * Math.PI) / 6);

            ctx.beginPath();
            ctx.moveTo(0, -this.radius);
            ctx.lineTo(0, -this.radius + 15);
            ctx.lineWidth = 3;
            ctx.stroke();

            ctx.restore();
        }
    }

    update() {
        const now = new Date();

        const ms = now.getMilliseconds();
        const seconds = now.getSeconds() + ms / 1000;
        const minutes = now.getMinutes() + seconds / 60;
        const hours = (now.getHours() % 12) + minutes / 60;

        return {
            hourAngle: hours * Math.PI / 6 - Math.PI / 2,
            minuteAngle: minutes * Math.PI / 30 - Math.PI / 2,
            secondAngle: seconds * Math.PI / 30 - Math.PI / 2
        };
    }

    draw() {
        const ctx = this.ctx;

        ctx.clearRect(0, 0, this.width, this.height);

        ctx.save();

        // centrowanie canvas
        ctx.translate(this.width / 2, this.height / 2);

        this.drawFace();

        const angles = this.update();

        this.hourHand.draw(ctx, angles.hourAngle);
        this.minuteHand.draw(ctx, angles.minuteAngle);
        this.secondHand.draw(ctx, angles.secondAngle);

        ctx.restore();
    }

    animate() {
        if (!this.isPaused) {
            this.draw();
        }

        requestAnimationFrame(() => this.animate());
    }
}

const canvas = document.getElementById("clockCanvas");
const clock = new Clock(canvas);