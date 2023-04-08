
# imports
import os
from distutils.dir_util import copy_tree
import shutil
import time
import cv2

CUR_DIR = "."
OLD_APP_DIR = "../Facial Recognition with a Siamese Network/app_data"
APP_DIR = "./app_data"
VER_DIR = "ver_images"
INP_DIR = "input_images"
H5_PATH = "../Facial Recognition with a Siamese Network/training_checkpoints/siamesenetwork.h5"
MODEL_PATH = "./siamese_network.h5"
# Variables used
CAM_POS = 2 # Change this value accordingly to the pos of the camera youre using
X_CAM_POS = 230
Y_CAM_POS = 90
FRAME = 250

def copy_model_n_data():
    # Copy Images from Data used in model
    if not os.path.isdir(APP_DIR) and os.path.isdir(OLD_APP_DIR):
        copy_tree(OLD_APP_DIR,APP_DIR)

    # Copy h5 model, verifies if exists
    if not os.path.isfile(MODEL_PATH) and os.path.isfile(H5_PATH):
        shutil.copy(H5_PATH,CUR_DIR)

def get_ver_images(cap):
    i=0
    while i<10:

        ret,frame = cap.read()
        
        frame = frame[Y_CAM_POS:Y_CAM_POS+FRAME,X_CAM_POS:X_CAM_POS+FRAME]

        cv2.imshow("Verification", frame)

        time.sleep(0.05)
        cv2.imwrite(os.path.join(f"{APP_DIR}/{INP_DIR}",f"input_img{i}.jpg"), frame)
        i+=1