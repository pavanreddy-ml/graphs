import numpy as np

def ease_in_out(x, ease_amount=1.4):
    normalized = np.linspace(0, 1, len(x))
    eased = 3 * (normalized ** (ease_amount * 2)) - 2 * (normalized ** (ease_amount * 3))
    return eased * (x[-1] - x[0]) + x[0]

def extend_array_to_num_frames(num_frames, array):
    array = np.array(array)

    if len(array) < num_frames:
        final_element = array[-1]
        extension = np.full(num_frames - len(array), final_element)
        array = np.concatenate([array, extension])

    return array