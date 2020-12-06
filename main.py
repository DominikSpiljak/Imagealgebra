import os
import cv2 as cv
import numpy as np
import utils.image_processing as utils
import matplotlib.pyplot as plt

# Silence TensorFlow log
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class Stack:
    _stack: list

    def __init__(self):
        self._stack = []

    def push(self, element):
        self._stack.append(element)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]


def hasPrecedence(operator1, operator2):
    if operator2 == '(' or operator2 == ')':
        return False
    elif (operator1 == '*' or operator1 == '/') and (operator2 == '+' or operator2 == '-'):
        return False
    else:
        return True


def evaluate_expression(expression):
    operator_map = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '/': lambda x, y: x / y,
        'x': lambda x, y: x * y
    }
    operator_stack = Stack()
    value_stack = Stack()
    current_number = ""
    for i in range(len(expression)):
        if expression[i] == '(':
            operator_stack.push(expression[i])

        if expression[i].isnumeric():
            current_number += expression[i]

        if not expression[i].isnumeric() and current_number != "":
            value_stack.push(int(current_number))
            current_number = ""

        if expression[i] == ')':
            while operator_stack.peek() != '(':
                value2 = value_stack.pop()
                value1 = value_stack.pop()
                value_stack.push(operator_map[operator_stack.pop()](
                    value1, value2))

            operator_stack.pop()

        if expression[i] in operator_map:
            while operator_stack._stack != [] and hasPrecedence(expression[i], operator_stack.peek()):
                value2 = value_stack.pop()
                value1 = value_stack.pop()
                value_stack.push(operator_map[operator_stack.pop()](
                    value1, value2))
            operator_stack.push(expression[i])

    if current_number != "":
        value_stack.push(int(current_number))
        current_number = ""

    while operator_stack._stack != []:
        value2 = value_stack.pop()
        value1 = value_stack.pop()
        value_stack.push(operator_map[operator_stack.pop()](
            value1, value2))

    return value_stack.pop()


def main():
    from keras.models import load_model
    model = load_model('models/lenet_25epochs_small_extended.h5')

    img = utils.load_and_process_image('test.jpeg')
    bounding_boxes = sorted(
        utils.find_unique_contours(img), key=lambda x: x[0])
    cropped_boxes = [utils.crop_bounding_box(
        img, bounding) for bounding in bounding_boxes]
    X = np.array([cv.resize(cropped, (30, 30)).reshape(30, 30, 1)
                  for cropped in cropped_boxes])

    preds = np.argmax(model.predict(X), axis=1)

    inverse_label_map = {
        10: '+',
        11: '-',
        12: 'x',
        13: '/',
        14: '(',
        15: ')'
    }

    expression = "".join([str(pred) if pred < 10 else inverse_label_map[pred]
                          for pred in preds])

    print('Decoded expression: {}'.format(expression))
    print('Calculated expression: {}'.format(evaluate_expression(expression)))


if __name__ == "__main__":
    main()
