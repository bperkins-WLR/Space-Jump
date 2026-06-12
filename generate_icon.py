"""Generate the Cloud Hopper home-screen icon (sky theme)."""
from PIL import Image, ImageDraw, ImageFilter
import math
import random

SIZE = 1024
ASSET_DIR = "/Users/Bricep11/space-jumper"

# ---------- Background: vertical sky gradient (deep blue -> pale horizon) ----------
img = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
px = img.load()
TOP = (58, 128, 200)     # 0x3a80c8 — matches in-game skyTop
MID = (136, 204, 255)    # 0x88ccff — skyMid
BOT = (226, 240, 255)    # 0xe2f0ff — skyBot
for y in range(SIZE):
    t = y / SIZE
    if t < 0.55:
        f = t / 0.55
        r = int(TOP[0] + (MID[0] - TOP[0]) * f)
        g = int(TOP[1] + (MID[1] - TOP[1]) * f)
        b = int(TOP[2] + (MID[2] - TOP[2]) * f)
    else:
        f = (t - 0.55) / 0.45
        r = int(MID[0] + (BOT[0] - MID[0]) * f)
        g = int(MID[1] + (BOT[1] - MID[1]) * f)
        b = int(MID[2] + (BOT[2] - MID[2]) * f)
    for x in range(SIZE):
        px[x, y] = (r, g, b)

img = img.convert("RGBA")
draw = ImageDraw.Draw(img, "RGBA")

# ---------- Sun (upper right, soft glow) ----------
glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([700, 30, 1010, 340], fill=(255, 245, 200, 180))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img = Image.alpha_composite(img, glow)
draw = ImageDraw.Draw(img, "RGBA")
draw.ellipse([790, 110, 950, 270], fill=(255, 248, 215, 255))

# ---------- Background clouds (soft, behind the fox) ----------
def cloud(cx, cy, scale, alpha=235):
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    cd = ImageDraw.Draw(layer)
    puffs = [
        (0, 0, 110), (-90, 18, 80), (95, 15, 85),
        (-45, -35, 75), (50, -32, 70), (150, 28, 55), (-150, 30, 55)
    ]
    for dx, dy, r in puffs:
        r = int(r * scale)
        x, y = cx + int(dx * scale), cy + int(dy * scale)
        cd.ellipse([x - r, y - int(r * 0.8), x + r, y + int(r * 0.8)],
                   fill=(255, 255, 255, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    return layer

img = Image.alpha_composite(img, cloud(170, 250, 0.7, 200))
img = Image.alpha_composite(img, cloud(870, 430, 0.55, 190))
img = Image.alpha_composite(img, cloud(120, 600, 0.5, 170))
draw = ImageDraw.Draw(img, "RGBA")

# ---------- Birds (simple distant chevrons) ----------
for bx, by, s in [(300, 170, 16), (360, 200, 12), (650, 300, 14)]:
    draw.arc([bx - s, by - s // 2, bx, by + s // 2], 180, 320, fill=(60, 70, 95, 255), width=4)
    draw.arc([bx, by - s // 2, bx + s, by + s // 2], 220, 360, fill=(60, 70, 95, 255), width=4)

# ---------- Cloud sea at the bottom ----------
sea = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
sd = ImageDraw.Draw(sea)
random.seed(11)
for i in range(26):
    cx = random.randint(-60, SIZE + 60)
    cy = random.randint(905, 1010)
    r = random.randint(60, 130)
    sd.ellipse([cx - r, cy - int(r * 0.62), cx + r, cy + int(r * 0.62)],
               fill=(255, 255, 255, 255))
sea = sea.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img, sea)
draw = ImageDraw.Draw(img, "RGBA")

# ---------- Platform under the fox ----------
plat_top, plat_bot = 770, 830
# soft shadow under platform onto the cloud sea
shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
shd.ellipse([240, 880, 784, 950], fill=(70, 110, 160, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, shadow)
draw = ImageDraw.Draw(img, "RGBA")

draw.rounded_rectangle([180, plat_top, 844, plat_bot], radius=14, fill=(80, 230, 170, 255))
draw.rounded_rectangle([180, plat_top, 844, plat_top + 14], radius=10, fill=(180, 255, 220, 255))

# ---------- Fox head (same friendly fox, brighter daytime light) ----------
ORANGE = (226, 110, 40, 255)
WHITE  = (252, 246, 232, 255)
DARK   = (90, 40, 16, 255)
BLACK  = (25, 20, 18, 255)
AMBER  = (255, 200, 90, 255)

def triangle(pts, fill):
    draw.polygon(pts, fill=fill)

# Ears
triangle([(300, 350), (380, 200), (430, 360)], fill=ORANGE)
triangle([(340, 320), (380, 240), (410, 330)], fill=WHITE)
triangle([(370, 218), (385, 198), (395, 220)], fill=DARK)
triangle([(720, 350), (640, 200), (590, 360)], fill=ORANGE)
triangle([(680, 320), (640, 240), (610, 330)], fill=WHITE)
triangle([(625, 218), (640, 198), (655, 220)], fill=DARK)

# Head
draw.ellipse([300, 320, 720, 740], fill=ORANGE)
hl = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
hd2 = ImageDraw.Draw(hl)
hd2.ellipse([330, 340, 690, 560], fill=(255, 170, 90, 170))
hl = hl.filter(ImageFilter.GaussianBlur(20))
img = Image.alpha_composite(img, hl)
draw = ImageDraw.Draw(img, "RGBA")

# Cheek ruffs
soft = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
sfd = ImageDraw.Draw(soft)
sfd.ellipse([285, 540, 430, 700], fill=WHITE)
sfd.ellipse([590, 540, 735, 700], fill=WHITE)
soft = soft.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img, soft)
draw = ImageDraw.Draw(img, "RGBA")

# Snout
draw.ellipse([420, 540, 600, 700], fill=WHITE)
draw.polygon([(485, 555), (535, 555), (510, 590)], fill=BLACK)
draw.ellipse([484, 545, 538, 580], fill=BLACK)
draw.line([(510, 595), (510, 625)], fill=BLACK, width=4)
draw.arc([470, 605, 510, 645], 270, 360, fill=BLACK, width=5)
draw.arc([510, 605, 550, 645], 180, 270, fill=BLACK, width=5)

# Eyes
for ex in (415, 605):
    draw.ellipse([ex - 38, 430, ex + 38, 506], fill=AMBER)
    draw.ellipse([ex - 10, 442, ex + 10, 494], fill=BLACK)
    draw.ellipse([ex + 8, 438, ex + 22, 452], fill=(255, 255, 255, 255))

# Eyebrow markings
draw.polygon([(370, 395), (445, 380), (445, 410), (380, 420)], fill=(185, 80, 28, 255))
draw.polygon([(650, 395), (575, 380), (575, 410), (640, 420)], fill=(185, 80, 28, 255))

# ---------- Save ----------
img = img.convert("RGB")
master = f"{ASSET_DIR}/icon-1024.png"
img.save(master, "PNG", optimize=True)
print("Saved:", master)
