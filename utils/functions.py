from matplotlib.patches import FancyArrowPatch
from .themes import *
import matplotlib.ticker as ticker

# Apply theme to figure
def apply_theme_to_figure(figure, **kwargs):
    settings = {**DEFAULT_SETTINGS["fig"], **kwargs}

    figure.patch.set_facecolor(settings['facecolor'])
    figure.patch.set_edgecolor(settings['edgecolor'])

    if settings['tight_layout']:
        figure.tight_layout()

def apply_theme_to_subplot(axis, **kwargs):
    settings = {**DEFAULT_SETTINGS["subplot"], **kwargs}

    # Remove spines completely (including top, bottom, left, and right)
    for spine in axis.spines.values():
        spine.set_visible(False)

    if settings["show_label"]:
        axis.set_xlabel(settings["xlabel"], fontsize=settings["xlabel_size"], color=settings["label_color"])
        axis.set_ylabel(settings["ylabel"], fontsize=settings["ylabel_size"], color=settings["label_color"])

    if settings["axhline"] is not None:
        axis.axhline(settings["axhline"], color=settings["spine_color"])
    if settings["axvline"] is not None:
        axis.axvline(settings["axvline"], color=settings["spine_color"])

    if settings["y_ticker_label"]:
        axis.yaxis.set_major_formatter(settings["y_ticker_label"])
    if settings["x_ticker_label"]:
        axis.xaxis.set_major_formatter(settings["x_ticker_label"])

    # Set axis face color (background color)
    axis.set_facecolor(settings['facecolor'])

    # Apply tick params (tick color, direction)
    axis.tick_params(axis='both', colors=settings['tick_color'], direction=settings['tick_direction'], labelsize=settings['tick_label_size'])

    # Grid settings
    if settings['grid']:
        axis.grid(True, which=settings['grid_which'], color=settings['grid_color'],
                  alpha=settings['grid_alpha'], linestyle=settings['grid_linestyle'],
                  linewidth=settings['grid_linewidth'])
    else:
        axis.grid(False)

    # Label colors
    axis.xaxis.label.set_color(settings['label_color'])
    axis.yaxis.label.set_color(settings['label_color'])

    if settings['title']:
        axis.set_title(settings['title'], color=settings['title_color'])

    # Axis limits and aspect ratio
    if settings['xlim']:
        axis.set_xlim(settings['xlim'])
    if settings['ylim']:
        axis.set_ylim(settings['ylim'])
    axis.set_aspect(settings['aspect'])

    # Hide the ticks but keep the x and y axes visible
    axis.get_xaxis().set_ticks_position('none')  # No ticks at the bottom
    axis.get_yaxis().set_ticks_position('none')  # No ticks on the left

    # Add x and y axis lines with arrows
    if settings['show_axis']:
        axis.axhline(0, color=settings['spine_color'], lw=settings['axes_linewidth'])  # x-axis at y=0
        axis.axvline(0, color=settings['spine_color'], lw=settings['axes_linewidth'])  # y-axis at x=0

    # Add arrows at the ends of the x and y axes if requested
    if settings["add_arrows"]:
        add_axis_arrows(axis)


# Function to add arrows at the end of axes
def add_axis_arrows(axis, arrow_length_ratio=0.005, y_axis_center_correction=0.1):
    x_min, x_max = axis.get_xlim()
    y_min, y_max = axis.get_ylim()

    x_offset = (x_max - x_min) * arrow_length_ratio
    y_offset = (y_max - y_min) * arrow_length_ratio

    x_intercept = 0 if (x_min <= 0 <= x_max) else x_min
    y_intercept = 0 if (y_min <= 0 <= y_max) else y_min

    arrow_x = FancyArrowPatch(
        (x_max, y_intercept),
        (x_max + x_offset, y_intercept),
        mutation_scale=20,  # Controls the head size
        shrinkA=0,
        shrinkB=0,  # Don't shrink the arrow
        color='white',
        lw=4,
        arrowstyle=f'->',  # Use a simple arrow style
        clip_on=False)

    axis.add_patch(arrow_x)

    arrow_y = FancyArrowPatch(
        (x_intercept + y_axis_center_correction, y_max),
        (x_intercept + y_axis_center_correction, y_max + y_offset),
        mutation_scale=20,  # Controls the head size
        shrinkA=0,
        shrinkB=0,  # Don't shrink the arrow
        color='white',
        lw=4,
        arrowstyle=f'->',  # Use a simple arrow style
        clip_on=False
    )
    axis.add_patch(arrow_y)

    axis.set_xlim(x_min, x_max + x_offset)
    axis.set_ylim(y_min, y_max + y_offset)
