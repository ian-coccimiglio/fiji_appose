#@ File (label="Select a Conda/Mamba Environment") env_path
from org.apposed.appose import Appose, NDArray
from java.util import Map, HashMap
from java.util.function import Consumer
from ij import IJ
from jy_tools import attrs

IJ.showStatus("Building Environment")
env = Appose.conda(env_path).logDebug().build()
service = env.python()
your_python_code = """
import sys
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from skimage.io import imshow
imshow(num.ndarray()[0])
sleep(50)
# ax = plt.plot(np.sqrt(num.ndarray()[0]))
# import napari
# viewer = napari.Viewer()
# napari.run()
"""
dType = NDArray.DType.FLOAT32;
imp = IJ.getImage()
ip = imp.getProcessor()
shape = NDArray.Shape(NDArray.Shape.Order.F_ORDER, imp.getWidth(), imp.getHeight(), 1)
ndArray = NDArray(dType, shape)
buf = ndArray.buffer().asFloatBuffer()
len = ndArray.shape().numElements()
for i in range(len): 
	buf.put(i,ip.getf(int(i)))

class TaskEventConsumer(Consumer):
    def accept(self, event):
        # Access properties of the TaskEvent
        task = event.task
        response_type = event.responseType
        # Insert your event handling logic
        if response_type == response_type.FAILURE:
        	print("[ERROR]\n" + task.error)
try:
	inputs = HashMap()
	
	inputs.put("num", ndArray)
	task = service.task(your_python_code, inputs)
	task.listen(TaskEventConsumer())
	task.start()
	task.waitFor()
	result = task.outputs.get("result")
	print result
	# print("Python version is: " + result)
except Exception as e:
    print("Oops, an error occurred:", e)