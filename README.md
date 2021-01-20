# Mirror

_See thyself through the lens of code._


TODO

- Think of ways to have emotion detection improve over time (like with active learning)

__Note:__ This is still a comparatively small early-stage project but I am looking for collaborators to make it grow.
So if the Mirror resonates with you, please reach out ;)


## The Vision

The overall purpose of this project is to develop software
that assists you in exploring yourself, so that you can find out more about what makes you feel,
what your typical behavioral patterns are and in which ways your own view might be biased or limited.

The central tool for this self exploration is the Mirror, which enables you to log and analyze different aspects
of your own behavior as you interact with your computer.


### Use Cases

To make the goal somewhat more concrete, consider the following examplary use cases:

- You may want to find out more about what makes you happy, sad or angry when you are interacting with your computer.
  You can use Mirror to detect and log your emotions based on the video stream from your webcam,
  and then find correlations to contents you are viewing on your screen.
  [Status: Basic version is there, but both analysis and emotion detection should still be improved]
- Find out what is the ratio of contents with positive vs negative sentiment.
  How does it relate to your emotions?
  [Status: Not yet done]
- You might want to know how often and how long you are distracted during work.
  Finding patterns in your distractions (e.g. you might distract yourself when trying to write a mail at certain times of the day)
  with Mirror can be the first step to organizing your work more efficiently.
  [Status: Not yet done]

Note: You are completely in charge. You decide which data to collect, what you analyze and whether or not you share any of that with anyone.


### Future Plans

It is planned to extend the Mirror in various ways:

- Individual components will be improved (see notes below)
- Have the Mirror adapt to you, by means of annotations or other feedback mechanisms:
    - Use active learning to fine-tune emotion detection on your own data
    - Train models to detect classes you define (e.g. you might want to detect whether you look tired based on the webcam capture)
    - Ultimately, you should be able to set your own objectives and have the system learn detect them from the available data
- Additional information sources could be interesting to consider (e.g. data from a fitness tracker)

Apart from helping you to understand yourself better,
a longer term goal is to have the Mirror also actively assist you in making any _changes_ to your behavior,
so that you can optimize any measurable outcomes which you define (e.g. limit distractions or stay more relaxed during work).


## Usage

### Requirements

- OpenCV: `pip install opencv-python` (note that on debian, version 4.4.0.44 causes issues, but 4.2.0.34 works)
- PyTorch
- Torchvision
- facenet-pytorch
- pyscreenshot
- jupyter (for analysis part)
- matplotlib (for analysis)


### Set Up

- Clone the repository
- Make sure that Python is installed (tested with Python 3.7.3)
- Create a virtual environment: `python3 -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `pip install -r requirements.txt`
- Install emotion recognition package: `pip install git+https://github.com/blandfort/emotion_recognition.git`
- Adjust the configurations in [config.py](config.py)


### Running the Mirror

- The simplest way to run a Mirror is to call `python run.py`
- Adjust [run.py](run.py) to use the Mirror in any of the following modes:
    - Viewing: The Mirror observes and processes what is going on and gives you real-time feedback
    - Logging: Instead (or on top) of giving real-time feedback, the Mirror stores its reflections on the hard disk
    - Dreaming: The Mirror simulates previously logged states and gives feedback about them (like Viewing, but with data from the past)
- Which data is processed by the Mirror and what is displayed can be adjusted by configuring the Mirror:
    - Shards are individual modules which capture particular data (e.g. CamShard captures frames from the webcam)
    - The Lens that is used decides which of the data from the Shards is displayed to the user and how this is done (e.g. CamLens shows the frames captured by the webcam in a stream)


### Analyzing your Data

- Currently all the code for analysis resides in the jupyter notebook [analysis.ipynb](analysis.ipynb)
- However, the plan is to extend this part quite a bit (see below)



## Code Structure – About Shards, Mirrors and Lenses

- The core of this repository is the [Mirror](mirror.py)
    - Think of your behavior and the current situation as light, so individual components (e.g. what is done on the screen or what the webcam seens) would form Rays of light
    - A Mirror contains a list of Shards, where each Shard captures a particular Ray
    - Mirrors can also use a Lens, which describes how the captured Rays are displayed to the user
- Basic Shards are described in [shards/](shards/)
    - Any Shard takes in the current state (which might be done with additional tools like emotion detection or communicating with active windows)
    - As output we have something that is observed at this moment by the Shard (e.g. the title of the currently active window or the current frame from the webcam) 
- Basic Lenses can be found in [lenses/](lenses/)
- The Mirror as well as the Shards can use Memory to store their states. Memory classes reside in [memory/](memory/)
- Sometimes we don't want to log all the data for every timestep. For such cases, there are MemoryBlocks, which are described in [blocks/](blocks/) and can be passed when running a Mirror to modify what is being logged
- Additional modules go into their own directories. They generally should define Shards or Lenses to be plugged into the Mirror. For example:
    - [emotions/](emotions/) contains a Shard to detect emotions from the webcam capture, and a Lens to display the result in a modified frame
    - [behavior/](behavior/) has Shards for taking screenshots and observing the title of the currently active window
    - [faces/](faces/) contains a Shard to detect faces in the webcam capture and return a list of face images cropped from the capture


## Modules

### Analysis

Some ideas for next steps:

- Analyze some correlations, see if it makes any sense
- Use Fourier transform to find patterns
- Create reports (so that e.g. end of the week you can view a summary)
- Use forecasting methods and predict which changes lead to a given desired outcome (e.g. make you more happy)


### Behavior

Room for improvement:

- For some windows (like browser), get more finegrained information (e.g. texts viewed in browser)
- Detect when multiple windows are used (like watching udemy on left side but taking notes on right)
- Use other sources of information:
    - Log what is typed (be careful not to log passwords and similar data though)
    - Mouse movement and clicks (even the way how dynamically one moves the mouse might be telling about emotions)

NOTE: WindowShard only works in linux, as it relies on the tool `xprop` under the hood.

