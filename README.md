# Fiji with Appose
Fiji has a few main scripting languages - Python and Groovy - which operate within the Java Virtual Machine.

Often, it is important to do a few key tasks that can't be done solely within Java:
1) Create a specific non-Java environment
2) Run processes within the environment
3) Pass data between environments

## Operating Interprocess:
So there's a need to be able to operate between processes.
- Java environment operating a Python environment
- Java environment operating a Groovy environment


| Task Status (Java)  | Response Type (Python) | Indicates |
| :------------------: | :-----------: | ---------------------------: |
| QUEUED               |               | Java put a task in the queue |
| INITIAL              |   LAUNCH      | The task had a successful execute request |
| RUNNING              |  UPDATE       | The program is running / has been updated |
| COMPLETE             |  COMPLETION   | The task has been completed and returns the output |
| CANCELED             |  CANCELATION  | The task was canceled |
| FAILED               |  FAILURE      | The task did not complete, and error/exception was raised |
| CRASHED              |  CRASH        | The task has crashed |

