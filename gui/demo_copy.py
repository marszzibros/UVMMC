from vedo import *
import os
import math
from pynput import mouse


pressed = None
button_key = None

def on_click(x, y, button, pressed_key):
    global pressed
    pressed = pressed_key
    
    global button_key
    if button == mouse.Button.left:
        button_key = "left"
    elif button == mouse.Button.right:
        button_key = "right"

listener = mouse.Listener(
    on_click=on_click)
listener.start()


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

    global cam_distance

    loc = box.GetPosition()
    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()

    sin_rad_alpha = (pos[0] - foc[0]) / cam_distance
    sin_rad_beta = (pos[2] - foc[2]) / cam_distance

    os.system(f"python example_projector.py {ct_name} {loc[2] - center[2]} {loc[0] - center[0]} {loc[1] - center[1]} {math.asin(sin_rad_alpha)} {math.asin(sin_rad_beta)}")
    plt.at(3).show(Picture("example_projector.png"),axes=0, zoom=1.5)


def move(evt):

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
    
    global pressed
    global cam_distance
    global cyl_distance

    box_loc = box.pos()

    print(box_loc)
    
    if pressed and button_key == "left" and abs(evt.delta2d[0]) < abs(evt.delta2d[1]):

        if evt.delta2d[1] > 0:

            if box_loc [2] - 10 < z1:
                box.z(box_loc[2] - 10)
                plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] - 10])
                plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] - 10])
        else:
    
            if box_loc [2] + 10 > z0:
                box.z(box_loc[2] + 10)
                plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] + 10])
                plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] + 10])        
                
            
    elif pressed and button_key == "left" and abs(evt.delta2d[0]) > abs(evt.delta2d[1]):

        if evt.delta2d[0] > 0:
            if box_loc [0] + 10 < x1:
                box.x(box_loc[0] + 10)
                plt.at(2).camera.SetFocalPoint([foc[0] + 10, foc[1], foc[2]])
                plt.at(2).camera.SetPosition([pos[0] + 10, pos[1], pos[2]])    
            
        else:
            if box_loc [0] - 10 > x0:
                box.x(box_loc[0] - 10)
                plt.at(2).camera.SetFocalPoint([foc[0] - 10, foc[1], foc[2]])
                plt.at(2).camera.SetPosition([pos[0] - 10, pos[1], pos [2]])       
    
    elif pressed and button_key == "right" and abs(evt.delta2d[0]) > abs(evt.delta2d[1]):

        a_box_x = box_loc[0] - foc[0]

        # direction check
        if evt.delta2d[0] > 0 and (pos[0] - foc[0]) / cam_distance < 0.2:
            a_box_x = box_loc[0] - foc[0] + 5
        elif evt.delta2d[0] < 0 and (pos[0] - foc[0]) / cam_distance > -0.2:
            a_box_x = box_loc[0] - foc[0] - 5

        # cylinder calculation
        a_box_y = foc[1] + math.sqrt(cyl_distance ** 2 - a_box_x ** 2)

        box.x(a_box_x + foc[0])
        box.y(a_box_y)

        # camera calculation
        cos_tri = a_box_x / a_box_y
        a_cam_x = cos_tri * cam_distance
        a_cam_y = foc[1] + math.sqrt(cam_distance ** 2 - a_cam_x ** 2)

        plt.at(2).camera.SetPosition([a_cam_x + foc[0], a_cam_y, pos[2]])       
        pos = [a_cam_x + foc[0], a_cam_y, pos[2]]

        box.orientation([pos[0] - foc[0], pos[1] - foc[1], pos[2] - foc[2]])

    elif pressed and button_key == "right" and abs(evt.delta2d[0]) < abs(evt.delta2d[1]):

        a_box_z = box_loc[2] - foc[2]

        # direction check
        if evt.delta2d[1] > 0 and (pos[2] - foc[2]) / cam_distance < 0.2:
            a_box_z = a_box_z + 5
        elif evt.delta2d[1] < 0 and (pos[2] - foc[2]) / cam_distance > -0.2:
            a_box_z = a_box_z - 5

        # cylinder calculation
        a_box_y = foc[1] + math.sqrt(cyl_distance ** 2 - a_box_z ** 2)

        box.z(a_box_z + foc[2])
        box.y(a_box_y)

        # camera calculation
        cos_tri = a_box_z / a_box_y
        a_cam_z = cos_tri * cam_distance
        a_cam_y = foc[1] + math.sqrt(cam_distance ** 2 - a_cam_z ** 2)

        plt.at(2).camera.SetPosition([pos[0], a_cam_y, a_cam_z + foc[2]])       
        pos = [pos[0], a_cam_y, a_cam_z + foc[2]]

        box.orientation([pos[0] - foc[0], pos[1] - foc[1], pos[2] - foc[2]])
    loc = box.GetPosition()

    sin_rad_alpha = (pos[0] - foc[0]) / cam_distance
    sin_rad_beta = (pos[2] - foc[2]) / cam_distance

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

center = [(x1 - x0) / 2, (y1 - y0) / 2 , (z1 - z0) / 2]
cam_high = [(x1 - x0) / 2, (y1 - y0)/1.1, (z1 - z0) / 2]
cam_side = [-(x1 - x0), (y1 - y0) * 2, (z1 - z0) / 2]

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

plt.at(1).camera.Zoom(1.5)

plt.at(2).look_at("xz").show(ct, roll = 180, mode = "image")

temp_pos = plt.at(2).camera.GetPosition()

plt.at(2).camera.SetFocalPoint(center[0], center[1], center[2])
plt.at(2).camera.SetPosition(center[0], - temp_pos[1], center[2])

cam_distance = -temp_pos[1] - center[1]
cyl_distance = box.pos()[1] - center[1]


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
    c=["w"],     # font color for each state
    bc=["dg"],  # background color for each state
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

plt.remove_callback("mouse move")
plt.remove_callback("keyboard")

plt.add_callback("mouse move", move)


bu3.switch()



plt.interactive().close()