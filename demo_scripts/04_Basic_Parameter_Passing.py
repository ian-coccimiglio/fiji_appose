#@ File (label="Select a Conda/Mamba Environment") env_path
from org.apposed.appose import Appose
from java.util import Map, HashMap
from java.util.function import Consumer
from ij import IJ

IJ.showStatus("Building Environment")
env = Appose.conda(env_path).logDebug().build()
service = env.python()
your_python_code = """
import numpy as np
np.sqrt(num)
"""

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
	input = 3600
	inputs.put("num", input)
	task = service.task(your_python_code, inputs)
	task.listen(TaskEventConsumer())
	task.start()
	task.waitFor()
	result = task.outputs.get("result")
	print result
except Exception as e:
    print("Oops, an error occurred:", e)