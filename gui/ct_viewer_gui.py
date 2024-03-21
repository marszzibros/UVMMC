from vedo import *
import math
from pynput import mouse
import random
import datetime
import rest_api_write
import threading
import sys
import time
from generate_deepdrr import Generate 

# initiate deepdrr initiation
g = Generate(sys.argv[1])
g.empty_file()

# initiate parameters
x = datetime.datetime.now()

ct_name = sys.argv[1].split('/')[-1][:-7]
operator = sys.argv[2]
case_name = sys.argv[1]

target = 0
order = 1

# mouse global variables
pressed = None
button_key = None

# Create a timer thread
timer_thread = None
time_pre = 0

# position starts
position_list = ["skull", "right_humeral_head", "left_humeral_head", "right_capula", "left_scapula", "T1", "carina", "T12", "L5", "right_iliac_crest", "left_iliac_crest"]


def random_start():
    """
    random_start

    descriptions
    ---------------------------------
    start random positions in the ct volume; it is set to randomly initiate from the bottom 1/3
    """

    # initiate camera and box locations
    cam_high_random = [random.randint(0, x1 // 1),(y1 - y0)/1.1,random.randint(z1 * 2 // 3, z1 // 1)]

    box.x(cam_high_random[0])
    box.z(cam_high_random[2])

    plt.at(2).reset_camera()
    plt.at(2).look_at("xz").roll(180)

    temp_pos = plt.at(2).camera.GetPosition()

    plt.at(2).camera.SetFocalPoint(cam_high_random[0], center[1], cam_high_random[2])
    plt.at(2).camera.SetPosition(cam_high_random[0], - temp_pos[1], cam_high_random[2])
    plt.at(2).camera.Zoom(3.5)    

    plt.render()

def send_post_threaded(*args):
    """
    send_post_threaded

    descriptions
    ---------------------------------
    background work for database POST method
    """    

    # Define a function to be executed in a separate thread
    def send_post_task():
        """
        request POST method 
        """
        rest_api_write.send_post(*args)

    # Create a new thread and start it
    thread = threading.Thread(target=send_post_task)
    thread.start()

def on_click(x, y, button, pressed_key):
    """
    on_click

    descriptions
    ---------------------------------
    mouse listener when clicked

    args
    ---------------------------------
    x: float
        x coordinate of the mouse
    y: float
        y coordinate of the mouse
    button: bool
        True/False whether the button is clicked
    pressed_key: mouse object
        left/right
    """
    global pressed
    pressed = pressed_key

    global button_key
    if button == mouse.Button.left:
        button_key = "left"
    elif button == mouse.Button.right:
        button_key = "right"

def buttonfunc_x():
    """
    buttonfunc_x

    descriptions
    ---------------------------------
    Function for x button
    """
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

def buttonfunc_y():
    """
    buttonfunc_y

    descriptions
    ---------------------------------
    Function for y button
    """

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

def buttonfunc_z():
    """
    buttonfunc_z

    descriptions
    ---------------------------------
    Function for z button
    """

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

def buttonfunc_n():
    """
    buttonfunc_n

    descriptions
    ---------------------------------
    Function for n button
    it will turns into surgeon view of patients
    """    
    if bu6.status_idx == 0:
        bu6.switch()
        plt.at(1).reset_camera()
        plt.at(1).look_at("xy")
        plt.at(1).camera.Azimuth(45)
        plt.at(1).camera.Elevation(45)
        plt.at(1).camera.Zoom(1.5)

def buttonfunc_r():
    """
    buttonfunc_r

    descriptions
    ---------------------------------
    Function for r button: rotate camera view
    """    
    if bu6.status_idx == 0:
        plt.at(1).roll(90)
    else:
        plt.at(1).camera.Azimuth(45)

def buttonfunc_g():
    """
    buttonfunc_g

    descriptions
    ---------------------------------
    Function for g button
    """    
    global cam_distance

    loc = box.GetPosition()
    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()

    sin_rad_alpha = (pos[0] - foc[0]) / cam_distance
    sin_rad_beta = (pos[2] - foc[2]) / cam_distance
    
    g.deepdrr_run(loc[2] - center[2], loc[0] - center[0],loc[1] - center[1], math.asin(sin_rad_alpha),math.asin(sin_rad_beta))
    plt.at(3).show(Picture("projector.png"),axes=0, zoom=1.5)

def buttonfunc_finish():
    """
    buttonfunc_finish

    descriptions
    ---------------------------------
    Function for finish button: it will send the post request and switch to the next task
    """        
    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()
    
    global cam_distance

    loc = box.GetPosition()

    sin_rad_alpha = (pos[0] - foc[0]) / cam_distance
    sin_rad_beta = (pos[2] - foc[2]) / cam_distance

    global order

    # x, y, z, a, b, position (1-11), ct_name (file name), operator_id, case name
    send_post_threaded(loc[2] - center[2], loc[0] - center[0], loc[1] - center[1], math.asin(sin_rad_alpha), math.asin(sin_rad_beta), order, ct_name, operator, case_name)
    order+=1
    plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0,zoom=2.2)
    random_start()
    
def move(evt):
    
    """
    move
    
    descriptions
    ---------------------------------
    functions for mouse movement

    if a or A is pressed
    alpha value will be changed - no positional changes; only cylinder's axis change

    if b or B is pressed
    beta value will be changed - no positional changes; only cylinder's axis change

    if x or X is pressed
    x value will be changed; left-to-right positional changes        

    if y or Y is pressed
    z value will be changed; top-to-bottom positional changes

    args
    ---------------------------------
    evt: vtk object
        contains mouse info
    """

    pos = plt.at(2).camera.GetPosition()
    foc = plt.at(2).camera.GetFocalPoint()
    
    global pressed
    global cam_distance
    global cyl_distance
    global time_pre

    # if not moved more than 0.5 secs and less than 3 secs, generate deepDRR 
    if not pressed and time_pre == 0:
        time_pre = time.time()
    elif not pressed and time.time() - time_pre >= 3:
        pass
    elif not pressed and time.time() - time_pre >= 0.5:
        buttonfunc_g()

    
    box_loc = box.pos()

    if pressed:
        time_pre = 0

    # x value will be changed; left-to-right positional changes        
    if pressed and button_key == "left" and abs(evt.delta2d[0]) > abs(evt.delta2d[1]):
        
        if evt.delta2d[0] > 0:

            if box_loc [2] + 10 < z1:
                box.z(box_loc[2] + 10)
                plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] + 10])
                plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] + 10])
                moved=True
        else:
    
            if box_loc [2] - 10 > z0:
                box.z(box_loc[2] - 10)
                plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] - 10])
                plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] - 10])        
                moved=True
                
    # z value will be changed; top-to-bottom positional changes
    elif pressed and button_key == "left" and abs(evt.delta2d[0]) < abs(evt.delta2d[1]):

        if evt.delta2d[1] > 0:
            if box_loc [0] + 10 < x1:
                box.x(box_loc[0] + 10)
                plt.at(2).camera.SetFocalPoint([foc[0] + 10, foc[1], foc[2]])
                plt.at(2).camera.SetPosition([pos[0] + 10, pos[1], pos[2]])    
                moved=True
            
        else:
            if box_loc [0] - 10 > x0:
                box.x(box_loc[0] - 10)
                plt.at(2).camera.SetFocalPoint([foc[0] - 10, foc[1], foc[2]])
                plt.at(2).camera.SetPosition([pos[0] - 10, pos[1], pos [2]])
                moved=True       
        
    loc = box.GetPosition()
    plt.render()

# mouse listener
listener = mouse.Listener( 
    on_click=on_click,)
listener.start()

# disable draging via mouse
settings.renderer_frame_width = 1
settings.enable_default_keyboard_callbacks = False

ct = Volume(sys.argv[1])

# get the demension/shape of the ct scans
x0, x1, y0, y1, z0, z1 = ct.bounds()

center = [(x1 - x0) / 2, (y1 - y0) / 2 , (z1 - z0) / 2]
cam_high = [random.randint(0, x1 // 1),(y1 - y0)/1.1,random.randint(z1 * 2 // 3, z1 // 1)]
cam_side = [-(x1 - x0), (y1 - y0) * 2, (z1 - z0) / 2]

click = False
box = Cylinder(pos = (cam_high[0], cam_high[1], cam_high[2]),
          r = 75,
          height = 20,
          alpha = 1,
           axis = (0, 1, 0) )

shape = [
    dict(bottomleft=(0,0), topright=(1,1), bg='k7'), # the full empty window
    dict(bottomleft=(0.01,0.6), topright=(0.65,0.99), bg='w'), # ct with box
    dict(bottomleft=(0.66,0.6), topright=(0.99,0.99), bg='w'), # ct x-ray view
    dict(bottomleft=(0.66,0.1), topright=(0.99,0.55), bg='w'), # x-ray view
    dict(bottomleft=(0.01,0.1), topright=(0.65,0.55), bg='w'), # instructions
]

# setup plotter
plt = Plotter(shape=shape, sharecam=False, size=(1050, 700))

plt.at(1).show(Assembly([ct,box]),axes= 1, mode = "image")
plt.at(1).look_at("xy")
plt.at(1).camera.Azimuth(270)
plt.at(1).camera.Elevation(45)
plt.at(1).camera.Zoom(1.5)

plt.at(2).look_at("xz").show(ct, roll = 180, mode = "image")

temp_pos = plt.at(2).camera.GetPosition()

plt.at(2).camera.SetFocalPoint(cam_high[0], center[1], cam_high[2])
plt.at(2).camera.SetPosition(cam_high[0], - temp_pos[1], cam_high[2])
plt.at(3).show(Picture("projector.png"),axes=0, zoom=1.5)

plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0, zoom=2.2)

cam_distance = -temp_pos[1] - center[1]
cyl_distance = box.pos()[1] - center[1]

plt.at(2).camera.Zoom(3.5)    

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
bu8 =plt.at(0).add_button(
    buttonfunc_finish,
    pos=(0.40, 0.01),   # x,y fraction from bottom left corner
    states=["Finish", "Finish"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)

plt.remove_callback("mouse move")
plt.remove_callback("keyboard")
plt.remove_callback("MouseWheelForward")
plt.remove_callback("MouseWheelBackward")

plt.add_callback("mouse move", move)

bu6.switch()

plt.interactive().close()