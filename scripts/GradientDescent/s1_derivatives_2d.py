import os
import io
import shutil
import ffmpeg
import imageio
import subprocess
import numpy as np
from tqdm import tqdm
from copy import deepcopy

from utils.themes import *
from utils.functions import *
from utils.string_utils import *
from utils.numpy_utils import *

import matplotlib.pyplot as plt



np.random.seed(42)
# -------------------------- DEFINE SETTINGS ----------------------------
SIZE_SCALE_FACTOR = 1
WIDTH = 20 * SIZE_SCALE_FACTOR  # inches
HEIGHT = 10 * SIZE_SCALE_FACTOR  # inches
DPI = 200

INIT = True
PROJECT_FILE_NAME = "s1_derivatives_2d"
SAVE_FILE = True

figures = []

def plot(save_file=SAVE_FILE):
    global figures

    if save_file:
        fig = plt.gcf()
        fig.tight_layout()
        plt.draw()
        canvas = plt.gca().figure.canvas
        canvas.draw()
        data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
        data = data.reshape(canvas.get_width_height()[::-1] + (4,))
        figures.append(data)
    else:
        fig = plt.gcf()
        fig.tight_layout()
        plt.show(block=True)


def create_video_and_cleanup(save_prefix=""):
    global figures, INIT
    video_dir = os.path.join("media", PROJECT_FILE_NAME)
    if INIT and os.path.exists(video_dir):
        shutil.rmtree(video_dir)
        INIT = False
    os.makedirs(video_dir, exist_ok=True)
    video_save_path = os.path.join(video_dir, save_prefix + ".mp4")
    imageio.mimsave(video_save_path, figures, fps=60)
    figures.clear()


# --------------------- DEFINE FIGURE AND SUBPLOTS ----------------------
axis1_settings = {"xlim": [-5, 5],
                  "ylim": [0, 30],
                  "axhline": 0,
                  "xlabel":"X",
                  "ylabel":"y"}

def get_matplotlib_fig():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
    apply_theme_to_figure(fig)
    apply_theme_to_subplot(axes[0], **axis1_settings)
    apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)
    return fig, axes

fig, axes = get_matplotlib_fig()

# --------------------------- DATA AND SCENES ---------------------------
def get_y(x, power=2, shift=0):
    return (x + shift) ** power

# ---------------------------- SCENE PRE-PLOTS --------------------------
def get_preplot(scene):
    global fig, axes
    fig, axes = get_matplotlib_fig()

    if scene > 0:
        pass

    if scene > 1:
        axes[0].plot(x, y, color="cyan")

    if scene > 2:
        axes[0].scatter(x_point, get_y(x_point), color="red",zorder=5)
        axes[0].plot(x_range, y_range, color="red",zorder=5)

    return fig, axes

# ---------------------------------- SCENE 1 -------------------------------------
scene = 1
n_frames = 100

x = ease_in_out(np.linspace(-5, 5, n_frames))
y = get_y(x, 2, 0)

for i in tqdm(range(1, len(x))):
    fig, axes = get_preplot(scene)
    axes[0].plot(x[:i], y[:i], color="cyan")
    plot()
    plt.close(fig)

axes[0].plot(x, y, color="cyan")

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="1_plot")
# -----------------------------------------------------------------------

# ---------------------------------- SCENE 2 -------------------------------------
scene = 2
n_frames = 100
n_frames_point = 100

x_point = 2
x_ponit1 = x_point + 0.00001
slope = (get_y(x_ponit1) - get_y(x_point)) / (x_ponit1 - x_point)
inverted_slope = -1 / slope

x_range = ease_in_out(np.linspace(1, 3, n_frames))
y_range = (inverted_slope * (x_range - x_point)) + get_y(x_point)

for i in tqdm(range(n_frames_point)):
    fig, axes = get_preplot(scene)
    axes[0].scatter(x_point, get_y(x_point), color="red", alpha=i/n_frames_point)
    plot()
    plt.close(fig)

for i in tqdm(range(1, len(x))):
    fig, axes = get_preplot(scene)
    axes[0].scatter(x_point, get_y(x_point), color="red",zorder=5)
    axes[0].plot(x_range[:i], y_range[:i], color="red",zorder=5)
    plot()
    plt.close(fig)

axes[0].scatter(x_point, get_y(x_point), color="red",zorder=5)
axes[0].plot(x_range, y_range, color="red",zorder=5)

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="2_tangent")
# -----------------------------------------------------------------------

