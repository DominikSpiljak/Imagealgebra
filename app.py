from decode_and_calculate import decode_and_calculate, MODEL
from time import strftime, localtime
import cv2 as cv
from flask import Flask, render_template, request, Response, send_file, redirect, url_for
import os
# Silence TensorFlow log
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


app = Flask(__name__)


class Camera(object):
    RESIZE_RATIO = 1.0

    def __init__(self):
        self.video = cv.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None

        if (Camera.RESIZE_RATIO != 1):
            frame = cv.resize(frame, None, fx=Camera.RESIZE_RATIO,
                              fy=Camera.RESIZE_RATIO)
        return frame

    def get_feed(self):
        frame = self.get_frame()
        if frame is not None:
            ret, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()

    def capture(self):
        frame = self.get_frame()
        return frame


camera = None
model = None


def get_camera():
    global camera
    if not camera:
        camera = Camera()

    return camera


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/index/')
def index():
    return render_template('index.html', expression=None, calculated=None)


def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/')
def video_feed():
    camera = get_camera()
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture/', methods=['GET', 'POST'])
def capture():
    camera = get_camera()
    image = camera.capture()
    expression, calculated = decode_and_calculate(image, model)
    del camera
    return render_template('index.html', expression=expression, calculated=str(calculated))


def main():
    global model
    from keras.models import load_model
    model = load_model(MODEL)
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    main()
