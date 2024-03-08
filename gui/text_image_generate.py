from PIL import Image, ImageDraw, ImageFont

width = 768
height = 400


position_list = ["skull", "right_humeral_head", "left_humeral_head", "right_capula", "left_scapula", "T1", "carina", "T12", "L5", "right_iliac_crest", "left_iliac_crest"]

font = ImageFont.load_default(size=20)



for position in position_list:
    img = Image.new('RGB', (width, height), color='white')
    imgDraw = ImageDraw.Draw(img)   

    imgDraw.text((10, 10), "1. The view is randomly chosen ", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 35), "Pressing on left key of the mouse and drag", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 60), "Dragging the mouse while pressing will move the green object", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 85), "The green object is a c-arm head", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 110), "2. Nevigate to the", font=font, fill=(0, 0, 0))
    imgDraw.text((180, 110), f"{position}", font=font, fill=(255, 0, 0))
    imgDraw.text((10, 135), f"3. Once you are done positioning it at the center, press ", font=font, fill=(0, 0, 0))
    imgDraw.text((500, 135), f"Finish", font=font, fill=(255, 0, 0))

    imgDraw.text((10, 180), f"The simulated x-ray should be generated automatcially when you stop clicking", font=font, fill=(255, 0, 0))
    imgDraw.text((10, 205), f"It takes about 3 seconds to generate", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 230), f"If it does not, move your mouse (don't click)", font=font, fill=(0, 0, 0))
    img.save(f'result/{position}.png')
