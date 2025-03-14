import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mayavi import mlab

from utils.themes import *
from utils.functions import *

# -------------------------- DEFINE SETTINGS ----------------------------
SIZE_SCALE_FACTOR = 0.9
WIDTH = 16 * SIZE_SCALE_FACTOR  # inches
HEIGHT = 9 * SIZE_SCALE_FACTOR  # inches

scene_frames_dict = {0: 0}
FRAMES_SCALE_FACTOR = 0.05
FRAME_RATE = 60
INTERVAL = int(1000 / FRAME_RATE)

CHANGING_ELEMENTS = []

# Enable offscreen rendering for Mayavi to prevent a separate window from opening
mlab.options.offscreen = True

def update_frames_dict(key, frames):
    scene_frames_dict[key] = scene_frames_dict[key - 1] + frames

def add_changing_elements(*args):
    for element in args:
        CHANGING_ELEMENTS.append(element)

def capture_mayavi_scene_to_image():
    fig = mlab.gcf()
    mlab.draw()
    image_array = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
    return image_array

# --------------------- DEFINE FIGURE AND SUBPLOTS ----------------------
fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
apply_theme_to_figure(fig)
apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)

# --------------------------- DATA AND SCENES ---------------------------

# Scene 1: Create Line (Mayavi 3D Plot)
num_frames = int(1000 * FRAMES_SCALE_FACTOR)
update_frames_dict(1, num_frames)

x1 = np.linspace(0, 9, num_frames)
y1 = deepcopy(x1)
z1 = np.zeros_like(x1)

# Create Mayavi figure with black background
mlab.figure(bgcolor=(0, 0, 0), size=(640, 480))

# Initialize the plot with at least two points
line_plot = mlab.plot3d(x1[:2], y1[:2], z1[:2], color=(0, 0, 1), tube_radius=0.1)

# Set axes once and don't change them in each frame
axes_obj = mlab.axes(xlabel='X', ylabel='Y', zlabel='Z', color=(1, 1, 1))
axes_obj.axes.bounds = (0, 10, 0, 10, -1, 1)  # Set axis limits once
axes_obj.label_text_property.color = (1, 1, 1)  # Set axis label color to white
axes_obj.axes.x_axis_visibility = True
axes_obj.axes.y_axis_visibility = True
axes_obj.axes.z_axis_visibility = True
axes_obj.axes.axis_label_text_property.color = (1, 1, 1)
axes_obj.axes.axis_title_text_property.color = (1, 1, 1)

# Set the view to zoom out
mlab.view(azimuth=45, elevation=50, distance=30, focalpoint=(5, 5, 0))

# Capture the initial scene as an image
scene1_image = capture_mayavi_scene_to_image()
scene1_line = axes[0].imshow(scene1_image, aspect='auto')
scene1_text = axes[1].text(0.5, 0.5, "", color="white", ha='center', va='center')

add_changing_elements(scene1_line, scene1_text)

# ---------------------- DEFINING UPDATE FUNCTION -----------------------
def update(frame):
    # Update Scene 1
    if frame < scene_frames_dict[1]:
        scene_frame = frame - scene_frames_dict[0]

        line_plot.mlab_source.set(x=[x1[0], x1[scene_frame]], y=[y1[0], y1[scene_frame]], z=[z1[0], z1[scene_frame]])

        # Capture the updated Mayavi plot as an image
        image = capture_mayavi_scene_to_image()
        scene1_line.set_data(image)  # Update subplot image

        # Update the text
        scene1_text.set_text(f"x = {x1[scene_frame - 1]:.2f}, y = {y1[scene_frame - 1]:.2f}")

        fig.canvas.draw()

    # Always return all lines or plots
    return tuple(CHANGING_ELEMENTS)

# ---------------------- DEFINING ANIMATION FUNCTION -----------------------
anim = FuncAnimation(fig=fig,
                     func=update,
                     frames=list(scene_frames_dict.values())[-1],
                     interval=INTERVAL,
                     blit=True,
                     repeat=False)

# Show the animation in a window
plt.show()
# Uncomment the following line to save the animation
# anim.save("animation.mp4", writer="ffmpeg", fps=FRAME_RATE)