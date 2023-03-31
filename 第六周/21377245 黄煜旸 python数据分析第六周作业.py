from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessor():
    def __init__(self,image) :
        self.image=image
        self.arg=[]
    def process(self):
        pass

class GrayScale(ImageProcessor):
    def __init__(self,image):
        super().__init__(image)
    def process(self):
        gray_image=self.image.convert('L')
        return gray_image

class Crop(ImageProcessor):
    def __init__(self,image,x0=50,y0=50,x1=250,y1=250):
        super().__init__(image)
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1
    def process(self):
        cut_image=self.image.crop(x0,y0,x1,y1)
        return cut_image
class Blur(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
    def process(self):
        blur_image=self.image.filter(ImageFilter.BLUR)
        return blur_image

class Edge(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
    def process(self):
        edge_image=self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return edge_image
    
class ImageShop():
    def __init__(self,form,index):
        self.form=form
        self.index=index
        self.im=[]
        self.pro_im=[]
    def load_images(self):
        for i in self.index:
            self.im.append(Image.open(i))
    def __batch_ps(self,Processor):
        Processor.process().show()
        self.pro_im.append(Processor.process())
    def batch_ps(self,*args):
        for i in range(len(self.im)):
            if args[i] == 'gray':
                self.__batch_ps(GrayScale(self.im[i]))
            elif args[i] == 'crop':
                self.__batch_ps(Crop(self.im[i]))
            elif args[i] == 'blur':
                self.__batch_ps(Blur(self.im[i]))
            elif args[i] == 'edge':
                self.__batch_ps(Edge(self.im[i]))
    def save(self):
        for i in range(len(self.pro_im)):
            filename = f"processed_{i+1}.{self.form}"
            self.pro_im[i].save(filename)


shop=ImageShop('jpg',[r'C:\Users\黄煜旸\Desktop\1.jpg',r'C:\Users\黄煜旸\Desktop\2.jpg',r'C:\Users\黄煜旸\Desktop\3.jpg'])
shop.load_images()
shop.batch_ps('gray','blur','edge')
shop.save()

        