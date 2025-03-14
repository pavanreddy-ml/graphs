DEFAULT_SETTINGS = {
    "fig": {
        "facecolor": "black",
        "edgecolor": "white",
        "tight_layout": True,
    },
    "subplot": {
        "facecolor": "black",
        "edgecolor": "white",
        "tick_color": "white",
        "grid": True,
        "grid_color": "#cccccc",
        "grid_alpha": 0.5,
        "grid_linestyle": "--",
        "grid_linewidth": 0.5,
        "grid_which": "major",  # 'major', 'minor', or 'both'
        "title_color": "white",
        "legend_facecolor": "black",
        "legend_edgecolor": "white",
        "legend_text_color": "white",
        "spine_color": "white",  # Set to white so the axes are visible
        "tick_direction": "out",
        "minor_ticks": True,
        "axes_linewidth": 2.0,  # Visible axis lines
        "fontsize": 10,
        "fontweight": "normal",
        "alpha": 1.0,
        "xlim": [-10, 10],  # Set a limit for demonstration
        "ylim": [-10, 10],  # Set a limit for demonstration
        "xlabel": "X Axis",
        "ylabel": "Y Axis",
        "xlabel_size": "xx-large",  # No x-axis label
        "ylabel_size": "xx-large",
        "label_color": "white",
        "y_ticker_label": None,
        "x_ticker_label": None,
        "show_label": True,
        "axvline": 0,
        "axhline": 0,
        "title": "",
        "xticks": None,  # List of tick locations, or None for auto
        "yticks": None,  # List of tick locations, or None for auto
        "xticklabels": None,  # List of tick labels, or None for auto
        "yticklabels": None,  # List of tick labels, or None for auto
        "tick_label_size": "xx-large",
        "xtick_rotation": 0,
        "ytick_rotation": 0,
        "aspect": "auto",  # 'auto', 'equal', or a number
        "xscale": "linear",  # 'linear', 'log', 'symlog', 'logit'
        "yscale": "linear",  # 'linear', 'log', 'symlog', 'logit'
        "show_spine": True,  # Spines are visible
        "show_axis": True,
        "add_arrows": True,
    }
}

TEXT_SUBPLOT_SETTINGS = {
    "facecolor": "black",  # Background color
    "edgecolor": "black",  # Edge color of the subplot
    "tick_color": "black",  # Tick color (won't be visible since ticks are off)
    "grid": False,  # No grid
    "spine_color": "white",  # Set spines color to white
    "tick_direction": "out",  # Default tick direction (won't be visible)
    "minor_ticks": False,  # Disable minor ticks
    "axes_linewidth": 2.0,  # Set non-zero line width for visible spines
    "fontsize": 10,  # Font size for any text that you place
    "fontweight": "normal",  # Font weight for any text
    "alpha": 1.0,  # Opacity of the box
    "xlim": [0, 100],  # x-axis limits
    "ylim": [0, 100],  # y-axis limits
    "axvline": None,
    "axhline": None,
    "title": "",  # No title
    "xticks": [],  # No x-tick marks
    "yticks": [],  # No y-tick marks
    "xticklabels": [],  # No x-tick labels
    "yticklabels": [],  # No y-tick labels
    "xtick_rotation": 0,  # Rotation of x-tick labels (won't matter as they're hidden)
    "ytick_rotation": 0,  # Rotation of y-tick labels (won't matter as they're hidden)
    "aspect": "auto",  # Keep aspect auto
    "xscale": "linear",  # Linear scale for x-axis
    "yscale": "linear",  # Linear scale for y-axis
    "show_spine": False,
    "show_axis": False,
    "add_arrows": False,
    "show_label": False,
}
