# Mirror

Next steps could be:

- Log for some time on a few different days
- Then analyze correlations, see if it makes sense
    - Consider postprocessing to account for problems with the detection
    - Think of ways to have emmotion detection improve over time (like with active learning)
- Clean up the repo, add some documentation, properly formulate long-term vision and make the thing open source


## On the Vision

- Develop a tool to help people understand themselves
    - Putting you completely in charge regarding what you log, what you analyze and whether or not you share that with anyone
    - Decide what you care about and analyze exactly that: Should be possible to use annotation to make the system detect and log what you really care about (like stress, certain emotions, happiness etc.)
    - Analysis should give you more objective grounds to see what is actually good for you, breaking free from everyday manipulation
- Build a community around that
    - Share trained models and extensions with others
    - Discuss insights and share ideas for using the software creatively
    - Could even consider sharing some of the data with the community for more comprehensive studies or even research projects


## Logging Behavior

Room for improvement:

- For some windows (like browser), get more finegrained information
- Detect when multiple windows are used (like watching udemy on left side but taking notes on right)
- Use other sources of information:
    - Log what is typed (be careful not to log passwords and similar data though)
    - Mouse movement and clicks (even the way how dynamically one moves the mouse might be telling about emotions)


## Emotion Detection

- Model trained on FERPlus seems reasonable already (SOTA on that dataset is not even that high)
    - Happiness is detected alright
    - For negative emotions it seems to be very conservative though
- Display certainty of the model as well
    - Not that bad, the model shows uncertainty in some unusual cases
    - -> Still, model doesn't use softmax at the moment and thus becomes overconfident in stuff; perhaps this has to be adjusted
- To improve further, could try the following:
    - Not only consider majority class (to get also some more subtle expressions)
    - Use additional datasets (compile some samples of aff-wild2, taking few from each video, rescaling and saving in separate directories so it can be read easily)
    - Change model architecture (also consider adding dropout)
    - Augment dataset by introducing noise or changing colors
    - How about active learning with my own webcam data?

Potential extensions:

- Consider audio data as well


## Requirements

- OpenCV: `pip install opencv-python` (note that on debian, version 4.4.0.44 causes issues, but 4.2.0.34 works)
- PyTorch
- Torchvision
- facenet-pytorch
- pyscreenshot
