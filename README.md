# Mirror

Next steps could be:

- Log emotions for some time on a few different days, taking notes on own observed state afterwards or logging other activities as well (perhaps screenshots), then check if the log makes any sense
    - Run detection without showing the stream, just give the labels
    - For other data, would be great to also log contents in browser or other applications that are "consumed", to correlate it to
- Then analyze correlations, see if it makes sense
    - Consider postprocessing to account for problems with the detection
    - Think of ways to have emmotion detection improve over time (like with active learning)


## Training own Emotion Detection

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


