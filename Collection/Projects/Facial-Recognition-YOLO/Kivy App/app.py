import os
import cv2
import numpy as np
import tensorflow as tf
from layers import L1Dist
import utils
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger

# Variables used
CAM_POS = 2 # Change this value accordingly to the pos of the camera youre using
X_CAM_POS = 230
Y_CAM_POS = 90
FRAME = 250
NUM_PIXELS = 105
APP_DIR = "./app_data"
VER_DIR = "ver_images"
INP_DIR = "input_images"
DET_THRESHOLD = 0.5
VER_THRESHOLD = 0.5


class CamApp(App):

    def build(self):
        self.img1 = Image(size_hint=(1,.8))
        self.ver = Label (text = "Verification Un Initiated", size_hint=(1,.1))
        self.button = Button(text="Verify", on_press=self.verify, size_hint=(1,.1))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.img1)
        layout.add_widget(self.ver)
        layout.add_widget(self.button)

        self.model = tf.keras.models.load_model("siamesenetwork.h5",custom_objects = {"L1Dist":L1Dist})

        self.capture = cv2.VideoCapture(CAM_POS)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout
    
    def update(self, *args):
        
        ret, frame = self.capture.read()
        frame = frame[Y_CAM_POS:Y_CAM_POS+FRAME,X_CAM_POS:X_CAM_POS+FRAME]

        buf = cv2.flip(frame,0).tostring()
        img_texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt="bgr")
        img_texture.blit_buffer(buf,colorfmt="bgr",bufferfmt="ubyte")
        self.img1.texture= img_texture

    def preprocess(self,file_path):

            # Reading image from file_path
            byte_img = tf.io.read_file(file_path)

            # Load the image, convert to jpeg
            img = tf.io.decode_jpeg(byte_img)

            # Resize to 105x105x3 ( According to paper )
            img = tf.image.resize(img,(NUM_PIXELS,NUM_PIXELS))

            # Normalize Image to be between 0 and 1
            img = img / 255.0
            
            return img
        
    def verify(self, * args):
        detection_threshold = DET_THRESHOLD
        verification_threshold = VER_THRESHOLD
        utils.get_ver_images(self.capture)
        results = []

        for inp_img in os.listdir(os.path.join(f"{APP_DIR}/{INP_DIR}")):
            for img in os.listdir(os.path.join(f"{APP_DIR}/{VER_DIR}")):
                input_img = self.preprocess(os.path.join(f"{APP_DIR}/{INP_DIR}",inp_img))
                val_img = self.preprocess(os.path.join(f"{APP_DIR}/{INP_DIR}",img))

                result = self.model.predict(list(np.expand_dims([input_img,val_img], axis=1)))
                results.append(result)

        detection = np.sum(np.array(results) > detection_threshold)

        verification = detection / len(os.listdir(os.path.join(f"{APP_DIR}/{VER_DIR}")))

        verified = verification > verification_threshold

        self.ver.text = "Verified" if verification==True else "Unverified"
        return results, verified

if __name__ == "__main__":
    utils.copy_model_n_data()
    CamApp().run()