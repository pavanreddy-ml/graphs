import os
import numpy as np
from copy import deepcopy

from utils.themes import *
from utils.functions import *
from utils.numpy_utils import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from IPython.display import HTML

# -------------------------- DEFINE SETTINGS ----------------------------
SIZE_SCALE_FACTOR = 0.4
WIDTH = 16 * SIZE_SCALE_FACTOR  # inches
HEIGHT = 9 * SIZE_SCALE_FACTOR  # inches

scene_frames_dict = {0: 0}
FRAMES_SCALE_FACTOR = 0.4
FRAME_RATE = 60
INTERVAL = int(1000 / FRAME_RATE)

CHANGING_ELEMENTS = []


def update_frames_dict(key, frames):
    scene_frames_dict[key] = scene_frames_dict[key - 1] + frames


def add_changing_elements(*args):
    for element in args:
        CHANGING_ELEMENTS.append(element)


# --------------------- DEFINE FIGURE AND SUBPLOTS ----------------------
fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
apply_theme_to_figure(fig)
apply_theme_to_subplot(axes[0], **{"xlim": [0, 10], "ylim": [0, 10]})
apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)

# --------------------------- DATA AND SCENES ---------------------------

# Scene 1: Create Line
num_frames = int(1000 * FRAMES_SCALE_FACTOR)
update_frames_dict(1, num_frames)
x1 = ease_in_out(np.linspace(0, 9, num_frames))
y1 = deepcopy(x1)
scene1_line, = axes[0].plot([], [], color="blue")
scene1_text = axes[1].text(5, 5, r"$\mathbf{x = 0 \quad y = 0}$", color="white")
add_changing_elements(scene1_line, scene1_text)

# Scene 2; Move Lines based on Slope and intecept
num_frames = int(1000 * FRAMES_SCALE_FACTOR)
update_frames_dict(2, num_frames)
slopes = [(1, 2), (2, 3), (3, 1)]
intercepts = [(0.5, 0.3), (0.3, 0.7), (0.7, 0.5)]
x2 = [0, 10]
intercepts_array = extend_array_to_num_frames(num_frames,
                                              np.concatenate([ease_in_out(
                                                  np.linspace(*(start, end), int(num_frames / len(intercepts)))) for
                                                              start, end in intercepts]))
slopes_array = extend_array_to_num_frames(num_frames,
                                          np.concatenate(
                                              [ease_in_out(np.linspace(*(start, end), int(num_frames / len(slopes))))
                                               for start, end in slopes]))
y2 = np.vstack([slopes_array * x2[0] + intercepts_array, slopes_array * x2[1] + intercepts_array]).T
scene2_line, = axes[0].plot([], [], color="green")
scene2_text = axes[1].text(10, 10, r"$\mathbf{y = mx + c}$", color="white")
add_changing_elements(scene2_line, scene2_text)


# Scene 3: Add points Fade In
lag_ratio = 0.6
num_frames_per_point = int(100 * FRAMES_SCALE_FACTOR)
num_points = 100
independent_frames_per_point = num_frames_per_point - int(lag_ratio * num_frames_per_point)
num_frames = (independent_frames_per_point * (num_points - 1)) + num_frames_per_point
opacity_array = ease_in_out(np.linspace(0, 1, num_frames_per_point))
point_size3 = 4
animate3 = 'size'           # 'size', 'opacity', 'both'
# opacity_array = np.ones(0, 1, num_frames_per_point)
update_frames_dict(3, num_frames)
x3 = np.random.uniform(0, 10, num_points)
y3 = np.random.uniform(0, 10, num_points)
scene3_scatter = axes[0].scatter(x3, y3, color='red',
                                 alpha=1 if animate3 == 'size' else 0,
                                 s=1 if animate3 == 'opacity' else 0)
add_changing_elements(scene3_scatter)
print(len(opacity_array))

print(scene_frames_dict)

# ---------------------- DEFINING UPDATE FUNCTION -----------------------
def update(frame):
    # Update Scene 1
    if frame < scene_frames_dict[1]:
        scene_frame = frame - scene_frames_dict[0]
        scene1_line.set_data(x1[:scene_frame], y1[:scene_frame])
        scene1_text.set_text(rf"$\mathbf{{x = {x1[scene_frame]:.2f} \quad y = {y1[scene_frame]:.2f}}}$")

    # Update Scene 2
    elif scene_frames_dict[1] <= frame < scene_frames_dict[2]:
        scene_frame = frame - scene_frames_dict[1]
        scene2_line.set_data(x2, y2[scene_frame])
        scene2_text.set_text(
            rf"$\mathbf{{y = {intercepts_array[scene_frame]:.2f}x + {slopes_array[scene_frame]:.2f}}}$")

    elif scene_frames_dict[2] <= frame < scene_frames_dict[3]:
        scene_frame = frame - scene_frames_dict[2]
        points_opacity = np.zeros_like(x3)
        for point_idx in range(len(x3)):
            start_frame = point_idx * int((1-lag_ratio) * num_frames_per_point)
            if scene_frame >= start_frame:
                frame_offset = scene_frame - start_frame
                if frame_offset < num_frames_per_point:
                    points_opacity[point_idx] = opacity_array[frame_offset]
                else:
                    points_opacity[point_idx] = 1.0  # Fully visible after full fade-in

        true_size = np.clip(points_opacity, 0, 1) * point_size3
        true_opacity = np.clip(points_opacity, 0, 1)
        if animate3 == 'size':
            scene3_scatter.set_sizes(true_size)
        elif animate3 == 'opacity':
            scene3_scatter.set_alpha(true_opacity)
        elif animate3 == 'both':
            scene3_scatter.set_sizes(true_size)
            scene3_scatter.set_alpha(true_opacity)
        else:
            raise ValueError(f"Invalid value for animate3: {animate3}")


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
# anim.save("animation.mp4", writer="ffmpeg", fps=FRAME_RATE)
