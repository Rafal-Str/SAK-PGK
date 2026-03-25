import math
import raylib as rl

ROT_SPEED = 2.5 
THRUST    = 200.0
FRICTION  = 60.0
MAX_SPEED = 300.0

DEBUG = True # BALISTYKA aby wyłączyć zmień na False

VERTS = [(0, -15), (-10, 10), (10, 10)]
FLAME = [(0, 18), (-6, 10), (6, 10)]


def rotate_point(x, y, angle):
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


def _to_screen(verts, cx, cy, angle):
    result = []
    for lx, ly in verts:
        rx, ry = rotate_point(lx, ly, angle)
        result.append((int(cx + rx), int(cy + ry)))
    return result


def _draw_poly(pts, color):
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        rl.DrawLine(x0, y0, x1, y1, color)


class Ship:

    def __init__(self, x, y):
        self.x     = float(x)  
        self.y     = float(y)
        self.angle = 0.0    
        self.vx    = 0.0    
        self.vy    = 0.0
        self.thrusting = False  

    def update(self, dt):

        if rl.IsKeyDown(rl.KEY_LEFT):
            self.angle -= ROT_SPEED * dt
        if rl.IsKeyDown(rl.KEY_RIGHT):
            self.angle += ROT_SPEED * dt

        self.thrusting = bool(rl.IsKeyDown(rl.KEY_UP))
        if self.thrusting:
            self.vx += math.sin(self.angle) * THRUST * dt
            self.vy -= math.cos(self.angle) * THRUST * dt

        speed = math.hypot(self.vx, self.vy)
        if speed > 0:
            decel = min(FRICTION * dt, speed)
            self.vx -= (self.vx / speed) * decel
            self.vy -= (self.vy / speed) * decel

        speed = math.hypot(self.vx, self.vy)
        if speed > MAX_SPEED:
            scale = MAX_SPEED / speed
            self.vx *= scale
            self.vy *= scale

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):

        hull_pts = _to_screen(VERTS, self.x, self.y, self.angle)
        _draw_poly(hull_pts, rl.WHITE)

        if self.thrusting:
            flame_pts = _to_screen(FLAME, self.x, self.y, self.angle)
            _draw_poly(flame_pts, rl.ORANGE)

        if DEBUG:
            speed = math.hypot(self.vx, self.vy)
            scale = 0.3
            ex = int(self.x + self.vx * scale)
            ey = int(self.y + self.vy * scale)
            rl.DrawLine(int(self.x), int(self.y), ex, ey, rl.GREEN)
            label = f"v = {speed:.1f} px/s".encode()
            rl.DrawText(label, 10, 40, 18, rl.GREEN)