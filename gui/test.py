from vedo import *
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

def move(evt):
    global pressed
    if pressed and button_key == "left":
        print(evt.delta2d)
        cone.rotate_z(evt.angle2d)
        plt.render()

# ...or, in a non-blocking fashion:
listener = mouse.Listener(
    on_click=on_click)
listener.start()

mode = interactor_modes.BlenderStyle()

plt = Plotter()

plt.remove_callback("mouse move")
plt.remove_callback("keyboard")

plt.add_callback("mouse move", move)

cone = Cone().rotateY(90)
disc = Disc(r2=0.8).scale(5).lighting('off')
plt.show(cone, disc, axes=3)
