"""Generate the Space Jumper home-screen icon."""
from PIL import Image, ImageDraw, ImageFilter
import math
import random

SIZE = 1024
ASSET_DIR = "/Users/Bricep11/space-jumper"

# ---------- Background: radial gradient (deep blue -> purple) ----------
img = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
px = img.load()
cx, cy = SIZE / 2, SIZE / 2
max_d = math.hypot(cx, cy)
for y in range(SIZE):
    for x in range(SIZE):
        d = math.hypot(x - cx, y - cy) / max_d
        # inner: deep indigo, outer: near black
        r = int(20 + (4 - 20) * d)
        g = int(8 + (0 - 8) * d)
        b = int(50 + (16 - 50) * d)
        # add a purple wash near top
        ty = y / SIZE
        r = min(255, r + int(30 * (1 - ty)))
        b = min(255, b + int(20 * (1 - ty)))
        px[x, y] = (max(0, r), max(0, g), max(0, b))

draw = ImageDraw.Draw(img, "RGBA")

# ---------- Stars ----------
random.seed(7)
for _ in range(140):
    sx = random.randint(0, SIZE - 1)
    sy = random.randint(0, int(SIZE * 0.7))
    sr = random.choice([1, 1, 2, 2, 3])
    alpha = random.randint(140, 255)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, alpha))

# bigger sparkle stars
for sx, sy, sr in [(180, 200, 6), (820, 160, 8), (760, 350, 5), (200, 480, 4)]:
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, 255))
    # cross-shaped glint
    draw.line([(sx - sr * 4, sy), (sx + sr * 4, sy)], fill=(255, 255, 255, 110), width=2)
    draw.line([(sx, sy - sr * 4), (sx, sy + sr * 4)], fill=(255, 255, 255, 110), width=2)

# ---------- Lava glow at bottom ----------
lava_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
ldraw = ImageDraw.Draw(lava_layer)
# big soft orange ellipse near the bottom
ldraw.ellipse([-200, 780, SIZE + 200, 1300], fill=(255, 80, 30, 220))
ldraw.ellipse([100, 880, SIZE - 100, 1200], fill=(255, 180, 70, 200))
lava_layer = lava_layer.filter(ImageFilter.GaussianBlur(40))
img = Image.alpha_composite(img.convert("RGBA"), lava_layer)
draw = ImageDraw.Draw(img, "RGBA")

# distinct lava band (sharp top edge)
draw.rectangle([0, 920, SIZE, SIZE], fill=(220, 50, 10, 255))
# molten flecks
for _ in range(40):
    fx = random.randint(0, SIZE - 1)
    fy = random.randint(920, SIZE - 8)
    fr = random.randint(3, 10)
    draw.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=(255, 220, 90, 230))

# ---------- Platform under the fox ----------
plat_top, plat_bot = 770, 830
draw.rounded_rectangle([180, plat_top, 844, plat_bot], radius=14, fill=(80, 230, 170, 255))
# platform shine
draw.rounded_rectangle([180, plat_top, 844, plat_top + 14], radius=10, fill=(180, 255, 220, 255))
# platform shadow on lava
shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow)
sdraw.ellipse([220, 870, 804, 940], fill=(0, 0, 0, 130))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, shadow)
draw = ImageDraw.Draw(img, "RGBA")

# ---------- Fox head (stylized, sits on the platform) ----------
# Coordinates centered ~ (512, 500)
ORANGE  = (220, 95, 30, 255)
ORANGE2 = (255, 130, 50, 255)
WHITE   = (250, 240, 220, 255)
DARK    = (90, 30, 10, 255)
BLACK   = (15, 12, 12, 255)
AMBER   = (255, 200, 90, 255)

# Ears (triangles, with inner detail)
def triangle(pts, fill):
    draw.polygon(pts, fill=fill)

# Left ear
triangle([(300, 350), (380, 200), (430, 360)], fill=ORANGE)
triangle([(340, 320), (380, 240), (410, 330)], fill=WHITE)
triangle([(370, 218), (385, 198), (395, 220)], fill=DARK)
# Right ear
triangle([(720, 350), (640, 200), (590, 360)], fill=ORANGE)
triangle([(680, 320), (640, 240), (610, 330)], fill=WHITE)
triangle([(625, 218), (640, 198), (655, 220)], fill=DARK)

# Head (rounded — use overlapping ellipses)
draw.ellipse([300, 320, 720, 740], fill=ORANGE)
# subtle highlight on top
hl = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
hdraw = ImageDraw.Draw(hl)
hdraw.ellipse([330, 340, 690, 560], fill=(255, 160, 80, 180))
hl = hl.filter(ImageFilter.GaussianBlur(20))
img = Image.alpha_composite(img, hl)
draw = ImageDraw.Draw(img, "RGBA")

# Cheek ruffs (white fluff)
draw.ellipse([285, 540, 430, 700], fill=WHITE)
draw.ellipse([590, 540, 735, 700], fill=WHITE)
# Blend the cheek edge a bit using a soft mask
soft = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
sd = ImageDraw.Draw(soft)
sd.ellipse([285, 540, 430, 700], fill=(250, 240, 220, 255))
sd.ellipse([590, 540, 735, 700], fill=(250, 240, 220, 255))
soft = soft.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img, soft)
draw = ImageDraw.Draw(img, "RGBA")

# Snout (white)
draw.ellipse([420, 540, 600, 700], fill=WHITE)
# Nose (black, rounded triangle)
draw.polygon([(485, 555), (535, 555), (510, 590)], fill=BLACK)
draw.ellipse([484, 545, 538, 580], fill=BLACK)
# Mouth
draw.line([(510, 595), (510, 625)], fill=BLACK, width=4)
draw.arc([470, 605, 510, 645], 270, 360, fill=BLACK, width=5)
draw.arc([510, 605, 550, 645], 180, 270, fill=BLACK, width=5)

# Eyes (amber with black pupil)
for ex in (415, 605):
    # whites of eye / amber iris
    draw.ellipse([ex - 38, 430, ex + 38, 506], fill=AMBER)
    # pupil (vertical slit-ish)
    draw.ellipse([ex - 10, 442, ex + 10, 494], fill=BLACK)
    # highlight
    draw.ellipse([ex + 8, 438, ex + 22, 452], fill=(255, 255, 255, 255))

# Eyebrow markings (a touch darker orange)
draw.polygon([(370, 395), (445, 380), (445, 410), (380, 420)], fill=(180, 70, 20, 255))
draw.polygon([(650, 395), (575, 380), (575, 410), (640, 420)], fill=(180, 70, 20, 255))

# ---------- Vignette ----------
v = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
vd = ImageDraw.Draw(v)
vd.rectangle([0, 0, SIZE, SIZE], fill=(0, 0, 0, 0))
vd.ellipse([-200, -200, SIZE + 200, SIZE + 200], outline=(0, 0, 0, 90), width=120)
v = v.filter(ImageFilter.GaussianBlur(60))
img = Image.alpha_composite(img, v)

# ---------- Save ----------
img = img.convert("RGB")
master = f"{ASSET_DIR}/icon-1024.png"
img.save(master, "PNG", optimize=True)
print("Saved:", master)
