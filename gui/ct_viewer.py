"""Show a cube for each available color name"""
from operator import itemgetter
from vedo import Cube, Text2D, show, settings
from vedo.colors import colors

# Set immediate rendering to False for faster rendering with multi-renderers
settings.immediate_rendering = False

# Sort the colors by hex color code (matplotlib colors)
sorted_colors1 = sorted(colors.items(), key=itemgetter(1))

print(len(sorted_colors1))
# Create a list of cubes for each color name
cbs=[]
for sc in sorted_colors1:
    # Get the color name
    cname = sc[0]
    # Skip the color if it ends in a number
    if cname[-1] in "123456789":
        continue
    # Create a cube and text object for the color name
    cb = Cube().lw(1).color(cname)
    tname = Text2D(cname, s=0.9)
    # Add the cube and text object to the list
    cbs.append([tname, cb])

print(len(cbs))
# Display the cubes and text objects in a grid
plt1= show(cbs, N=len(cbs), azimuth=.2, size=(2100,1300),
           title="matplotlib colors", interactive=True)