from PIL import Image
import numpy as np
import os
class FaceDataset():
    def __init__(self,path):
        self.path=path
        self._path=[]
        for root, dirs, files in os.walk(self.path):
            for name in files:
                self._path.append(os.path.join(root, name))
        self.len=len(self._path)
    def image_generator(self):
        for path in self.img_path:
            im=Image.open(path)
            yield np.asarray(im)
    def __iter__(self):
        self.num=0
        return self
    def __next__(self):
        if self.num>=self.len:
            raise StopIteration
        else:
            ipath=self.img_path[self.num]
            im=Image.open(ipath)
            self.num+=1
            return np.asarray(im)
real_face=FaceDataset(r'C:\Users\黄煜旸\Desktop\originalPics')
for im in real_face:
    print(im.shape)

