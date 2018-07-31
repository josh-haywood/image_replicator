import sys, random, math, operator

try:
  from PIL import Image, ImageChops, ImageDraw
except:
  print("PIL not found, install it with `pip install pillow`")
  exit(1)

sys.argv += [False]*4

if not sys.argv[1]:
  print("usage: python replicator.py image.png [iterations] [circle radius] [output filename]")
  exit(1)

# open the source image
src_img = Image.open(sys.argv[1])
pixels = src_img.convert("RGBA")

# get list of unique colors
colors = list(set(src_img.getdata()))

img1 = Image.new(src_img.mode, src_img.size, "white")
img2 = Image.new(src_img.mode, src_img.size, "white")

r = int(sys.argv[3] or 25)

def draw_circle(image):
  x = random.randint(0, src_img.size[0] - 1)
  y = random.randint(0, src_img.size[1] - 1)

  draw = ImageDraw.Draw(image)
  coords = (x - r, y - r, x + r, y + r)
  draw.ellipse(coords, fill=random.choice(colors))

  return coords

def compare(image1, image2, coords):
  im1 = image1.crop(coords)
  im2 = image2.crop(coords)

  diff = ImageChops.difference(im1, im2)
  h = diff.histogram()
  sq = (value*(idx**2) for idx, value in enumerate(h))
  sum_of_squares = sum(sq)
  rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
  return rms

rounds = int(sys.argv[2] or 2500)
for x in range(rounds):
  coords = draw_circle(img1)

  a = compare(src_img, img1, coords)
  b = compare(src_img, img2, coords)

  if a <= b:
    img2 = img1.copy()
  else:
    img1 = img2.copy()

  if x % 100 == 0 and x != 0:
    print("%d/%d iterations performed, %.02f%% done" % (x, rounds, float(x)/rounds*100))
  if x % 100 == 0 and r > 5:
    r = r / 2
    if r < 5:
      r = 5

filename = sys.argv[4] or "output.png"
img1.save(filename)
print("done, resulting image saved to %s" % filename)
