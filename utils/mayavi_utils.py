from utils.mayavi_theme import *
import numpy as np


def get_mayavi_figure_from_matplotlib_axis(mlab, axis, size_scale_factor):
    base_width = 3840
    base_height = 2160

    fig = axis.get_figure()
    fig_width, fig_height = fig.get_size_inches()
    bbox = axis.get_position()
    width = bbox.width * fig_width
    height = bbox.height * fig_height
    aspect_ratio = width / height

    if aspect_ratio >= 1:
        adjusted_width = int(base_width * size_scale_factor)
        adjusted_height = int(adjusted_width / aspect_ratio)
    else:
        adjusted_height = int(base_height * size_scale_factor)
        adjusted_width = int(adjusted_height * aspect_ratio)

    mayavi_figure = mlab.figure(bgcolor=(0, 0, 0), size=(adjusted_width, adjusted_height))

    return mayavi_figure


def create_3d_axes(mlab, **kwargs):
    xlim = kwargs.get('xlim', (0, 1500))
    ylim = kwargs.get('ylim', (0, 10))
    zlim = kwargs.get('zlim', (500000, 1500000))

    axis_line_width = kwargs.get("axis_line_width", 0.5)
    arrow_thickness = kwargs.get("arrow_thickness", 0.01)
    axis_color = MAYAVI_COLORS[kwargs.get("axis_color", "white")]

    x_label = kwargs.get('x_label', r'X')
    y_label = kwargs.get('y_label', r'Y')
    z_label = kwargs.get('z_label', r'Z')
    label_color = MAYAVI_COLORS[kwargs.get("label_color", "white")]
    label_offset = kwargs.get("label_offset", 11)
    label_size = kwargs.get("label_size", (0.5, 0.5, 0.5))

    num_ticks = kwargs.get("num_ticks", 5)
    tick_line_thickness = kwargs.get("line_thickness", 0.005)
    tick_offset = kwargs.get("tick_offset", (0.5, 0.5, 0.5))
    tick_scale = kwargs.get("tick_scale", (0.5, 0.5, 0.5))
    x_tick_values = kwargs.get('x_tick_values', [f'{x:.0f}' for x in np.linspace(xlim[0], xlim[1], num_ticks)])
    y_tick_values = kwargs.get('y_tick_values', [f'{y:.0f}' for y in np.linspace(ylim[0], ylim[1], num_ticks)])
    z_tick_values = kwargs.get('z_tick_values', [f'{z:,.0f}' for z in np.linspace(zlim[0], zlim[1], num_ticks)])

    for label_list in [x_tick_values, y_tick_values, z_tick_values]:
        if len(label_list) != num_ticks:
            raise ValueError(f"Number of tick labels ({len(label_list)}) does not match num_labels ({num_ticks})")

    # Create axes from 0 to 10
    x_axis = mlab.quiver3d(0, 0, 0, 10, 0, 0, color=axis_color, mode='arrow', scale_factor=1, line_width=axis_line_width)
    y_axis = mlab.quiver3d(0, 0, 0, 0, 10, 0, color=axis_color, mode='arrow', scale_factor=1, line_width=axis_line_width)
    z_axis = mlab.quiver3d(0, 0, 0, 0, 0, 10, color=axis_color, mode='arrow', scale_factor=1, line_width=axis_line_width)

    # Adjust arrow properties
    for axis in [x_axis, y_axis, z_axis]:
        axis.glyph.glyph_source.glyph_source.shaft_radius = arrow_thickness
        axis.glyph.glyph_source.glyph_source.tip_radius = arrow_thickness * 2
        axis.glyph.glyph_source.glyph_source.tip_length = arrow_thickness * 8

    # Add labels next to arrows
    mlab.text3d(label_offset, 0, 0, x_label, color=label_color, scale=label_size[0])
    mlab.text3d(0, label_offset, 0, y_label, color=label_color, scale=label_size[1])
    mlab.text3d(0, 0, label_offset, z_label, color=label_color, scale=label_size[2])

    # Add tick marks and labels
    for i in range(num_ticks-1):
        pos = i * 10 / (num_ticks - 1)

        # X-axis ticks
        mlab.plot3d([pos, pos], [0, -0.2], [0, 0], color=axis_color, tube_radius=tick_line_thickness)
        mlab.text3d(pos, -tick_offset[0], 0, x_tick_values[i], color=label_color, scale=tick_scale[0])

        # Y-axis ticks
        mlab.plot3d([0, -0.2], [pos, pos], [0, 0], color=axis_color, tube_radius=tick_line_thickness)
        mlab.text3d(-tick_offset[1], pos, 0, y_tick_values[i], color=label_color, scale=tick_scale[1])
        # Z-axis ticks
        mlab.plot3d([0, -0.2], [0, 0], [pos, pos], color=axis_color, tube_radius=tick_line_thickness)
        mlab.text3d(-tick_offset[2], 0, pos, z_tick_values[i], color=label_color, scale=tick_scale[2])


def set_image_on_subplot(mlab, axis, **kwargs):
    # Default view parameters
    kwargs.setdefault("azimuth", -45)
    kwargs.setdefault("elevation", 20)
    kwargs.setdefault("distance", 25)
    kwargs.setdefault("focalpoint", (5, 5, 5))


    shift_leftright = kwargs.pop("shift_leftright", 0)
    shift_updown = kwargs.pop("shift_updown", 0)
    shift_inout = kwargs.pop("shift_inout", 0)

    mlab.view(**kwargs)
    camera = mlab.gcf().scene.camera

    position = np.array(camera.position)
    focal_point = np.array(camera.focal_point)

    view_vector = position - focal_point
    up_vector = np.array(camera.view_up)
    right_vector = np.cross(view_vector, up_vector)

    right_vector /= np.linalg.norm(right_vector)
    up_vector /= np.linalg.norm(up_vector)
    view_vector /= np.linalg.norm(view_vector)

    shift = (right_vector * shift_leftright +
             up_vector * shift_updown +
             view_vector * shift_inout)

    camera.position = tuple(position + shift)
    camera.focal_point = tuple(focal_point + shift)

    fig = mlab.gcf()
    mlab.draw()
    fig.scene._lift()

    image_array = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)

    axis.clear()
    axis.imshow(image_array, aspect='auto')

    return image_array
