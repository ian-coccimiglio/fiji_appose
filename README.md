# Fiji with Appose
Fiji implements some programming languages - Java, Jython, and Groovy for example - which operate within the Java Virtual Machine. However, these scripting languages do not normally have access to modern Python3 packages and environment management (e.g., Conda). This meant that certain functionalities were often difficult to implement:
1) Creating/Building/Activating Conda environments
2) Run processes within the environment
3) Pass data between environments

Appose addresses these issues by implementing Interprocess Cooperation with Shared Memory.

## Operating Interprocess:
Conceptually, appose should be thought of as a way of communicating between Java and Python.

In practice, implementing this can be very simple. This code will first build a conda environment, and then print out the version of Python running in it.
```python
#@ File (label="Select a Conda/Mamba Environment") env_path
from org.apposed.appose import Appose
from ij import IJ

IJ.showStatus("Building Environment")
your_python_code = """
import sys
sys.version.split(' ')[0] # returns the version of Python in this environment.
"""

env = Appose.conda(env_path).logDebug().build()
service = env.python()
try:
    task = service.task(your_python_code)
    task.start()
    task.waitFor()
    result = task.outputs.get("result")
    print("Python version is: " + result)
except Exception as e:
    print("Oops, an error occurred:", e)
```

**Important:**
- Appose needs to be installed/available on both the caller side (appose-java), and in the specific conda environment (appose-python) 
- When python code is being run in a `task`, the `task` can be queried, interacted with, and updated to send information back to the caller. 
```python
your_python_code = """
import sys
task.update(message="importing libraries")
sys.version.split(' ')[0] # returns the version of Python in this environment.
"""
``` 

## Task Status and Response types
Often you'll want java (main thread) to query the python (subthread) program to determine and control what's happening in the thread. So each task runs through a standard loop of being initalized/launched, then running/updated, and finally completed/crashed/failed/canceled. We can query these with the following attributes.

| Task Status (Java)  | Response Type (Python) | Indicates task |
| :------------------: | :-----------: | :---------------------------: | 
| QUEUED               |               | has been placed in the queue | 
| INITIAL              |   LAUNCH      | had a successful execute request |
| RUNNING              |               | program is running | 
|                      |  UPDATE       | has been updated |
| COMPLETE             |  COMPLETION   | has been completed and returns the output |
| CANCELED             |  CANCELATION  | was canceled |
| FAILED               |  FAILURE      | did not complete, and error/exception was raised |
| CRASHED              |  CRASH        | has crashed |

## Code samples
### TODO

| Basic Tasks | Example Java Code | Example Jython code |
| :------------: | :----------- | :---------------|
| Build conda environment | <pre lang="java">import org.apposed.appose.Appose&#13;Environment env = Appose&#13;  .conda("/path/to/environment.yml")&#13;  .logDebug()&#13;  .build();</pre> | <pre lang="python">from org.apposed.appose import Appose&#13;env_path="/path/to/environment.yml"&#13;env = Appose.conda(env_path).logDebug().build()</pre>
| Start a service | <pre lang="java">import org.apposed.appose.Service&#13;try (Service service = env.python()) {&#13;// Python/Groovy task management &#13;}</pre> | <pre lang="python">service = env.python()&#13;try:&#13;    # Python/Groovy task management&#13;except Exception as e:&#13;    print("Oops, an error occurred:", e)</pre> |
| Create a task | <pre lang="java">String your_python_code="""&#13;import sys&#13;sys.version.split(' ')[0] # returns Python version.&#13;"""&#13;Task task = service.task(your_python_code);</pre> | <pre lang="python">your_python_code="""&#13;import sys&#13;sys.version.split(' ')[0] # returns the version of Python in this environment.&#13;"""&#13;task = service.task(your_python_code):</pre> |  |
| Create a task listener | <pre lang="java">task.listen(event -> {&#13;  switch (event.responseType) {&#13;    case LAUNCH&#13;      System.out.println("Task started");&#13;      break;&#13;    case UPDATE&#13;      System.out.println(task.message);&#13;      break;&#13;  }&#13;});</pre> | <pre lang="python">from java.util.function import Consumer&#13;&#13;class TaskEventConsumer(Consumer):&#13;    def accept(self, event):&#13;        response_type = event.responseType&#13;        if response_type == response_type.LAUNCH:&#13;            print("[LAUNCH] Task started")&#13;        if response_type == response_type.UPDATE:&#13;            print("[UPDATE] " + task.message)&#13;task.listen(TaskEventConsumer())</pre>|
| Start a task | <pre lang="java">task.start();</pre> | <pre lang="python">task.start();</pre> |
| Wait for task completion | <pre lang="java">task.waitFor();</pre> | <pre lang="python">task.waitFor();</pre> |
| Get task output | <pre lang="java">Object result = task.outputs.get("result")</pre> | <pre lang="python">result=task.outputs.get("result")</pre> |

### TODO

| Intermediate Tasks | Example Java Code | Example Jython code |
| :------------: | :----------- | :---------------|
| Passing parameter as input | <pre lang="java">import java.util.Map&#13;import java.util.HashMap&#13;final Map< String, Object > inputs = new HashMap<>();&#13;inputs.put( "num", 100);</pre> | <pre lang="python">from java.util import HashMap&#13;inputs = HashMap()&#13;inputs.put("num", 100)</pre> |
| Passing image as input | <pre lang="java">package org.apposed.appose;&#13;import java.nio.FloatBuffer;&#13;import java.util.HashMap;&#13;import java.util.Map;&#13;import static org.apposed.appose.NDArray.Shape.Order.F_ORDER;&#13;&#13;final NDArray.DType dType = NDArray.DType.FLOAT32;&#13;final NDArray.Shape shape = new NDArray.Shape(F_ORDER, 4, 3, 2);&#13;final NDArray ndArray = new NDArray(dType, shape);&#13;final FloatBuffer buf = ndArray.buffer().asFloatBuffer();&#13;final long len = ndArray.shape().numElements();&#13;for ( int i = 0; i < len; ++i ){&#13;  buf.put(i, i);&#13;}&#13;final Map< String, Object > inputs = new HashMap<>();&#13;inputs.put("img", ndArray);&#13;try (Service service = env.python()) {&#13; Service.Task task = service.task(your_python_code, inputs);&#13;}</pre> | <pre lang="python">from org.apposed.appose import Appose, NDArray&#13;dType = NDArray.DType.FLOAT32&#13;imp = IJ.getImage()&#13;ip = imp.getProcessor()&#13;shape = NDArray.Shape(NDArray.Shape.Order.F_ORDER, imp.getWidth(), imp.getHeight(), 1)&#13;ndArray = NDArray(dType, shape)&#13;buf = ndArray.buffer().asFloatBuffer()&#13;len = ndArray.shape().numElements()&#13;for i in range(len):&#13;    buf.put(i,ip.getf(int(i)))&#13;inputs.put("img", ndArray)&#13;try:&#13;    service.task(your_python_code, inputs)</pre> |

### TODO

| Advanced Tasks | Example Java Code | Example Jython code |
| :------------: | :----------- | :---------------|
| Run Napari concurrently with ImageJ |              |                 |
| Pass ROIs between processes |                   |                 |
| Pass nD images between processes |       |      |
