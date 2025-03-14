import os
import io
import shutil
import ffmpeg
import imageio
import subprocess
import numpy as np
from tqdm import tqdm
from copy import deepcopy

from mayavi import mlab
import matplotlib.pyplot as plt

from utils.themes import *
from utils.functions import *
from utils.numpy_utils import *
from utils.string_utils import *
from utils.mayavi_utils import *
from utils.mayavi_theme import *
from utils.functions_3d import *

import numpy as np
np.random.seed(42)

from sklearn.linear_model import LinearRegression

# -------------------------- DEFINE SETTINGS ----------------------------
SIZE_SCALE_FACTOR = 1
WIDTH = 20 * SIZE_SCALE_FACTOR  # inches
HEIGHT = 10 * SIZE_SCALE_FACTOR  # inches
DPI = 200

INIT = True
PROJECT_FILE_NAME = "3d_base"
SAVE_FILE = True
mlab.options.offscreen = True

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
def get_matplotlib_fig():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
    apply_theme_to_figure(fig)
    apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)
    return fig, axes

fig, axes = get_matplotlib_fig()

axis1_settings_3d = {
    "x_label": "Sqft",
    "y_label": "Age",
    "z_label": "Price",
    "xlim": [0, 1500],
    "ylim": [0, 10],
    "zlim": [500000, 1500000],
    "tick_offset": (1.1, 0.8, 0.8),
    "tick_line_thickness": 0.1,
    "num_ticks": 5,
    "z_tick_values": ["0.5M", "0.75M", "1M", "1.25M", "1.5M"],
    "tick_scale": [0.3, 0.3, 0.3]
}
get_mayavi_figure_from_matplotlib_axis(mlab, axes[0], SIZE_SCALE_FACTOR)
create_3d_axes(mlab, **axis1_settings_3d)

axis1_scaler = AxisScaler(**axis1_settings_3d)

# -----------------------------------------------------------------------
set_image_on_subplot(mlab, axes[0], azimuth=10, elevation=30, distance=35, focalpoint=(5, 5, 5))
plot()
create_video_and_cleanup(save_prefix="0_axis")
# -----------------------------------------------------------------------




# --------------------------- DATA AND GRAPHS ---------------------------
N = 100
x1 = np.random.permutation(np.linspace(0, 1500, num=N))
x2 = np.random.permutation(np.linspace(0, 10, num=N))
m1 = (1500000 - 500000) / 1500
m2 = -15000
intercept = 500000 - 4116

y = ((m1 * x1) + (m2 * x2) + intercept) + np.random.normal(0, 20000, size=x1.shape)
x1_scaled, x2_scaled, y_scaled = axis1_scaler.convert(x1, x2, y)

# ---------------------------- SCENE PRE-PLOTS --------------------------
def get_preplot(scene):
    global fig, axes
    fig, axes = get_matplotlib_fig()

    if scene > 0:
        pass

    if scene > 1:
        scatter = mlab.points3d(x1_scaled, x2_scaled, y_scaled, scale_factor=0.15, color=MAYAVI_COLORS["red"])
        set_image_on_subplot(mlab, axes[0], azimuth=10, elevation=30, distance=35, focalpoint=(5, 5, 5))

    return fig, axes

# ---------------------------------- SCENE 1 -------------------------------------
scene = 1

frames_per_point = 3
for pt in tqdm(range(1, N)):
    for i in range(frames_per_point):
        alphas = np.concatenate([np.ones(pt - 1), [i / frames_per_point]])
        fig, axes = get_preplot(scene)
        rgba_colors = np.array([[1, 0, 0, alpha] for alpha in alphas])
        if len(rgba_colors) == 1:
            rgba_colors = np.vstack([rgba_colors, rgba_colors])
        scatter = mlab.points3d(
            x1_scaled[:pt],
            x2_scaled[:pt],
            y_scaled[:pt],
            scale_factor=0.15,
            color=None
        )
        scatter.glyph.color_mode = 'color_by_scalar'
        scatter.mlab_source.dataset.point_data.scalars = alphas
        scatter.module_manager.scalar_lut_manager.lut.table = (rgba_colors * 255).astype(np.uint8)
        mlab.draw()
        mlab.process_ui_events()
        set_image_on_subplot(mlab, axes[0], azimuth=10, elevation=30, distance=35, focalpoint=(5, 5, 5))
        plot()
        plt.close(fig)

fig, axes = get_preplot(scene+1)

# -----------------------------------------------------------------------
plot()
create_video_and_cleanup(save_prefix="1_scatter")
# -----------------------------------------------------------------------
