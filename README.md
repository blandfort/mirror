# Mirror

Next steps could be:

- Clean up the repo, add some documentation
    - Properly describe the code structure
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


## Code Structure

TODO explain overall structure, what kind of modules we have and how the flow is

### Overview

- Mirror: highest level, containing Shards and optionally a Lens
    - Shard
        - Memory: Can be used to store data of a certain type 
    - Lens


### Analysis

Also do:

- Analyze some correlations, see if it makes any sense
- Create reports (so that e.g. end of the week you can view a summary)


### Logging Behavior

Room for improvement:

- For some windows (like browser), get more finegrained information
- Detect when multiple windows are used (like watching udemy on left side but taking notes on right)
- Use other sources of information:
    - Log what is typed (be careful not to log passwords and similar data though)
    - Mouse movement and clicks (even the way how dynamically one moves the mouse might be telling about emotions)


## Requirements

- OpenCV: `pip install opencv-python` (note that on debian, version 4.4.0.44 causes issues, but 4.2.0.34 works)
- PyTorch
- Torchvision
- facenet-pytorch
- pyscreenshot
- jupyter (for analysis part)
- matplotlib (for analysis)
