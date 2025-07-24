import pyautogui
import matplotlib.pyplot as plt
import numpy as np
import pygetwindow
import time

UCERTIFY_WINDOW_STRING = "-uCertify"
UCERTIFY_WINDOW_POSITION = (0, 0)
UCERTIFY_WINDOW_SIZE = (810, 880)
UCERTIFY_WINDOW_ROI = [0, 0, 797, 872]
# GREEN_DOT_X_COORD = 748
green_dot_x_range = (741, 756)

GREEN_COLORS = [
    [112, 173, 71],
    [53, 94, 59],
    [112, 173, 71],
    [53, 94, 59],
    [96, 128, 100],
    [67, 105, 73],
    # [176,192,179],
]

ignore_green_colors = [
    [82, 133, 139],
    [100, 76, 41],
]


def pixel_in_ignore_green_colors(pixel):
    for ignore_color in ignore_green_colors:
        if pixel_is_equal(pixel, ignore_color, tol=10):
            return True
    return False


def pixel_is_green(pixel):
    if pixel_in_ignore_green_colors(pixel):
        return False
    for green_color in GREEN_COLORS:
        if pixel_is_equal(pixel, green_color, tol=40):

            return True
    return False


def pixel_is_equal(p1, p2, tol=30):
    p1 = [int(x) for x in p1]
    p2 = [int(x) for x in p2]

    for i in range(3):
        if abs(p1[i] - p2[i]) > tol:
            return False
    return True


def show_image(image):
    plt.imshow(image)
    plt.show()


def screenshot():
    image = pyautogui.screenshot(region=UCERTIFY_WINDOW_ROI)
    image = np.array(image)
    return image


def orientate_uceritfy_window():
    window = pygetwindow.getWindowsWithTitle(UCERTIFY_WINDOW_STRING)[0]
    window.moveTo(UCERTIFY_WINDOW_POSITION[0], UCERTIFY_WINDOW_POSITION[1])
    window.resizeTo(UCERTIFY_WINDOW_SIZE[0], UCERTIFY_WINDOW_SIZE[1])


def find_green_dots():
    image = screenshot()

    green_coords = []

    min_y_value = 180
    max_y_value = 730

    for y_index in range(image.shape[0]):
        if y_index < min_y_value:
            continue
        if y_index > max_y_value:
            continue
        for x_index in range(*green_dot_x_range):
            coord = (x_index, y_index)
            pixel = image[y_index][x_index]
            if pixel_is_green(pixel):
                # print(f"found green coord at ({x_index},{y_index}) | pixel is {pixel}")
                green_coords.append(coord)

    green_coords = coords_set(green_coords, threshold=30)

    return green_coords


def click(x, y):
    pyautogui.moveTo(x, y, 0.3)
    pyautogui.click(x, y)


import math


def coords_are_equal(c1, c2, threshold=10):
    x1, y1 = c1
    x2, y2 = c2
    euclidian_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # print(f'{c1} | {c2} | {euclidian_distance}')
    if euclidian_distance > threshold:
        return False
    return True


def coord_in_coords(coords, coord_to_search, threshold):
    for coord in coords:
        if coords_are_equal(coord, coord_to_search, threshold):
            return True
    return False


def coords_set(coords, threshold=10):
    unique_coords = []

    for coord_to_add in coords:
        if not coord_in_coords(unique_coords, coord_to_add, threshold):
            unique_coords.append(coord_to_add)

    # print(f'Combined a list of {len(coords)} coords into {len(unique_coords)} coords')
    return unique_coords


def mark_as_read(green_coord):
    # click the green space
    pyautogui.click(green_coord[0], green_coord[1], duration=0.3)
    mark_as_read_y_difference = 30
    mark_as_read_x_difference = -10
    time.sleep(0.3)
    pyautogui.click(
        green_coord[0] + mark_as_read_x_difference,
        green_coord[1] + mark_as_read_y_difference,
        duration=0.3,
    )


def next_page():
    next_page_button = (600,840)
    pyautogui.click(next_page_button[0], next_page_button[1], duration=0.3)
    time.sleep(2)


def get_page_pixels():
    pixels = []
    image = screenshot()
    ltrb = [120,265,300,440]
    for x in range(ltrb[0],ltrb[2]):
        for y in range(ltrb[1],ltrb[3]):
            pixel = image[y][x]
            pixels.append(pixel)

    return pixels

def mark_this_section_as_read():
    green_dot_coords = find_green_dots()
    for green_coord in green_dot_coords:
        mark_as_read(green_coord)
        # pyautogui.moveTo(green_coord[0], green_coord[1], duration=0.3)
        print(f'Marked as read: {green_coord}')

def page_pixels_are_equal(pixels1, pixels2, tol=30):
    if len(pixels1) != len(pixels2):
        return False

    for i in range(len(pixels1)):
        if not pixel_is_equal(pixels1[i], pixels2[i], tol):
            return False

    return True

def mark_this_page_as_read():
    while 1:
        current_section_pixels = get_page_pixels()
        mark_this_section_as_read()
        scroll()
        next_section_pixels = get_page_pixels()
        if page_pixels_are_equal(current_section_pixels, next_section_pixels, tol=30):
            print('No more content loaded after scrolling, stopping marking this page')
            break

def scroll(direction="down"):
    amount = 600

    if direction == "down":
        pyautogui.scroll(amount*-1)
    elif direction == "up":
        pyautogui.scroll(amount)
    else:
        raise ValueError("Direction must be 'up' or 'down'")
    time.sleep(1)

def spam_read():
    while 1:
        mark_this_page_as_read()
        next_page()

if __name__ == "__main__":
    spam_read()

