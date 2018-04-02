# Watch Over Me
### A real-time, city-wide, surveillance system.
![](screenshots/preview.jpg?raw=true)
#### [Website](http://watchoverme.net:25565/) | [Devpost](https://devpost.com/software/watch-over-me)

-----
### Running
```shell
# Convert training data into frequency-time matricies.
# Copy .wav files into the train and test directories.
# Filenames prefixed with no will be trained against the network.
> python2.7 conv_to_img.py

# Train the CNN
> python3.6 ml.py

# Start the client
> python3.6 main.py

# Start the web-server
# python2.7 backend.py
```

#### `secure.json`
This file is required to run the servers and stores your personal API keys. Place it in the project's root directory.
```json
{
    "twilio_acct_sid" : "123456",
    "twilio_api_key" : "123456",
    "twilio_number" : "+1231231234",
    "google_maps_api_key" : "123456",
    "contact_numbers" : [
        "+1231231235",
        "+1231231236"
    ]
}
```

#### Dependencies
- Keras
- Tensorflow
- pyaudio
- requests
- numpy
- scipy
- matplotlib
- Tornado
- Twilio

-----

## Inspiration
We wanted to tackle the increased number of shootings, violence, and crime in dense city blocks, especially around areas where it's hard to maintain 24-hour surveillance. Usually this technology, microphones and a basic processing board, is already available throughout various locations in the block (think of things like Amazon Alexa and Google Home which are always listening) and our algorithm can be deployed very easily.

## What it does
Our platform continuously collects audio samples waits for a sound sample to reach a certain amplitude (perhaps screaming or gun-shots). Once the threshold is passed, the program clips just the specific sound and a few milliseconds before and after and feeds it through a waveform processor. The sound pressure data gets mapped into a frequency domain over time. This is because certain sounds have a very good patterns. For example, a gun-shot would have a rapid rise time and slowly fall off while dropping in frequency. This matrix of data gets fed through our convolutional neural network where further analysis gives us a prediction of whether it was that certain sound or not. If it is, the system automatically reacts, marks a warning zone on a publicly available map, broadcasts warning SMS to nearby people, and alerts police.

#### TLDR;
1. Waits for sound to reach a high volume.
2. Algorithm extracts the sample from a continuous recording.
3. Data is converted into the frequency domain over time and stored in a matrix.
4. Matrix is fed through a neural network to determine if it is the specific sound we are looking for.
5. If yes, update a live map and mark a warning zone and alert nearby users of the danger through Twilio's SMS API.

## How we built it
The core algorithm took quite a bit of thought as this was our first time working with audio and machine learning. We developed a few different tools to help us go through this process smoothly. At the start we were using Audacity to manually record and transform raw audio data to train our network but we soon realized that this would be unfeasible. We developed a tool that would let us automatically record a sound, show a graph of its waveform and let us choose what it would be classified as. Another tool was created to quickly convert the raw data into 32x32 matrices to be fed into the neural network. Keras allowed us to quickly prototype and modify parameters without large changes and took care of most of the math behind the scenes. The live map is served through another back-end server written in Python.

## Challenges we ran into
We didn't know much machine learning or signal processing at the start of all this. Being under a large time constraint we weren't able to generate copious amounts of training data usually necessary to train a solid neural network, although given the constraints the network is very accurate.

## Accomplishments that we're proud of
Devising a convolutional model to detect *claps* (in lieu of gun-shots or screams for obvious reasons) and ignore static noise, background conversations, sudden impulses, etc. Learning about signal processing and machine learning.

## What we learned
Mainly real-time signal processing, machine learning models. Effective full stack development which would need to provide real-time data to multiple devices at a time. And cool APIs provided by the sponsors here at LAHacks!

## What's next for Watch Over Me
Originally we were going to use a trio of microphones to be able to triangulate the exact location of the incident but since we lacked equipment and were restricted to our laptops and phones this plan was put on hold. When we get a with high quality microphones this will definitely be the next step.

-----

##### Developed for LAHacks 2018
