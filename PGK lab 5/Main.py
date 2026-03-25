import raylib as rl
from Ship import Ship

SCREEN_W = 800
SCREEN_H = 600


def main():
    rl.InitWindow(SCREEN_W, SCREEN_H, b"statek")
    rl.SetTargetFPS(60)

    ship = Ship(SCREEN_W // 2, SCREEN_H // 2)

    while not rl.WindowShouldClose():
        dt = rl.GetFrameTime()

        ship.update(dt)

        rl.BeginDrawing()
        rl.ClearBackground(rl.BLACK)

        ship.draw()

        rl.DrawText(b"Strzalki: obrot | Gora: thrust", 10, 10, 18, rl.DARKGRAY)

        rl.EndDrawing()

    rl.CloseWindow()


if __name__ == "__main__":
    main()