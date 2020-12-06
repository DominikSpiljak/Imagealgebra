# Imagealgebra

Walmart Photomath

## Handwritten character detector

All functionality for this section is written in `utils/image_processing`.

First off, we need to load the image and do a little bit of processing using `load_and_process_image` function.
This function, given a path to the image, loads that image, greyscales it and inverts it.
Image needs to be inverted for cv2 to be able to find contours where background is black and character is white.

Secondly, we find contours using `find_contours` function.
There are situations where this function could return multiple contours for one character. In that case, we simply take the contour with the biggest area.
After that we need to find a bounding box for that contour and then crop that bounding box using `crop_bounding_box` function.
Also, we resize the cropped photo to **30x30** pixels.

## Training the model

### Dataset

First off, I took this dataset: https://www.kaggle.com/xainano/handwrittenmathsymbols and thought:

> Oh wow, this will be easy

Well, it wasn't. Some classes in the dataset are reeealy unbalanced. For instance there are 25683 images for number 1 and 515 for forward_slash.
Also, the dataset is pretty wild.

This is a number 8:

![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/8_15575.jpg?raw=true)
