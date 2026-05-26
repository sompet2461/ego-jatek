from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    img = Image.new('RGB', (size, size), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Piros kör
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#e94560')
    
    # EGO felirat
    font_size = size // 3
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "EGO"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='white', font=font)
    
    return img

os.makedirs('static', exist_ok=True)
create_icon(192).save('static/icon-192.png')
create_icon(512).save('static/icon-512.png')
print("Ikonok elkészültek!")