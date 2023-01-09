import numpy as np
from PIL import Image
import seaborn as sns
#import cv2 
import matplotlib.pyplot as plt
import io
import json
import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras.models import load_model
import gc

height = 128
width = 256


def np_array_to_image(array_image_file) :
    img = np.array(array_image_file)
    img = Image.fromarray((img*255).astype(np.uint8))
    return img


def give_color_to_seg_img(seg_array, n_classes=8):
    seg_img = np.zeros( (seg_array.shape[0],seg_array.shape[1],3) ).astype('float')
    colors = sns.color_palette("hls", n_classes)
    for c in range(n_classes):
        segc = (seg_array == c)
        seg_img[:,:,0] += (segc*( colors[c][0] ))
        seg_img[:,:,1] += (segc*( colors[c][1] ))
        seg_img[:,:,2] += (segc*( colors[c][2] ))
    return(seg_img)


def process(path_to_img, height=height, width= width) :
    # Image ========================================================
    img = Image.open(path_to_img)
    newsize = (width ,height)
    img = img.resize(newsize)
    img_array = np.array(img)
    #img_array = cv2.resize(img_array, (width ,height ))
    img_array = np.asarray(img_array, dtype=np.float32) / 255.
    # Prediction ====================================================
    img_for_pred = np.reshape(img_array, (1, height, width, 3))
    # load the model
    model_file_name = 'best_model_Unet_special_for_api_light_config_api.h5'
    model = keras.models.load_model( model_file_name )
    # Make pred
    pred = model.predict(img_for_pred)
  

    y_pred = tf.math.argmax(pred, axis=-1)
    y_pred_to_array = np.array(y_pred)
    # Reshape for creating the image mask
    pred_mask_to_mak_image = np.squeeze(y_pred_to_array)
    # Make array 3 Cannels with colors
    seg_img = give_color_to_seg_img(pred_mask_to_mak_image)
    # Make image
    mask_img = np_array_to_image(seg_img)
    # Image resizing
    img = np_array_to_image(img_array)
    # Merge both img and mask
    imgs = Image.blend(img, mask_img, 0.6)

    del img_array, img_for_pred, model, pred, y_pred, y_pred_to_array, pred_mask_to_mak_image, seg_img
    gc.collect()

    return img, mask_img, imgs
