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

import sympy as sp



np.random.seed(42)
# -------------------------- DEFINE SETTINGS ----------------------------
SIZE_SCALE_FACTOR = 1
WIDTH = 20 * SIZE_SCALE_FACTOR  # inches
HEIGHT = 10 * SIZE_SCALE_FACTOR  # inches
DPI = 200

INIT = True
PROJECT_FILE_NAME = "Activation Functions"
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
axis1_settings = {"xlim": [-2, 2],
                  "ylim": [-2, 2],
                  "axhline": 0,
                  "xlabel":"",
                  "ylabel":""}

def get_matplotlib_fig():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
    apply_theme_to_figure(fig)
    apply_theme_to_subplot(axes[0], **axis1_settings)
    apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)
    return fig, axes

fig, axes = get_matplotlib_fig()

from functools import lru_cache
import json

if os.path.isfile("cache.json"):
    with open("cache.json", "r") as f:
        cache = json.load(f)
else:
    cache = {}


def activation(x):
    """
    Returns the positive and negative y roots for a given x value (or array of x values)
    using sympy for symbolic solving.
    """
    x_sym, y_sym = sp.symbols('x y')
    equation = (x_sym ** 2 + y_sym ** 2 - 1) ** 3 - x_sym ** 2 * y_sym ** 3

    positive_y = []
    negative_y = []

    for i, x_val in enumerate(np.atleast_1d(x)):  # Ensure x is iterable
        # Substitute x_val into the equation
        x_v = float(round(x_val, 3))
        if x_v in cache:
            positive_y.append(cache[x_v][0])
            negative_y.append(cache[x_v][1])
            continue
        eq_sub = equation.subs(x_sym, x_v)

        # Solve the equation for y
        roots = sp.solveset(eq_sub, y_sym, domain=sp.S.Reals)

        # Filter the roots into positive and negative
        roots = sorted(list(roots))  # Convert to sorted list for easier separation

        if len(roots) >= 2:  # Ensure there are two roots
            positive_y.append(float(roots[-1]))  # Largest root (positive)
            negative_y.append(float(roots[0]))  # Smallest root (negative)
            cache[x_v] = [float(roots[-1]), float(roots[0])]
        else:
            # Append NaN if roots are not found or invalid
            positive_y.append(None)
            negative_y.append(None)
            cache[x_v] = [None, None]

        if i % 50 == 0:
            with open("cache.json", "w") as f:
                json.dump(cache, f)

    with open("cache.json", "w") as f:
        json.dump(cache, f)

    for i in range (len(positive_y)):
        if positive_y[i] is None:
            positive_y[i] = np.nan

    return np.array(positive_y), np.array(negative_y)

# --------------------------- DATA AND SCENES ---------------------------

# ---------------------------- SCENE PRE-PLOTS --------------------------
def get_preplot(scene):
    global fig, axes
    fig, axes = get_matplotlib_fig()

    if scene > 0:
        pass
    if scene > 1:
        x_vals = np.linspace(-0, 1.139, n_frames)
        axes[0].plot(x_vals, activation(x_vals)[0], color="red")
        axes[0].plot([x_vals[-1], x_vals[-1]], list(activation(x_vals[-1])), color="red")
    if scene > 2:
        x_vals = np.linspace(1.139, 0, n_frames)
        axes[0].plot(x_vals, activation(x_vals)[1], color="red")
    if scene > 3:
        x_vals = np.linspace(0, -1.139, n_frames)
        axes[0].plot(x_vals, activation(x_vals)[1], color="red")
        axes[0].plot([x_vals[-1], x_vals[-1]], list(activation(x_vals[-1])), color="red")
    if scene > 4:
        x_vals = np.linspace(-1.139, 0, n_frames)
        axes[0].plot(x_vals, activation(x_vals)[0], color="red")

    return fig, axes

# ---------------------------------- SCENE 1 -------------------------------------
scene = 1
n_frames = 400
x_vals = np.linspace(-0, 1.139, n_frames)
for i in tqdm(range(1, len(x_vals)+1)):
    fig, axes = get_preplot(scene)
    axes[0].plot(x_vals[:i], activation(x_vals[:i])[0], color="red")
    plot()
    plt.close(fig)

fig, axes = get_preplot(scene)
axes[0].plot(x_vals[:i], activation(x_vals[:i])[0], color="red")
axes[0].plot([x_vals[-1], x_vals[-1]], list(activation(x_vals[-1])), color="red")
plot()
plt.close(fig)

# ---------------------------------- SCENE 2 -------------------------------------
scene = 2
x_vals = np.linspace(1.139, 0, n_frames)
for i in tqdm(range(1, len(x_vals)+1)):
    fig, axes = get_preplot(scene)
    axes[0].plot(x_vals[:i], activation(x_vals[:i])[1], color="red")
    plot()
    plt.close(fig)

# ---------------------------------- SCENE 2 -------------------------------------
scene = 3
x_vals = np.linspace(0, -1.139, n_frames)
for i in tqdm(range(1, len(x_vals)+1)):
    fig, axes = get_preplot(scene)
    axes[0].plot(x_vals[:i], activation(x_vals[:i])[1], color="red")
    plot()
    plt.close(fig)

# ---------------------------------- SCENE 1 -------------------------------------
scene = 4
x_vals = np.linspace(-1.139, 0, n_frames)

for i in tqdm(range(1, len(x_vals)+1)):
    fig, axes = get_preplot(scene)
    axes[0].plot(x_vals[:i], activation(x_vals[:i])[0], color="red")
    plot()
    plt.close(fig)

# ---------------------------------- SCENE 5 -------------------------------------
scene = 5
x_vals = np.linspace(-1.139, 1.139, n_frames)
for i in tqdm(range(1, len(x_vals))):
    fig, axes = get_preplot(scene)
    for x_v in range(i):
        x = x_vals[x_v]
        y_min, y_max = activation(x)
        axes[0].plot([x, x], [y_min, y_max], color="red")
    plot()
    plt.close(fig)


fig, axes = get_preplot(scene)
for x_v in range(len(x_vals)-1):
    x = x_vals[x_v]
    y_min, y_max = activation(x)
    axes[0].plot([x, x], [y_min, y_max], color="red")

for i in range (len(x_vals)):
    plot()

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="Heart")
# -----------------------------------------------------------------------