from org.apposed.appose import Appose
from org.apposed.appose import TaskEvent
from java.io import File
from jy_tools import attrs, reload_modules
from java.util.function import Consumer

reload_modules(force=True, verbose=True)
env = Appose.conda(File("/home/ian/Documents/Appose/Fiji_Appose/cell_appose.yml")).logDebug().build()
service = env.python()
your_python_code = """
import sys
task.update(message=f"Python version is {sys.version}")
task.update(message="Loading Cellpose")
from cellpose import models
import cellpose
task.update(message=f"Cellpose Version: {cellpose.version}")
task.update(message=f"Cellpose GPU Available: {models.torch.cuda.is_available()}")
"""
class TaskEventConsumer(Consumer):
    def accept(self, event):
        # Access properties of the TaskEvent
        task = event.task
        response_type = event.responseType
        
        # Your event handling logic here
        if response_type == response_type.UPDATE:
        	print("[UPDATE] " + task.message)

try:
	task = service.task(your_python_code)
	task.listen(TaskEventConsumer())
	task.start()
	task.waitFor()
	
	# attrs(task, method=False)
	result = task.outputs.get("result")
	print("Python version is: " + result)
except Exception as e:
    print("An error occurred:", e)

