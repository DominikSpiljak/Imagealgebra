import cv2 as cv
import numpy as np
import matplotlib as plt


def load_and_process_image(path):
    img = cv.imread(path)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_invert = cv.bitwise_not(img_gray)
    return img_invert


def find_contours(image):
    ret, thresh = cv.threshold(image, 127, 255, 0)
    return cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


def overlapping_axes(coord1, delta1, coord2, delta2):
    if coord1 <= coord2 + delta2 and coord1 >= coord2:
        return True
    if coord1 + delta1 <= coord2 + delta2 and coord1 + delta1 >= coord2:
        return True
    if coord2 <= coord1 + delta1 and coord2 >= coord1:
        return True
    if coord2 + delta2 <= coord1 + delta1 and coord2 + delta2 >= coord1:
        return True

    return False


def find_unique_contours(image):
    contours, hierarchy = find_contours(image)
    boundingRects = [cv.boundingRect(contour) for contour in contours]

    # If 2 bounding boxes are overlapping, take the bigger one
    for i in range(len(boundingRects)):
        if boundingRects[i] is None:
            continue
        for j in range(i + 1, len(boundingRects)):
            if boundingRects[j] is None:
                continue
            x1, y1, width1, height1 = boundingRects[i]
            x2, y2, width2, height2 = boundingRects[j]

            if overlapping_axes(x1, width1, x2, width2) and overlapping_axes(y1, height1, y2, height2):
                if width1 * height1 > width2 * height2:
                    boundingRects[j] = None
                else:
                    boundingRects[i] = None
                    break

    return [bounding for bounding in boundingRects if bounding is not None]


def crop_bounding_box(image, bounding_box):
    x, y, width, height = bounding_box
    cropped_image = image[y:y+height, x:x+width]
    return cropped_image


def vectorize(path):
    img = load_and_process_image(path)
    contours, _ = find_contours(img)
    try:
        # In case of multiple contours, take one with the biggest area
        bounding_box = cv.boundingRect(sorted(contours, key=cv.contourArea)[-1])
    except IndexError:
        plt.imshow(img)
        plt.show()
        raise
    img = crop_bounding_box(img, bounding_box)
    img = cv.resize(img, (30, 30))
    img = img.reshape(30, 30, 1)
    return img


if __name__ == "__main__":
    x1, y1, width1, height1 = (62, 59, 135, 363)
    x2, y2, width2, height2 = (181, 76, 3, 3)
    print(overlapping_axes(x1, width1, x2, width2),
          overlapping_axes(y1, height1, y2, height2))
