import cv2
import time
import imutils
import argparse
import numpy as np


from math import pow, sqrt
from imutils.video import FPS
from imutils.video import VideoStream
from flask import Flask, render_template, Response


#Initialize Flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('Direct_Stream.html')

def sketch(image):
    # Convert image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Clean up image using Guassian Blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    
    # Extract edges
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    
    # Do an invert binarize the image 
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask

def gen():

#Initialize Video Stream (Use src = 0 for Webcam or src = 'path to video input')
    print('[Status] Starting Video Stream...')
    vs = VideoStream(src = 0).start()
    #time.sleep(0.1)
    fps = FPS().start()





#Loop Video Stream
    while True:
    
    #Resize Frame to 600 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=750,height=500)
	



        frame=sketch(frame)                  
         
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        fps.update()

    fps.stop()
    print("[INFO]Elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO]Approx. FPS:  {:.2f}".format(fps.fps()))


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of image tag in html code
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
