from PIL import Image, ImageDraw, ImageFont

width = 768
height = 400


position_list = ["skull", 
                 "right_humeral_head", 
                 "left_humeral_head", 
                 "right_scapula", 
                 "left_scapula",
                 "right_elbow",
                 "left_elbow",
                 "right_wrist",
                 "left_wrist", 
                 "T1", 
                 "carina", 
                 "T12", 
                 "L5", 
                 "right_iliac_crest", 
                 "left_iliac_crest",
                 "public_symphysis",
                 "right_femoral_head",
                 "left_femoral_head"]

position_specific_list = ["centered on the nasal septum at the level of the inferior orbital rim",
                          "centered on the humeral head",
                          "centered on the humeral head",
                          "centered at the inferior angle of the right scapula",
                          "centered at the inferior angle of the left scapula",
                          "centered on the olecranon process",
                          "centered on the olecranon process",
                          "centered on the distal radius, styloid process",
                          "centered on the distal radius, styloid process",
                          "centered on T1 vertebral body",
                          "centered at the carina",
                          "centered on T12 vertebral body",
                          "centered on the L5 vertebral body",
                          "centered at the top of the iliac crest",
                          "centered at the top of the iliac crest",
                          "centered on the pubic symphysism",
                          "centered on the femoral head",
                          "centered on the femoral head"]

font = ImageFont.load_default(size=20)



for position, specific in zip(position_list, position_specific_list):
    img = Image.new('RGB', (width, height), color='white')
    imgDraw = ImageDraw.Draw(img)   

    imgDraw.text((10, 10), "1. For the big move, use the top-left image", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 35), "Simply left-clicking to the target will lead to the target", font=font, fill=(0, 0, 0))
    imgDraw.text((10, 60), "(To generate right-bottom x ray image, it takes 3 seconds)", font=font, fill=(0, 0, 0))

    imgDraw.text((10, 110), "2. Nevigate to the", font=font, fill=(0, 0, 0))
    imgDraw.text((180, 110), f"{position}", font=font, fill=(255, 0, 0))
    imgDraw.text((10, 135), f"{specific}", font=font, fill=(255, 0, 0))

    imgDraw.text((10, 185), "3. Fine-tuning can be done by clicking on generated xray image", font=font, fill=(0, 0, 0))

    imgDraw.text((10, 235), f"3. Once you are done positioning it at the center, press ", font=font, fill=(0, 0, 0))
    imgDraw.text((500, 235), f"Finish", font=font, fill=(255, 0, 0))

    img.save(f'result_text/{position}.png')
