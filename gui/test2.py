"""Create a simple Play/Pause app with a timer event
You can interact with the scene during the loop!
..press q to quit"""
import vedo
from pynput import mouse

pressed = False

def on_click(x, y, button, pressed_key):
    global pressed
    pressed = pressed_key
    print(pressed_key)

    global button_key
    if button == mouse.Button.left:
        button_key = "left"
    elif button == mouse.Button.right:
        button_key = "right"

listener = mouse.Listener(
    on_click=on_click)
listener.start()

def buttonfunc():
    global timerId
    plotter.timer_callback("destroy", timerId)
    if pressed:
        # instruct to call handle_timer() every 10 msec:
        timerId = plotter.timer_callback("create", dt=10)
    button.switch()

def handle_timer(event):
    ### Animate your stuff here ######################################
    earth.rotateZ(1)            # rotate the Earth by 1 deg
    plotter.render()


plotter = vedo.Plotter()

timerId = None
button = plotter.add_button(buttonfunc, states=[" Play ","Pause"], size=40)
evntId = plotter.add_callback("timer", handle_timer)

earth = vedo.Earth()

plotter.show(earth, __doc__, axes=1, bg2='b9', viewup='z').close()