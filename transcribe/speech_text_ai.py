import requests
import time
from utils.config import SPEECHTEXTAI_API_KEY
import sounddevice as sd
import scipy.io.wavfile as wav


def record_audio(duration=5, sample_rate=16000, filename="recorded.wav"):
    print("Recording...")
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    wav.write(filename, sample_rate, audio_data)
    print(f"Recording saved as {filename}")


def transcribe_speech_text(audio_file="recorded.wav"):
    with open(audio_file, mode="rb") as file:
        post_body = file.read()

    endpoint = "https://api.speechtext.ai/recognize?"
    header = {'Content-Type': "application/octet-stream"}

    config = {
        "key": SPEECHTEXTAI_API_KEY,
        "language": "en-US",
        "punctuation": True,
        "format": "m4a"
    }

    r = requests.post(
        endpoint,
        headers=header,
        params=config,
        data=post_body
    ).json()

    config = {
        "key": SPEECHTEXTAI_API_KEY,
        "task": r["id"],
        "summary": True,
        "summary_size": 15,
        "highlights": True,
        "max_keywords": 10
    }

    while True:
        endpoint = "https://api.speechtext.ai/results?"
        results = requests.get(endpoint, params=config).json()
        if "status" not in results:
            break
        print("Task status: {}".format(results["status"]))
        if results["status"] == 'failed':
            print("The task is failed: {}".format(results))
            break
        if results["status"] == 'finished':
            break
        time.sleep(15)
    return results
