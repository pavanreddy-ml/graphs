import numpy as np


class AxisScaler:
    def __init__(self, **kwargs):
        self.xlim = kwargs.get('xlim', [0, 1500])
        self.ylim = kwargs.get('ylim', [0, 10])
        self.zlim = kwargs.get('zlim', [500000, 1500000])

        # Calculate scaling factors
        self.x_scale = 10 / (self.xlim[1] - self.xlim[0])
        self.y_scale = 10 / (self.ylim[1] - self.ylim[0])
        self.z_scale = 10 / (self.zlim[1] - self.zlim[0])

    def convert(self, x, y, z):
        # Function to scale a single value
        def scale_value(val, orig_min, scale_factor):
            return (val - orig_min) * scale_factor

        # Function to scale an array
        def scale_array(arr, orig_min, scale_factor):
            return (arr - orig_min) * scale_factor

        # Determine input type and scale accordingly
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float)):
            # Single values
            x_scaled = scale_value(x, self.xlim[0], self.x_scale)
            y_scaled = scale_value(y, self.ylim[0], self.y_scale)
            z_scaled = scale_value(z, self.zlim[0], self.z_scale)
        elif isinstance(x, np.ndarray) and isinstance(y, np.ndarray) and isinstance(z, np.ndarray):
            # Numpy arrays
            x_scaled = scale_array(x, self.xlim[0], self.x_scale)
            y_scaled = scale_array(y, self.ylim[0], self.y_scale)
            z_scaled = scale_array(z, self.zlim[0], self.z_scale)
        else:
            raise ValueError("Input must be either all single numbers or all numpy arrays")

        return x_scaled, y_scaled, z_scaled