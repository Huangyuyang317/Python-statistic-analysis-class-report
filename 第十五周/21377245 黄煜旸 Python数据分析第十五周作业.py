import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from IPython import display

class DataAnalysis:
    def __init__(self, datas):
        self.datas = datas
        self.datadic = dict()
    
    def read_data(self):
        for file in self.datas:
            self.datadic[file]=pd.read_csv(file)
    def time_analysis(self,place,pollution):
        i=0
        for file in self.datas:
            if place in file:
                filename=file
                i=1
                break
        if i==0:
            raise ValueError("No correct place detected")
        data=self.datadic[filename]
        y=data[pollution].tolist()
        x_raw=[str(data['year'].tolist()[i])+'-'+str(data['month'].tolist()[i])+'-'+str(data['day'].tolist()[i])+' '+str(data['hour'].tolist()[i])+':00:00' for i in range(len(data['year'].tolist()))]
        x=[datetime.strptime(raw, '%Y-%m-%d %H:%M:%S') for raw in x_raw]
        return x,y
    
class DataVisualization():
    def __init__(self, x,y):
        self.x=x
        self.y=y
    def time_visualization(self):
        display.set_matplotlib_formats('svg')
        if len(self.x) == len(self.y):
            plt.figure(figsize=(9,3))
            xlimit=(x[0],x[-1])
            label='pollution'
            fileName='pollution.svg'
            if xlimit and isinstance(xlimit, tuple):
                plt.xlim(xlimit)
            plt.plot(x, y, label=label)
            if label and isinstance(label, str):
                plt.legend()
            if fileName:
                plt.savefig(fileName)
            plt.show()


data_path = r"C:\Users\HenryYoung\Desktop\PRSA_Data_20130301-20170228"
files=[str(os.path.join(data_path,file)) for file in os.listdir(data_path)]
analysis=DataAnalysis(files)
analysis.read_data()
x,y=analysis.time_analysis('Aotizhongxin','SO2')
DataVisualization(x,y).time_visualization()

