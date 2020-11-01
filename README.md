# Mirror

_See thyself through the lens of code._


TODO

- Add MIT license thing to emotion detection code
- Add a license
- Make the thing open source ;) (think whether to move to github and do it as a group; could then simply have a link here and say the project moved)
- Think of ways to have emotion detection improve over time (like with active learning)



## The Vision

Simply speaking, the purpose of this project is to develop software
that assists you in exploring yourself.

The central tool for this self exploration is the Mirror, which enables you to log and analyze different aspects
of your own behavior as you interact with your computer.


### Use Cases

To make the goal somewhat more concrete, consider the following example use cases:

- You may want to find out more about what makes you happy, sad or angry when you are interacting with your computer. You can use Mirror to detect and log your emotions based on the video stream from your webcam, and then find correlations to contents you are viewing on your screen. [Status: basic version of emotion logging is there, but analysis still needs to be extended]
- You might want to know how often and how long you are distracted during work. [Status: Not yet done]

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
a longer term goal is to have the Mirror also actively assist you in making any changes to your behavior,
so that you can optimize any measurable outcomes which you define (e.g. limit distractions or stay more relaxed during work).



The hope is that eventually a community will grow around that software, where extensions to the software are shared with others and new ideas for using the software creatively emerge.


### About Shards, Mirrors and Lenses

TODO formulate that nicely

- Metaphor:
    - We build a "mirror" out of individual "shards" that reflect individual properties of you and your behavior back onto you
    - We, our behavior and even our perception would thus be considered as light, or "rays" of light
    - The idea is that all of this is already there and we can decide to hold up shards to reflect it back at us
    - Analyzing would be done by holding a "lens" into the reflected light, the results still being rays, but potentially different types of rays
    - The Mirror (probably implemented on shards level) can also "memorize", forming "memories" of the rays that passed through
    - Memories can then be played back by "remembering"
    - For visualization, we might introduce something like "screen" or "display"
    - For more artistic stuff we could also consider "loops", to break the whole analogy and get deeper
    - Can also have other entities that are not a part of Mirror or lenses anymore, but just use it as interface
- Observation and logging ("shards" to form the mirror): Need to make it easy for people to add other things to log and configure what is logged
    - Any shard takes in the current state (which might be done with additional tools like emotion detection)
    - As output we have something that is observed at this moment
    - Logging is not done by the shard but by the mirror (or some similar entity that combines results)
- Analyzer should be quite generic, starting with correlation analysis
- Visualization (bit later):
    - evaluate the logs live to give direct feedback
    - artistic stuff like displaying the web capture but altering it
    - can even be a chatbot or similar agent that gives you feedback, telling you when to take breaks, calm down etc.



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
- Adjust the configurations in `config.py`


### Running the Mirror

- The simplest way to run a Mirror is to call `python run.py`
- Adjust `run.py` to use the Mirror in any of the following modes:
    - Viewing: The Mirror observes and processes what is going on and gives you real-time feedback
    - Logging: Instead (or on top) of giving real-time feedback, the Mirror stores its reflections on the hard disk
    - Dreaming: The Mirror simulates previously logged states and gives feedback about them (like Viewing, but with data from the past)
- Which data is processed by the Mirror and what is displayed can be adjusted by configuring the Mirror:
    - Shards are individual modules which capture particular data (e.g. CamShard captures frames from the webcam)
    - The Lens that is used decides which of the data from the Shards is displayed to the user and how this is done (e.g. CamLens shows the frames captured by the webcam in a stream)


### Analyzing your Data

- Currently all the code for analysis resides in the jupyter notebook `analysis.ipynb`
- However, the plan is to extend this part quite a bit (see below)



## Code Structure

- The core of this repository is the [Mirror](mirror.py)
    - A Mirror contains a list of Shards, where each Shard captures a particular type of data
    - Mirrors can also use a Lens, which describes how the captured data is displayed to the user
- Basic Shards are described in [shards/](shards/)
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

- For some windows (like browser), get more finegrained information
- Detect when multiple windows are used (like watching udemy on left side but taking notes on right)
- Use other sources of information:
    - Log what is typed (be careful not to log passwords and similar data though)
    - Mouse movement and clicks (even the way how dynamically one moves the mouse might be telling about emotions)

NOTE: WindowShard only works in linux, as it uses the tool `xprop` under the hood.


