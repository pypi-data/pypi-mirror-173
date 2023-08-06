import numpy as np

CHIP_BITMAP_CHIP_BY_CHIP = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536,
                                     131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432,
                                     67108864, 134217728, 268435456, 536870912])


def convert(chip_bitmap: int, incr: int) -> (np.ndarray, np.ndarray):
    """
    Convert chip_bitmap to the corresponding bitmap array, and position array
    :param chip_bitmap: bitmap of the selected chip
    :param incr: size of the data we expect, 5 for chip register and 480 for pixel_register
    :return: bitmap array / position array
    """
    number_of_chips: int = len(CHIP_BITMAP_CHIP_BY_CHIP)
    binary_list = [int(c) for c in bin(chip_bitmap)[2:]]
    binary_list = np.flip(binary_list) > 0

    if len(binary_list) < number_of_chips:
        app = np.full((number_of_chips - len(binary_list),), False)
        binary_list = np.append(binary_list, app)

    out_list = CHIP_BITMAP_CHIP_BY_CHIP[binary_list]
    pos_list = np.uint32(np.log2(out_list))
    incr_arr = np.multiply(pos_list, incr)

    return out_list, incr_arr
