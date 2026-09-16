from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 900, 600


def clamp(value):
    return max(0, min(255, int(value)))


def render(path, variant):
    pixels = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            nx, ny = x / WIDTH, y / HEIGHT
            if variant == 'profile':
                base = (16 + 35 * ny, 17 + 22 * nx, 30 + 58 * nx + 22 * ny)
                glow = max(0, 1 - math.hypot(nx - .7, ny - .2) * 1.55)
                color = (base[0] + 55 * glow, base[1] + 42 * glow, base[2] + 42 * glow)
            elif variant == 'linaje':
                color = (222 - 42 * ny, 208 - 54 * nx, 188 - 43 * nx)
                glow = max(0, 1 - math.hypot(nx - .78, ny - .12) * 1.4)
                color = (color[0] + 30 * glow, color[1] + 14 * glow, color[2] - 8 * glow)
            elif variant == 'portfolio':
                glow = max(0, 1 - math.hypot(nx - .8, ny - .18) * 1.4)
                color = (22 + 55 * glow, 22 + 44 * glow, 32 + 85 * glow)
            else:
                color = (232 - 15 * ny, 237 - 16 * nx, 241 - 10 * nx)
            pixels.append(tuple(clamp(part) for part in color))

    def paint_circle(cx, cy, radius, color):
        for y in range(max(0, cy - radius), min(HEIGHT, cy + radius)):
            for x in range(max(0, cx - radius), min(WIDTH, cx + radius)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    pixels[y * WIDTH + x] = color

    def paint_rect(left, top, right, bottom, color):
        for y in range(max(0, top), min(HEIGHT, bottom)):
            for x in range(max(0, left), min(WIDTH, right)):
                pixels[y * WIDTH + x] = color

    if variant == 'profile':
        paint_circle(515, 250, 130, (30, 25, 38))
        paint_circle(515, 220, 138, (20, 18, 26))
        paint_rect(340, 390, 710, 600, (19, 17, 25))
        paint_circle(515, 425, 125, (30, 25, 38))
    elif variant == 'linaje':
        paint_circle(720, 80, 210, (165, 128, 98))
        paint_circle(180, 530, 170, (74, 58, 50))
    elif variant == 'portfolio':
        paint_rect(80, 70, 820, 530, (39, 40, 50))
        paint_circle(730, 120, 170, (110, 94, 183))
        paint_circle(760, 500, 135, (125, 155, 78))
    else:
        paint_rect(55, 55, 845, 545, (255, 255, 255))
        paint_rect(55, 55, 845, 125, (23, 33, 43))
        paint_rect(560, 195, 775, 375, (229, 233, 236))
        paint_circle(680, 270, 68, (190, 205, 211))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as image:
        image.write(f'P6\n{WIDTH} {HEIGHT}\n255\n'.encode())
        image.write(bytes(channel for pixel in pixels for channel in pixel))


render(ROOT / 'public/images/profile.ppm', 'profile')
render(ROOT / 'public/images/projects/linaje-bendito.ppm', 'linaje')
render(ROOT / 'public/images/projects/portfolio.ppm', 'portfolio')
render(ROOT / 'public/images/projects/business.ppm', 'business')
