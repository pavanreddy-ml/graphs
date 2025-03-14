import matplotlib

MAYAVI_COLORS = {}
MAYAVI_COLORS.update(matplotlib.colors.CSS4_COLORS)
MAYAVI_COLORS = {name: matplotlib.colors.to_rgb(color) for name, color in MAYAVI_COLORS.items()}