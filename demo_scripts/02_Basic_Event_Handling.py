#@ File (label="Select a Conda/Mamba Environment") env_path
from org.apposed.appose import Appose, TaskEvent
from ij import IJ
from java.util.function import Consumer

IJ.showStatus("Building Environment")
env = Appose.conda(env_path).logDebug().build()
service = env.python()
your_python_code = """
from random import choice
jukebox = ["Queen: Somebody to Love", "GLaDOS: Still Alive ", "Billy Joel: Piano Man", "Sum 41: Walking Disaster", "Rebecca Black: Friday", "Samuel E. Wright: Under the Sea", "Simon and Garfunkel: The Sound of Silence", "Camila Cabello: Havana", "David Bowie: Starman"]

num_songs = 0
keep_playing = 1
task.update(message=f"Starting jukebox")
while (keep_playing == 1):
	current_song = choice(jukebox)
	num_songs += 1
	if current_song == "Simon and Garfunkel: The Sound of Silence":
		keep_playing = 0
	task.update(message=f"Currently playing: {current_song}", current=num_songs)
	
f"Number of songs played: {num_songs}"
"""
class TaskEventConsumer(Consumer):
    def accept(self, event):
        # Access properties of the TaskEvent
        task = event.task
        response_type = event.responseType
        
        # Insert your event handling logic
        # print("Task status/response: {}/{}".format(task.status, response_type))
        if response_type == response_type.LAUNCH:
            print("[LAUNCH] The task launched successfully")
        if response_type == response_type.UPDATE:
            print("[UPDATE] " + task.message + "\t\t\t" + str(task.current))
        if response_type == response_type.COMPLETION:
            print("[COMPLETION] The task is over!")
        if response_type == response_type.FAILURE:
            print("[ERROR]\n" + task.error)
try:
	task = service.task(your_python_code)
	task.listen(TaskEventConsumer())
	task.start()
	task.waitFor()
	result = task.outputs.get("result")
	print(result)
except Exception as e:
    print("An error occurred:", e)

