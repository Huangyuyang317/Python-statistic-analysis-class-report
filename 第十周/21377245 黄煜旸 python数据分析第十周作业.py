from abc import ABCMeta, abstractmethod
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Point():
    def __init__(self,x,y):
        self.x=x
        self.y=y


class Plotter(metaclass=ABCMeta):
    def __init__(self):
        pass
    
    @abstractmethod
    def plot(self,*args,**kwargs):
        pass


class PointPlotter(Plotter):
    def __init__(self):
        super().__init__()

    def plot(self,data,*args,**kwargs):
        x1=[]
        y1=[]
        for i in range(len(data)):
            x1.append(data[i].x)
            y1.append(data[i].y)
        plt.scatter(x1,y1)
        plt.show()
    
class ArrayPlotter(Plotter):
    def __init__(self):
        super().__init__()
        
    def plot(self,data,*args,**kwargs):
        if len(data[0])==2:
            x1=[]
            y1=[]
            for i in range(len(data)):
                x1.append(data[i][0])
                y1.append(data[i][1])
            plt.scatter(x1,y1)
            plt.show()
        if len(data[0])==3:
            x1=[]
            y1=[]
            z1=[]
            ax = plt.subplot(projection = '3d')
            for i in range(len(data)):
                x1.append(data[i][0])
                y1.append(data[i][1])
                z1.append(data[i][2])
            ax.scatter(x1,y1,z1)
            plt.show()

data1=[Point(1,3),Point(2,7),Point(6,9),Point(11,30),Point(15,32)]
point=PointPlotter()
point.plot(data1)

data2=[[1,3,9],[2,7,10],[5,3,6],[10,15,18]]
array=ArrayPlotter()
array.plot(data2)