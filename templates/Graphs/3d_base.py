import os
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

SAVE_FILE = True
mlab.options.offscreen = True

def plot(save_file=SAVE_FILE, save_prefix=""):
    if save_file:
        save_path = os.path.join("media", os.path.splitext(os.path.basename(__file__))[0])
        os.makedirs(save_path, exist_ok=True)
        count = 1

        while os.path.isfile(os.path.join(save_path, f"{save_prefix}_{count}.png")):
            count += 1

        file_name = f"{save_prefix}_{count}.png"
        final_save_path = os.path.join(save_path, file_name)
        plt.savefig(final_save_path, dpi=DPI, bbox_inches='tight')
    else:
        plt.show(block=True)


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
# set_image_on_subplot(mlab, axes[0], azimuth=10, elevation=30, distance=35, focalpoint=(5, 5, 5))
# plot(save_prefix="0_axis")
# -----------------------------------------------------------------------




# --------------------------- DATA AND GRAPHS ---------------------------
x1 = np.random.permutation(np.linspace(0, 1500, num=100))
x2 = np.random.permutation(np.linspace(0, 10, num=100))
m1 = (1500000 - 500000) / 1500
m2 = -15000
intercept = 500000 - 4116

y = ((m1 * x1) + (m2 * x2) + intercept) + np.random.normal(0, 20000, size=x1.shape)
x1_scaled, x2_scaled, y_scaled = axis1_scaler.convert(x1, x2, y)
scatter = mlab.points3d(x1_scaled, x2_scaled, y_scaled, scale_factor=0.15, color=MAYAVI_COLORS["red"])

# -----------------------------------------------------------------------
# set_image_on_subplot(mlab, axes[0], azimuth=10, elevation=30, distance=35, focalpoint=(5, 5, 5))
# plot(save_prefix="1_scatter")
# -----------------------------------------------------------------------