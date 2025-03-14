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
PROJECT_FILE_NAME = "2d_base"
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
axis1_settings = {"xlim": [0, 1500],
                  "ylim": [500000, 1500000],
                  "axhline": 500000,
                  "xlabel":"Additaional Sqft.",
                  "ylabel":"Price (x $1M)"}

def get_matplotlib_fig():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
    apply_theme_to_figure(fig)
    apply_theme_to_subplot(axes[0], **axis1_settings)
    apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)
    return fig, axes

fig, axes = get_matplotlib_fig()

# --------------------------- DATA AND SCENES ---------------------------
N = 100
x = np.random.permutation(np.linspace(0, 1500, num=N))
slope = (1500000 - 500000) / 1500
intercept = 492486.26
y = (slope * x + intercept) + np.random.normal(0, 50000, size=x.shape)

# ---------------------------- SCENE PRE-PLOTS --------------------------
def get_preplot(scene):
    global fig, axes
    fig, axes = get_matplotlib_fig()

    if scene > 0:
        pass

    if scene > 1:
        axes[0].scatter(x, y, color="red", s=64)

    if scene > 2:
        axes[0].plot(x_vals[:-1], intercept+(slope * x_vals[:-1]), color="cyan")

    return fig, axes

# ---------------------------------- SCENE 1 -------------------------------------
scene = 1

frames_per_point = 10
for pt in tqdm(range(0, N)):
    for i in range(frames_per_point):
        alphas = [(1, 0, 0, 1) for _ in range(pt - 1)] + [(1, 0, 0, i / frames_per_point)]
        fig, axes = get_preplot(scene)
        axes[0].scatter(x[:pt], y[:pt], color=alphas, s=64)
        plot()
        plt.close(fig)

axes[0].scatter(x, y, color="red", s=64)

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="1_scatter")
# -----------------------------------------------------------------------

# ---------------------------------- SCENE 2 -------------------------------------
scene = 2
n_frames = 1000
x_vals = ease_in_out(np.linspace(0, 1500, n_frames))
for i in tqdm(range(1, len(x_vals))):
    fig, axes = get_preplot(scene)
    axes[0].plot(x_vals[:i], intercept+(slope * x_vals[:i]), color="cyan")
    plot()
    plt.close(fig)

axes[0].plot(x_vals[:-1], intercept+(slope * x_vals[:-1]), color="cyan")

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="2_line")
# -----------------------------------------------------------------------