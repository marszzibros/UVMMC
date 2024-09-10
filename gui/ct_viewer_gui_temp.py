from vedo import *
import math

import datetime
import rest_api_write
import threading
from vedo.applications import IsosurfaceBrowser
from generate_deepdrr import Generate 

# initiate deepdrr initiation

g = Generate(sys.argv[1])
g.empty_file()

# initiate parameters
x = datetime.datetime.now()

ct_name = sys.argv[1]
operator = sys.argv[2]
case_name = sys.argv[1].split('/')[1].split('_')[0]

target = 0
order = 1

# Create a timer thread
timer_thread = None
time_pre = 0

# position starts
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
                 "right_hemidiaphragm",
                 "left_hemidiaphragm",
                 "T12", 
                 "L5", 
                 "right_iliac_crest", 
                 "left_iliac_crest",
                 "pubic_symphysis",
                 "right_femoral_head",
                 "left_femoral_head"]


coordinate_to_send = []


def random_start():
    """
    random_start

    descriptions
    ---------------------------------
    start random positions in the ct volume; it is set to randomly initiate from the bottom 1/3
    """

    pass


def buttonfunc_na():
    """
    buttonfunc_na

    descriptions
    ---------------------------------
    Function for na button: it will send the post request and switch to the next task
    """        

    global order
    global coordinate_to_send
    if order < 21:
        order+=1
        coordinate_to_send.append(None)

        if order != 21:
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

def buttonfunc_back():
    """
    buttonfunc_back

    descriptions
    ---------------------------------
    Function for back button: it will send the post request and switch to the back task
    """        
    global order
    global coordinate_to_send
    if order != 1:

        # x, y, z, a, b, position (1-11), ct_name (file name), operator_id, case name
        coordinate_to_send = coordinate_to_send[:-1]

        order -=1
        plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0,zoom=2.2)
        random_start()

def buttonfunc_next():
    """
    buttonfunc_next

    descriptions
    ---------------------------------
    Function for next button: it will send the post request and switch to the next task
    """        
    global order
    global coordinate_to_send
    if order < 21:
        pos = plt.at(2).camera.GetPosition()
        foc = plt.at(2).camera.GetFocalPoint()
        
        global cam_distance

        loc = circle.GetPosition()

        sin_rad_alpha = (pos[0] - foc[0]) / cam_distance
        sin_rad_beta = (pos[2] - foc[2]) / cam_distance



        # x, y, z, a, b, position (1-11), ct_name (file name), operator_id, case name
        coordinate_to_send.append((loc[2] - center[2], loc[0] - center[0], loc[1] - center[1], math.asin(sin_rad_alpha), math.asin(sin_rad_beta), order, ct_name, operator, case_name))

        order+=1
        if order != 21:
            plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0,zoom=2.2)
        random_start()
    
def buttonfunc_finish():
    """
    buttonfunc_finish

    descriptions
    ---------------------------------
    Function for finish button: it will send the post request and switch to the next task
    """       
    global order 
    global coordinate_to_send
    print(order)
    if order == 21:
        for coordinate_order in coordinate_to_send:
            if coordinate_order is not None:
                rest_api_write.send_post(*coordinate_order)
        plt.close()



def func(evt):
    msh = evt.actor
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

ct = Volume(ct_name, mapper="gpu")

ct.cmap("rainbow").alpha([0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.8, 1])
vol_arr = ct.tonumpy()

vol_arrc = np.zeros_like(vol_arr, dtype=np.uint8)
vol_arrc[(vol_arr > 123) & (vol_arr < 3000)] = 1
ct.mask(vol_arrc)
# substitute scalarbar3d to a 2d scalarbar
# get the demension/shape of the ct scans
x0, x1, y0, y1, z0, z1 = ct.bounds()

center = [(x1 - x0) / 2, (y1 - y0) / 2 , (z1 - z0) / 2]
cam_high = [x1 / 2,(y1 - y0)/1.1, z1 * (1 / 4)]
cam_side = [-(x1 - x0), (y1 - y0) * 2, (z1 - z0) / 2]

click = False

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

temp_pos = plt.at(1).camera.GetPosition()

plt.at(1).camera.SetFocalPoint(cam_high[0], center[1], cam_high[2])
plt.at(1).camera.SetPosition(cam_high[0], temp_pos[1], cam_high[2])


plt.at(2).look_at("xz").show(Assembly([ct,circle]), roll = 180, mode = "image")

temp_pos = plt.at(2).camera.GetPosition()

plt.at(2).camera.SetFocalPoint(cam_high[0], center[1], cam_high[2])
plt.at(2).camera.SetPosition(cam_high[0], - temp_pos[1], cam_high[2])
plt.at(3).show(Picture("projector.png"),axes=0, zoom=1.5)

plt.at(4).show(Picture(f"result_text/{position_list[order - 1]}.png"),axes=0, zoom=2.2)

cam_distance = -temp_pos[1] - center[1]

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
    buttonfunc_back,
    pos=(0.40, 0.01),   # x,y fraction from bottom left corner
    states=["back", "back"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)
bu9 =plt.at(0).add_button(
    buttonfunc_next,
    pos=(0.55, 0.01),   # x,y fraction from bottom left corner
    states=["next", "next"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)
bu10 =plt.at(0).add_button(
    buttonfunc_na,
    pos=(0.70, 0.01),   # x,y fraction from bottom left corner
    states=["na", "na"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["dg", "dv"],  # background color for each state
    font="courier",   # font type
    size=20,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
)
bu11 =plt.at(0).add_button(
    buttonfunc_finish,
    pos=(0.85, 0.01),   # x,y fraction from bottom left corner
    states=["finish", "finish"],  # text for each state
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