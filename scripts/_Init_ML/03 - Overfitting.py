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

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from tqdm import tqdm


np.random.seed(42)
# -------------------------- DEFINE SETTINGS ----------------------------
SIZE_SCALE_FACTOR = 1
WIDTH = 20 * SIZE_SCALE_FACTOR  # inches
HEIGHT = 10 * SIZE_SCALE_FACTOR  # inches
DPI = 200

INIT = True
PROJECT_FILE_NAME = "03 - Overfitting"
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
axis1_settings = {"xlim": [0, 10],
                  "ylim": [0, 20],
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
np.random.seed(42)
X = np.linspace(0, 10, 30).reshape(-1, 1)
y = (1.5*X) + 2 + np.random.uniform(-2, 2, X.shape)

model = tf.keras.Sequential([
    layers.Dense(4096, activation='relu', input_shape=(1,)),
    layers.Dense(4096, activation='relu'),
    layers.Dense(4096, activation='relu'),
    layers.Dense(4096, activation='relu'),
    layers.Dense(4096, activation='relu'),
    layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# ---------------------------- SCENE PRE-PLOTS --------------------------
def get_preplot(scene):
    global fig, axes
    fig, axes = get_matplotlib_fig()

    if scene > 0:
        pass

    if scene > 1:
        pass

    return fig, axes

# ---------------------------------- SCENE 1 -------------------------------------
for _ in tqdm(range(400)):
    history = model.fit(X, y, epochs=1, verbose=0)
    y_pred = model.predict(X)
    fig, axes = get_matplotlib_fig()
    axes[0].scatter(X, y, color="r")
    axes[0].plot(X, y_pred, color='cyan')
    plot()
    plt.close(fig)

y_pred = model.predict(X)
fig, axes = get_matplotlib_fig()
axes[0].scatter(X, y, color="r")
axes[0].plot(X, y_pred, color='cyan')

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="1_fit")
# -----------------------------------------------------------------------
