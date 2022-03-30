def crop_circle(img_path):
    img = Image.open(img_path)
    h, w = img.size
    lum_img = Image.new('L', [h, w], 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0, 0), (h, w)], 0, 360, fill=255)
    final_image = ImageOps.fit(img, lum_img.size, centering=(0.5, 0.5))
    final_image.putalpha(lum_img)
    return final_image

def save_circular_image(surf: pygame.Surface, import_path, export_path, color_key=(255, 255, 255), img_type='PNG'):
    key_red, key_green, key_blue = color_key
    pygame.image.save(surf, import_path)
    img = Image.open(import_path)
    img = img.convert('RGBA')
    data = img.getdata()

    data_with_alpha = []
    for item in data:
        if item[0] == key_red and item[1] == key_green and item[2] == key_blue:
            data_with_alpha.append((255, 255, 255, 0))
        else:
            data_with_alpha.append(item)

    img.putdata(data_with_alpha)

    img.save(export_path, img_type)

    final_image = crop_circle(export_path)
    final_image.save(export_path, img_type)
    remove(import_path)
