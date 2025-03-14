import os
import numpy as np
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

SAVE_FILE = False

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
        plt.show(block=True, tight_layout=True)


# --------------------- DEFINE FIGURE AND SUBPLOTS ----------------------
axis1_settings = {"xlim": [0, 1500], "ylim": [500000, 1500000], "axhline": 500000, "xlabel":"Additaional Sqft.", "ylabel":"Price (x $1M)"}

def get_matplotlib_fig():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))
    apply_theme_to_figure(fig)
    apply_theme_to_subplot(axes[0], **axis1_settings)
    apply_theme_to_subplot(axes[1], **TEXT_SUBPLOT_SETTINGS)
    return fig, axes

fig, axes = get_matplotlib_fig()

# -----------------------------------------------------------------------
plot(save_prefix="0_axis")
# -----------------------------------------------------------------------

# --------------------------- DATA AND SCENES ---------------------------

# ---------------------------------- SCENE 1 -------------------------------------

x = np.random.permutation(np.linspace(0, 1500, num=100))
slope = (1500000 - 500000) / 1500
intercept = 492486.26
y = (slope * x + intercept) + np.random.normal(0, 50000, size=x.shape)

axes[0].scatter(x, y, color="red", s=64)

# -----------------------------------------------------------------------
# plot(save_prefix="1_scatter")
# -----------------------------------------------------------------------

# ---------------------------------- SCENE 2 -------------------------------------