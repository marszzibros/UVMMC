from vedo import *
import os
import math
import random

# import dicom2nifti

# Function for x button
def buttonfunc_x():

    if bu1.status_idx == 0:
        plt.at(1).reset_camera()
        plt.at(1).look_at("yz")
        plt.at(1).camera.Zoom(1.5)
    if bu2.status_idx == 1:
        bu2.switch()
        bu1.switch()
    elif bu3.status_idx == 1:
        bu3.switch()
        bu1.switch()
    
    if bu6.status_idx == 1:
        bu6.switch()

# Function for y button
def buttonfunc_y():


    if bu2.status_idx == 0:
        plt.at(1).reset_camera()
        plt.at(1).look_at("xz")
        foc_temp = plt.at(1).camera.GetFocalPoint()
        pos_temp = plt.at(1).camera.GetPosition()

        plt.at(1).camera.SetFocalPoint(foc_temp[0], - foc_temp[1] + (- foc_temp[1] * 0.3), foc_temp[2])
        plt.at(1).camera.SetPosition(pos_temp[0],- pos_temp[1] + (- pos_temp[1] * 0.3), pos_temp[2])
        plt.at(1).camera.Zoom(1.5)

    if bu1.status_idx == 1:
        bu1.switch()
        bu2.switch()
    elif bu3.status_idx == 1:
        bu3.switch()
        bu2.switch()
    if bu6.status_idx == 1:
        bu6.switch()

# Function for z button
def buttonfunc_z():


    if bu3.status_idx == 0:
        plt.at(1).reset_camera()
        plt.at(1).look_at("xy")
        plt.at(1).camera.Zoom(1.5)

    if bu1.status_idx == 1:
        bu1.switch()
        bu3.switch()
    elif bu2.status_idx == 1:
        bu2.switch()
        bu3.switch()
    if bu6.status_idx == 1:
        bu6.switch()

# Function for n button
# it will turns into surgeon view of patients
def buttonfunc_n():
    if bu6.status_idx == 0:
        bu6.switch()
        plt.at(1).reset_camera()
        plt.at(1).look_at("xy")
        plt.at(1).camera.Azimuth(45)
        plt.at(1).camera.Elevation(45)
        plt.at(1).camera.Zoom(1.5)

# Function for r button
def buttonfunc_r():
    if bu6.status_idx == 0:
        plt.at(1).roll(90)
    else:
        plt.at(1).camera.Azimuth(45)
# Function for g button
def buttonfunc_g():

    loc = box.GetPosition()
    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()

    sin_rad_alpha = (pos[0] - foc[0]) / distance
    sin_rad_beta = (pos[2] - foc[2]) / distance

    os.system(f"python example_projector.py {ct_name} {loc[2] - center[2]} {loc[0] - center[0]} {loc[1] - center[1]} {math.asin(sin_rad_alpha)} {math.asin(sin_rad_beta)}")
    plt.at(3).show(Picture("example_projector.png"),axes=0, zoom=1.5)

# Wheel function
def func_wheelfor(evt):

    """
    if a or A is pressed
    alpha value will be changed - no positional changes; only cylinder's axis change

    if b or B is pressed
    beta value will be changed - no positional changes; only cylinder's axis change

    if x or X is pressed
    x value will be changed; left-to-right positional changes        

    if y or Y is pressed
    z value will be changed; top-to-bottom positional changes

    """
    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()

    if evt.keypress == "a" or evt.keypress == "A": 

        box_loc = box.pos()

        if foc[0] > pos[0] or abs(pos[0] - foc[0]) < distance - 50:

            """
            pos: (x1, y1)
            foc: (x1 - 10, y2)
            """
            foc_new = pos[1] - math.sqrt(distance ** 2 - (20) ** 2)
            plt.at(2).camera.SetFocalPoint([foc[0] - 20, foc_new, foc[2]])

            box.orientation([pos[0] - foc[0] + 20, pos[1] - foc_new, pos[2] - foc[2]])

    elif evt.keypress == "b" or evt.keypress == "B": 

        box_loc = box.pos()


        if foc[2] < pos[2] or abs(pos[2] - foc[2]) < distance - 50:

            """
            pos: (x1, y1)
            foc: (x1 - 10, y2)
            """
            foc_new = pos[1] - math.sqrt(distance ** 2 - (20) ** 2)
            plt.at(2).camera.SetFocalPoint([foc[0], foc_new, foc[2] + 20])

            box.orientation([pos[0] - foc[0], pos[1] - foc_new, pos[2] - foc[2] - 20])

    elif evt.keypress == "y" or evt.keypress == "Y":
        box_loc = box.pos()

        if box_loc [2] + 20 < z1:
            box.z(box_loc[2] + 20)
            plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] + 20])
            plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] + 20])    
    elif evt.keypress == "x" or evt.keypress == "X":
        box_loc = box.pos()

        if box_loc [0] + 20 < x1:
            box.x(box_loc[0] + 20)
            plt.at(2).camera.SetFocalPoint([foc[0] + 20, foc[1], foc[2]])
            plt.at(2).camera.SetPosition([pos[0] + 20, pos[1], pos[2]])    
    loc = box.GetPosition()
    sin_rad_alpha = (pos[0] - foc[0]) / distance
    sin_rad_beta = (pos[2] - foc[2]) / distance

    print(f"({loc[2] - center[2]}, {loc[0] - center[0]}, {loc[1] - center[1]}, {math.asin(sin_rad_alpha)}, {math.asin(sin_rad_beta)})")
    plt.render()
def func_wheelback(evt):

    """
    if a or A is pressed
    alpha value will be changed - no positional changes; only cylinder's axis change

    if b or B is pressed
    beta value will be changed - no positional changes; only cylinder's axis change

    if x or X is pressed
    x value will be changed; left-to-right positional changes        

    if y or Y is pressed
    z value will be changed; top-to-bottom positional changes

    """

    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()

    if evt.keypress == "a" or evt.keypress == "A": 

        box_loc = box.pos()

        if foc[0] < pos[0] or abs(pos[0] - foc[0]) < distance - 50:

            """
            pos: (x1, y1)
            foc: (x1 - 10, y2)
            """
            foc_new = pos[1] - math.sqrt(distance ** 2 - (20) ** 2)
            plt.at(2).camera.SetFocalPoint([foc[0] + 20, foc_new, foc[2]])

            box.orientation([pos[0] - foc[0] - 20, pos[1] - foc_new, pos[2] - foc[2]])

    elif evt.keypress == "b" or evt.keypress == "B": 

        box_loc = box.pos()


        if foc[2] > pos[2] or abs(pos[2] - foc[2]) < distance - 50:

            """
            pos: (x1, y1)
            foc: (x1 - 10, y2)
            """
            foc_new = pos[1] - math.sqrt(distance ** 2 - (20) ** 2)
            plt.at(2).camera.SetFocalPoint([foc[0], foc_new, foc[2] - 20])

            box.orientation([pos[0] - foc[0], pos[1] - foc_new, pos[2] - foc[2] + 20])

    elif evt.keypress == "y" or evt.keypress == "Y":
        box_loc = box.pos()
        if box_loc [2] - 20 > z0:
            box.z(box_loc[2] - 20)
            plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] - 20])
            plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] - 20])    

    elif evt.keypress == "x" or evt.keypress == "X":
        box_loc = box.pos()

        if box_loc [0] - 20 > x0:
            box.x(box_loc[0] - 20)
            plt.at(2).camera.SetFocalPoint([foc[0] - 20, foc[1], foc[2]])
            plt.at(2).camera.SetPosition([pos[0] - 20, pos[1], pos [2]])       

    loc = box.GetPosition()
    sin_rad_alpha = (pos[0] - foc[0]) / distance
    sin_rad_beta = (pos[2] - foc[2]) / distance

    print(f"({loc[2] - center[2]}, {loc[0] - center[0]}, {loc[1] - center[1]}, {math.asin(sin_rad_alpha)}, {math.asin(sin_rad_beta)})")
    plt.render()
shape = [
    dict(bottomleft=(0,0), topright=(1,1), bg='k7'), # the full empty window
    dict(bottomleft=(0.01,0.6), topright=(0.65,0.99), bg='w'), # the display window
    dict(bottomleft=(0.66,0.6), topright=(0.99,0.99), bg='w'), # the display window
    dict(bottomleft=(0.66,0.1), topright=(0.99,0.55), bg='w'), # the display window
]

# disable draging via mouse
settings.renderer_frame_width = 1
settings.enable_default_keyboard_callbacks = False

ct_name = "THIN_ST_TORSO"

ct = Volume(f"{ct_name}.nii.gz")

# get the demension/shape of the ct scans
x0, x1, y0, y1, z0, z1 = ct.bounds()


# center = [(x1 - x0) / 2, (y1 - y0) / 2 , (z1 - z0) / 2]
#cam_high = [(x1 - x0) / 2, (y1 - y0)/1.1, (z1 - z0) / 2]

cam_high = [random.randint(0, x1 // 1),(y1 - y0)/1.1,random.randint(0, z1 // 1)]
center = [cam_high[0],(y1 - y0) / 2, cam_high[2]]
cam_side = [-(x1 - x0), (y1 - y0) * 2, (z1 - z0) / 2]



distance = sqrt((cam_high[0] - center[0]) ** 2 + (cam_high[1] - 0) ** 2 + (cam_high[2] - center[2]) ** 2)
click = False
box = Cylinder(pos = (cam_high[0], cam_high[1], cam_high[2]),
          r = 75,
          height = 20,
          alpha = 1,
           axis = (0, 1, 0) )

# setup plotter
plt = Plotter(shape=shape, sharecam=False, size=(1050, 700))
plt.at(1).show(Assembly([ct,box]),axes= 1, mode = "image")
plt.at(1).look_at("xy")
plt.at(1).camera.Azimuth(270)
plt.at(1).camera.Elevation(45)
plt.at(1).camera.Zoom(1.5)


plt.at(2).look_at("xz").show(ct, roll = 180, mode = "image")

temp_foc = plt.at(2).camera.GetFocalPoint()
temp_pos = plt.at(2).camera.GetPosition()


plt.at(2).camera.SetFocalPoint(center[0], center[1], center[2])
plt.at(2).camera.SetPosition(temp_pos[0], - temp_pos[1], temp_pos[2])
plt.at(2).camera.Zoom(3)


# Add a button to the plotter with buttonfunc as the callback function
bu1 = plt.at(0).add_button(
    buttonfunc_x,
    pos=(0.03, 0.01),   # x,y fraction from bottom left corner
    states=["x", "x"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)
bu2 = plt.at(0).add_button(
    buttonfunc_y,
    pos=(0.07, 0.01),   # x,y fraction from bottom left corner
    states=["y", "y"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)
bu3 = plt.at(0).add_button(
    buttonfunc_z,
    pos=(0.11, 0.01),   # x,y fraction from bottom left corner
    states=["z", "z"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style

)
bu5 = plt.at(0).add_button(
    buttonfunc_r,
    pos=(0.2, 0.01),   # x,y fraction from bottom left corner
    states=["r"],  # text for each state
    c=["w"],     # font color for each state
    bc=["dg"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style

)
bu6 = plt.at(0).add_button(
    buttonfunc_n,
    pos=(0.26, 0.01),   # x,y fraction from bottom left corner
    states=["n", "n"],  # text for each state
    c=["w","w"],     # font color for each state
    bc=["dg","dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style

)
bu7 = plt.at(0).add_button(
    buttonfunc_g,
    pos=(0.32, 0.01),   # x,y fraction from bottom left corner
    states=["g", "g"],  # text for each state
    c=["w"],     # font color for each state
    bc=["dg"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style

)

bu6.switch()
plt.remove_callback('MouseWheelForward')
plt.remove_callback('MouseWheelBackward')
plt.remove_callback('KeyPress')
plt.at(0).remove_callback('KeyPress')
plt.at(1).remove_callback('KeyPress')
plt.at(2).remove_callback('KeyPress')
plt.add_callback('MouseWheelForward',func_wheelfor)
plt.add_callback('MouseWheelBackward',func_wheelback)



plt.interactive().close()