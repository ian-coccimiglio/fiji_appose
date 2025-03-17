#@ File (label="Select a Conda/Mamba Environment") env_path
from org.apposed.appose import Appose
from ij import IJ


IJ.showStatus("Building Environment")
env = Appose.conda(env_path).logDebug().build()
service = env.python()
your_python_code = """
import sys
sys.version.split(' ')[0] # returns the version of Python in this environment.
"""

try:
	task = service.task(your_python_code)
	task.start()
	task.waitFor()
	result = task.outputs.get("result")
	print("Python version is: " + result)
except Exception as e:
    print("Oops, an error occurred:", e)