from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
import os

class MyDecorater(object):
    def __init__(self,f):
        self.f=f

    def __call__(self,*args, **kwargs):
        image_path = args[0]
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        brightness = hsv_image[..., 2].mean()
        saturation = hsv_image[..., 1].mean()
        print(f"Image size: {width} x {height}")
        print(f"Image brightness: {brightness}")
        print(f"Image saturation: {saturation}")

def check(func):
    def wrapper(*args):
        if(os.path.exists(args[0])):
            pass
        else:
            os.mkdir(path)
    return wrapper

class ImageUse():
    def __init__(self,path):
        self._im=path

    def create(self):
        im=Image.open(self._im)
        return im
    
    def shape(self):
        shaped_im=self.create(im).crop(0,0,780,512)
        return shaped_im
    
    @MyDecorater
    def rotate(self,im):
        rotated_im=self.create(im).transpose(Image.ROTATE_270)
        return rotated_im
        
    def edge(self,im):
        edge_im=self.create(im).filter(ImageFilter.EMBOSS)
        return edge_im
    @check
    def save(self,path):
        self.create(im).save(path+'./changed.png')

i=ImageUse(r'C:\Users\黄煜旸\Desktop\test.png')
im1=i.shape()
im2=i.rotate()
im3=i.edge()
i.save(r'C:/Users/黄煜旸/Desktop')
