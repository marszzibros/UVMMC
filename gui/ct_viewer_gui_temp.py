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
g = Generate("test_folder/case-100114.nii.gz")
g.empty_file()

# initiate parameters
x = datetime.datetime.now()

ct_name = "test_folder/case-100114.nii.gz"
operator = "s"
case_name = "a"

target = 0
order = 1

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

    circle.x(cam_high_random[0])
    circle.z(cam_high_random[2])

    plt.at(2).reset_camera()
    plt.at(2).look_at("xz").roll(180)

    temp_pos = plt.at(2).camera.GetPosition()

    plt.at(2).camera.SetFocalPoint(cam_high_random[0], center[1], cam_high_random[2])
    plt.at(2).camera.SetPosition(cam_high_random[0], - temp_pos[1], cam_high_random[2])
    plt.at(2).camera.Zoom(2.8)    

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

def buttonfunc_na():
    """
    buttonfunc_na

    descriptions
    ---------------------------------
    Function for na button: it will send the post request and switch to the next task
    """        

    global order

    order+=1
    plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0,zoom=2.2)
    random_start()
def buttonfunc_g():
    """
    buttonfunc_g

    descriptions
    ---------------------------------
    Function for g button
    """    
    global cam_distance

    loc = circle.GetPosition()
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
    
# def move(evt):
    
#     """
#     move
    
#     descriptions
#     ---------------------------------
#     functions for mouse movement

#     if a or A is pressed
#     alpha value will be changed - no positional changes; only cylinder's axis change

#     if b or B is pressed
#     beta value will be changed - no positional changes; only cylinder's axis change

#     if x or X is pressed
#     x value will be changed; left-to-right positional changes        

#     if y or Y is pressed
#     z value will be changed; top-to-bottom positional changes

#     args
#     ---------------------------------
#     evt: vtk object
#         contains mouse info
#     """

#     pos = plt.at(2).camera.GetPosition()
#     foc = plt.at(2).camera.GetFocalPoint()
    
#     global pressed
#     global cam_distance
#     global cyl_distance
#     global time_pre

#     # if not moved more than 0.5 secs and less than 3 secs, generate deepDRR 
#     if not pressed and time_pre == 0:
#         time_pre = time.time()
#     elif not pressed and time.time() - time_pre >= 3:
#         pass
#     elif not pressed and time.time() - time_pre >= 0.5:
#         buttonfunc_g()

    
#     box_loc = box.pos()

#     if pressed:
#         time_pre = 0

#     # x value will be changed; left-to-right positional changes        
#     if pressed and button_key == "left" and abs(evt.delta2d[0]) > abs(evt.delta2d[1]):
        
#         if evt.delta2d[0] > 0:

#             if box_loc [2] + 10 < z1:
#                 box.z(box_loc[2] + 10)
#                 circle.z(box_loc[2] + 10)
#                 plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] + 10])
#                 plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] + 10])
#                 moved=True
#         else:
    
#             if box_loc [2] - 10 > z0:
#                 box.z(box_loc[2] - 10)
#                 circle.z(box_loc[2] - 10)
#                 plt.at(2).camera.SetFocalPoint([foc[0], foc[1], foc[2] - 10])
#                 plt.at(2).camera.SetPosition([pos[0], pos[1], pos [2] - 10])        
#                 moved=True
                
#     # z value will be changed; top-to-bottom positional changes
#     elif pressed and button_key == "left" and abs(evt.delta2d[0]) < abs(evt.delta2d[1]):

#         if evt.delta2d[1] > 0:
#             if box_loc [0] + 10 < x1:
#                 box.x(box_loc[0] + 10)
#                 circle.x(box_loc[0] + 10)
#                 plt.at(2).camera.SetFocalPoint([foc[0] + 10, foc[1], foc[2]])
#                 plt.at(2).camera.SetPosition([pos[0] + 10, pos[1], pos[2]])    
#                 moved=True
            
#         else:
#             if box_loc [0] - 10 > x0:
#                 box.x(box_loc[0] - 10)
#                 circle.x(box_loc[0] - 10)
#                 plt.at(2).camera.SetFocalPoint([foc[0] - 10, foc[1], foc[2]])
#                 plt.at(2).camera.SetPosition([pos[0] - 10, pos[1], pos [2]])
#                 moved=True       
        
#     loc = box.GetPosition()
#     plt.render()
def func(evt):                       ### called every time mouse moves!
    msh = evt.actor                 # get the mesh that triggered the event
    event_at = evt.at
    if msh and event_at == 1:
    
        pos1 = plt.at(1).camera.GetPosition()
        foc1 = plt.at(1).camera.GetFocalPoint()

        pos2 = plt.at(2).camera.GetPosition()
        foc2 = plt.at(2).camera.GetFocalPoint()

        cood = evt.picked3d

        circle.x(cood[0])
        circle.z(cood[2])

        plt.at(1).camera.SetFocalPoint([cood[0], foc1[1], cood[2]])
        plt.at(1).camera.SetPosition([cood[0], pos1[1], cood[2]])

        plt.at(2).camera.SetFocalPoint([cood[0], foc2[1], cood[2]])
        plt.at(2).camera.SetPosition([cood[0], pos2[1], cood[2]])

        plt.render()

        buttonfunc_g()
    if msh and event_at == 3:
        cood = evt.picked3d

        pos1 = plt.at(1).camera.GetPosition()
        foc1 = plt.at(1).camera.GetFocalPoint()

        pos2 = plt.at(2).camera.GetPosition()
        foc2 = plt.at(2).camera.GetFocalPoint()

        circle_cood = circle.GetCenter()

        x_d = (cood[0] - (1536 / 2)) / (1536 * 3) * (y1 - y0)
        y_d = (cood[1] - (1536 / 2)) / (1536 * 3) * (y1 - y0)

        circle.x(circle_cood[0] + x_d)
        circle.z(circle_cood[2] - y_d)

        plt.at(1).camera.SetFocalPoint([circle_cood[0] + x_d, foc1[1], circle_cood[2] - y_d])
        plt.at(1).camera.SetPosition([circle_cood[0] + x_d, pos1[1], circle_cood[2] - y_d])

        plt.at(2).camera.SetFocalPoint([circle_cood[0] + x_d, foc2[1], circle_cood[2] - y_d])
        plt.at(2).camera.SetPosition([circle_cood[0] + x_d, pos2[1], circle_cood[2] - y_d])

        plt.render()

        buttonfunc_g()

# disable draging via mouse
settings.renderer_frame_width = 1
settings.enable_default_keyboard_callbacks = False

ct = Volume(ct_name)

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
circle = Cylinder(pos = (cam_high[0], cam_high[1] / 1.39, cam_high[2]),
          r = 10,
          height = 20,
          alpha = 1,
           axis = (0, 1, 0), c='red')

shape = [
    dict(bottomleft=(0,0), topright=(1,1), bg='k7'), # the full empty window
    dict(bottomleft=(0.01,0.5), topright=(0.65,0.93), bg='w'), # ct with box
    dict(bottomleft=(0.66,0.5), topright=(0.99,0.93), bg='w'), # ct x-ray view
    dict(bottomleft=(0.66,0.1), topright=(0.99,0.43), bg='w'), # x-ray view
    dict(bottomleft=(0.01,0.1), topright=(0.65,0.43), bg='w'), # instructions
]

# setup plotter
plt = Plotter(shape=shape, sharecam=False, size=(1050, 700))

plt.at(1).show(Assembly([ct,circle]),axes= 1, mode = "image")
plt.at(1).look_at("xz")
plt.at(1).camera.Azimuth(180)
plt.at(1).roll(180)
plt.at(1).camera.Zoom(6)

plt.at(2).look_at("xz").show(Assembly([ct,circle]), roll = 180, mode = "image")

temp_pos = plt.at(2).camera.GetPosition()

plt.at(2).camera.SetFocalPoint(cam_high[0], center[1], cam_high[2])
plt.at(2).camera.SetPosition(cam_high[0], - temp_pos[1], cam_high[2])
plt.at(3).show(Picture("projector.png"),axes=0, zoom=1.5)

plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0, zoom=2.2)

cam_distance = -temp_pos[1] - center[1]
cyl_distance = box.pos()[1] - center[1]

plt.at(2).camera.Zoom(2.8)    

# Add a button to the plotter with buttonfunc as the callback function
bu7 = plt.at(0).add_button(
    buttonfunc_g,
    pos=(0.03, 0.01),   # x,y fraction from bottom left corner
    states=["g", "g"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
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
bu9 =plt.at(0).add_button(
    buttonfunc_na,
    pos=(0.55, 0.01),   # x,y fraction from bottom left corner
    states=["na", "na"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)
plt.add_callback('mouse click', func) # add the callback function
plt.at(3).remove_callback('mouse wheel')
plt.interactive().close()