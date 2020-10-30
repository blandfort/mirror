# Mirror

_See thyself through the lens of code._


Next steps could be:

- Properly formulate long-term vision
- Add MIT license thing to emotion detection code
- Add a license
- Make the thing open source ;) (think whether to move to github and do it as a group; could then simply have a link here and say the project moved)
- Think of ways to have emotion detection improve over time (like with active learning)


## The Vision

TODO explain what the status is and where this project shall go (this has to be easy to understand; include examples)

The purpose of this project is to develop software which helps you to learn more about who you are
and assists you in making whatever changes you'd like to make.


- Develop a tool to help people understand themselves
    - Putting you completely in charge regarding what you log, what you analyze and whether or not you share that with anyone
    - Decide what you care about and analyze exactly that: Should be possible to use annotation to make the system detect and log what you really care about (like stress, certain emotions, happiness etc.)
    - Analysis should give you more objective grounds to see what is actually good for you, breaking free from everyday manipulation

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


