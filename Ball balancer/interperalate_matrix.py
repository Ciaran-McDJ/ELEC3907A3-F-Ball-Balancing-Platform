import numpy as np
from scipy.interpolate import griddata

data = [
    [None, None, (178.23778, 239.69135), None, None, (283.03058, 233.97826), None],
    [(106.958, 276.26096), (144.38188, 275.03555), (180.18245, 273.52017), None, None, (286.1315, 267.27582), None],
    [(109.04088, 310.93637), (146.4808, 309.42035), (182.21104, 307.64346), (218.0415, 305.8496), (253.5068, 303.55048), (288.44675, 301.45132), None],
    [(110.95607, 346.48093), (148.18893, 344.60837), (184.18681, 342.6748), (220.05864, 340.8926), (255.89188, 339.04794), (290.91943, 336.8224), (326.0357, 334.405)],
    [(112.67258, 381.97296), (150.09456, 379.88773), (186.30792, 378.13492), (222.2882, 376.3092), (258.04102, 374.3302), (293.2953, 372.0947), (329.0721, 369.8592)],
    [(114.11052, 418.11792), (151.80594, 415.9457), (188.386, 414.0369), (224.71135, 412.08063), (259.94263, 410.31418), (295.9383, 408.4535), (331.94348, 405.98557)],
    [None, None, None, None, None, (298.59924, 445.02005), (334.81857, 442.8071)]
]

# Flatten the data and remove None values
flat_data = [point for row in data for point in row if point is not None]

# Separate x and y coordinates
x_coords = [point[0] for point in flat_data]
y_coords = [point[1] for point in flat_data]

# Generate grid
grid_x, grid_y = np.meshgrid(np.arange(len(data[0])), np.arange(len(data)))

# Interpolate missing values using linear interpolation
interpolated_values = griddata((x_coords, y_coords), flat_data, (grid_x, grid_y), method='linear')

print(interpolated_values)