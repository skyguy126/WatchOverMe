from AudioCapture import AudioCapture
import signal, keras, json, requests
import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
from process_waveform import process_waveform
from comms import send_sms
import scipy.io.wavfile

signal.signal(signal.SIGINT, signal.SIG_DFL)
secure = None

def broadcast():
    payload = {"key" : "c1", "val" : True}
    r = requests.post("http://73.223.184.186:25565/change", json=payload)
    print("requests called: " + str(r.status_code))
    msg = "Warning, potential incident detected at the UCLA Medical Center. Click here for more information: http://watchoverme.net:25565/"
    send_sms(secure["twilio_acct_sid"], secure["twilio_api_key"], secure["twilio_number"], secure["contact_numbers"], msg)

def get_clip_bounds(data, threshold, index):
    length = len(data)

    b1 = index - threshold
    b2 = index + threshold

    if b1 < 0: b1 = 0
    if b2 > length: b2 = length - 1

    return data[b1 : b2]

if __name__ == "__main__":

    # Load secure params

    with open('secure.json', 'r') as f:
        secure = json.loads(f.read())

    # Load model and weights

    model = None
    with open('model.json', 'r') as f:
        model = model_from_json(f.read())

    model.load_weights('weights.h5')

    a = AudioCapture(1)
    a.setup()

    for x in range(1000):
        print("getting data...")
        data = a.record()
        print(str(len(data)))

        amp_peak_index = np.argmax(np.abs(np.array(data)))
        amp_peak = abs(data[amp_peak_index])
        print(str(amp_peak))

        if amp_peak > 2000:
            sub = get_clip_bounds(data, 2022, amp_peak_index)
            output = process_waveform(sub)

            #plt.plot(sub)
            #plt.show()

            '''
            is_clap = int(input("is clap: "))
            f_name = None
            if is_clap == 1:
                f_name = "clap" + str(x) + ".wav"
            else:
                f_name = "noclap" + str(x) + ".wav"
            scipy.io.wavfile.write(f_name, 44100, sub)
            '''

            prediction_confidence = model.predict(output.reshape(1, 32, 32, 1))
            prediction = np.argmax(prediction_confidence)
            print("confidence: " + str(prediction_confidence))
            print("prediction: " + str(prediction))
            if prediction == 1: broadcast()
        else:
            print("failed to reach threshold, ignoring...")
