import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import cv2
from playsound import playsound
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

frequency = 5
waitTime = 60/frequency
minutes = 20

threshold = frequency * minutes * .90

count = 0


KEY = 'a92776836a8e40318cdc4f493b2eb564'

ENDPOINT = 'https://eyesafe.cognitiveservices.azure.com/'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))




test_image_array = glob.glob(r'picture/name.png')
image = open(test_image_array[0], 'r+b')

face_ids = []

# We use detection model 2 because we are not retrieving attributes.
detected_faces = face_client.face.detect_with_stream(image, detectionModel='detection_01')
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))



while(True):
    if(count > threshold ):
        count = 0
        playsound(r'audio/test.wav')
    else:

        cam = cv2.VideoCapture(0)

        ret, frame = cam.read()

        img_name = r"picture\name.png".format()
        cv2.imwrite(img_name, frame)

        cam.release()
        cv2.destroyAllWindows()


        test_image_array = glob.glob(r'picture/name.png')
        image = open(test_image_array[0], 'r+b')

        face_ids = []

        detected_faces = face_client.face.detect_with_stream(image, detectionModel='detection_01')
        if detected_faces:
            print(detected_faces.faceId)
        count += 1

    print(count)
    time.sleep(waitTime)
