import os
import glob
from PIL import Image, ImageChops

ASSETS_PATH = "./assets"

images_to_fix = [os.path.normpath(g) for g in glob.glob("./src/cards2fix/**/*", recursive=True) if os.path.isfile(g)]

def fix_zextra_orientation(img):
    img = img.rotate(90, expand=True)
    return img

def fix_whitspaces(img):
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if bbox:
        return img.crop(bbox)

    return img

def fix_image(image_path, image_type):
    id = image_path.split("\\")[-1].split(".")[0]
    series = id.split('-')[0]

    if series == "P":
        series = "PromotionCards"

    dest_path = f'{ASSETS_PATH}/{series}/{id}.webp'

    with Image.open(image_path) as img:
        if image_type == "zextra":
            img = fix_zextra_orientation(img)
            img = fix_whitspaces(img)

            img.save(dest_path, format='webp')


for image_path in images_to_fix:
    image_type = image_path.split("\\")[-2]
    fix_image(image_path, image_type)