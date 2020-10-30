# Mirror

Next steps could be:

- Properly formulate long-term vision
- Make the thing open source ;)
- Think of ways to have emotion detection improve over time (like with active learning)


## The Vision

TODO explain main metaphors and where this project shall go

- Develop a tool to help people understand themselves
    - Putting you completely in charge regarding what you log, what you analyze and whether or not you share that with anyone
    - Decide what you care about and analyze exactly that: Should be possible to use annotation to make the system detect and log what you really care about (like stress, certain emotions, happiness etc.)
    - Analysis should give you more objective grounds to see what is actually good for you, breaking free from everyday manipulation
- Build a community around that
    - Share trained models and extensions with others
    - Discuss insights and share ideas for using the software creatively
    - Could even consider sharing some of the data with the community for more comprehensive studies or even research projects


## Usage

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


## Requirements

- OpenCV: `pip install opencv-python` (note that on debian, version 4.4.0.44 causes issues, but 4.2.0.34 works)
- PyTorch
- Torchvision
- facenet-pytorch
- pyscreenshot
- jupyter (for analysis part)
- matplotlib (for analysis)
