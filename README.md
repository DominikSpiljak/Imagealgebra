# Imagealgebra

Walmart Photomath

## Handwritten character detector

All functionality for this section is written in `utils/image_processing`.

First off, we need to load the image and do a little bit of processing using `load_and_process_image` function.
This function, given a path to the image, loads that image, greyscales it and inverts it.
Also, I've set the threshold for characters to be 190. The reason is so that we don't draw contour over shadows and darker areas that aren't characters.
Image needs to be inverted for cv2 to be able to find contours where background is black and character is white.

Secondly, we find contours using `find_contours` function.
There are situations where this function could return multiple contours for one character. In that case, we simply take the contour with the biggest area.
After that we need to find a bounding box for that contour and then crop that bounding box using `crop_bounding_box` function.
Also, we resize the cropped photo to **30x30** pixels.

## Training the model

### Dataset

First off, I took this dataset: https://www.kaggle.com/xainano/handwrittenmathsymbols and created the initial dataset and thought:

> Oh wow, this will be easy

Well, it wasn't. Some classes in the dataset are reeealy unbalanced. For instance there are 25683 images for number 1 and 515 for forward_slash.
Also, the dataset is pretty wild.

This is a number 8:

![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/8_15575.jpg?raw=true)

And it's not even the worst one.
Then I hand-picked 200 images for each class and created a smaller dataset.

Also, I came across: https://www.kaggle.com/clarencezhao/handwritten-math-symbol-dataset and extended the smaller dataset to get the final dataset.
I also considered to add MNIST dataset but the current one prove to be okay.

**Important note**: This is far from good, the dataset needs a lot of work and images from different sources. This is just proof of concept so anything that works most of the time is good.

**Note**: In the mean time, since I had more time, I managed to extend the dataset with some images from MNIST. The problem I came across is that most of the 1's are written as "sticks". Am I the only one who doesn't write ones like that? I mean, it's really difficult to come across images of 1's that look literally like 1's. Well, it wouldn't be a problem if we didn't want to classify '/' characters. A LOT of 1's looked like '/' character. So in this new dataset I focused on creating some kind of "gap" between those 2 classes.

### Model and training

Since the problem isn't too complex, I decided to use a popular Convolutional Neural Network called LeNet-5.

It's relatively simple:

![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/model.png?raw=true)

If you want to read more about this model, check out: http://yann.lecun.com/exdb/lenet/

In total I trained 5 models:

1. `lenet_25epochs.h5`

   - This model is trained **only** on the initial big dataset and achieved around 98% accuracy during evaluation but was really bad on real-life problems.

2. `lenet_10epochs_small.h5`

   - This model is trained on hand-picked 200 images-per-class dataset. It achieved around 96% accuracy during evaluation but was also really bad on real-life problems.

3. `lenet_25epochs_small.h5`

   - Same data as the 2. one but trained over 25 epochs. Same results as the one above.

4. `lenet_25epochs_weighted.h5`

   - Same data and number of epochs as 1. one but I added class weights because of the class imbalance. Same results as the first one.

5. `lenet_25epochs_small_extended.h5`
   - Trained on the 2-datasets combined dataset, hence the extended in the name. Until I came up with the MNIST update this was by far the best model.

**note**: Reffering to the last note, I trained a new model on the final dataset.

6. `lenet_15epochs_small_weighted_extended_refined.h5`

   Just before we move to model description, I'm really sorry for the long name, my naming conventions are terrible.

   Anyways while training this model I noticed a huge mistake I've made. There is no regularization and my model was overfitting like crazy.
   So this model differs from the last 5 ones in a few ways:

   - I've added a Dropout(0.23) just after second Pooling. Also, after some reading on CNN's I switched activations of Conv layers to tanh which proved to be better.

   - Test accuracy: 0.9568434032059187
   - Training loss:
     ![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/loss.png?raw=true)
   - Training accuracy:
     ![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/accuracy.png?raw=true)
   - Test F1 score, recall and precision over classes:
     ![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/f1_prec_rec.png?raw=true)
   - Confusion matrix:
     ![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/readme_images/cm.png?raw=true)

## Solver

Solver is relatively simple and is found in `main.py` as `evaluate_expression`.
The idea is to use two stacks, one is for operators and one is for number values.

We iterate through expression and store numbers into value stack.
When we get to an operator, we check if he has precedence over other operators in stack.

When we get to the end of the expression, apply remaining operators and the solution is the only value left in the value stack.

## Usage

This project is really simple to setup and use:

- Clone the repo
- Run the script using `python main.py path/to/image_containing expression`

I commited an some example images to this repo:

![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/test1.jpg?raw=true)

![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/test2.jpg?raw=true)

![alt text](https://github.com/DominikSpiljak/Imagealgebra/blob/main/test3.jpg?raw=true)

and after running `python main.py test1.jpg`, the output is:

Decoded expression: 87+95

Calculated expression: 182

`python main.py test2.jpg`:

Decoded expression: 87+95

Calculated expression: 182

`python main.py test3.png`:

Decoded expression: 7x(8/11)

Calculated expression: 5.090909090909091
