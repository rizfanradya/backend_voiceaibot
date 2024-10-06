import os
import queue
import re
import sys
from google.cloud import speech, texttospeech
import pyaudio
import openai
from utils.config import OPENAI_API_KEY
from pyaudio import PyAudio, paInt16

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "lib/voice_ai_bot_service_account.json"
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream:
    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self: object) -> object:
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> None:
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        frame_count: int,
        time_info: object,
        status_flags: object,
    ) -> object:
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)


def googlecloud_only():
    language_code = "id-ID"
    stt_client = speech.SpeechClient()
    tts_client = texttospeech.TextToSpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
    with MicrophoneStream(RATE, CHUNK) as stream_gcloud:
        audio_generator = stream_gcloud.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = stt_client.streaming_recognize(streaming_config, requests)

        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            overwrite_chars = " " * (num_chars_printed - len(transcript))
            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + "\r")
                sys.stdout.flush()
                num_chars_printed = len(transcript)
            else:
                print(transcript + overwrite_chars)

                # nlp
                try:
                    openai.api_key = OPENAI_API_KEY
                    openai_client = openai
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "user",
                                "content": transcript
                            }
                        ]
                    )
                    response_openai = response.choices[0].message.content
                    print("OpenAI Response:", response_openai)

                    # text to speech
                    try:
                        synthesis_input = texttospeech.SynthesisInput(
                            text=response_openai
                        )
                        voice = texttospeech.VoiceSelectionParams(
                            language_code='id-ID',
                            name='id-ID-Wavenet-D'
                        )
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                            sample_rate_hertz=16000
                        )
                        tts_response = tts_client.synthesize_speech(
                            input=synthesis_input,
                            voice=voice,
                            audio_config=audio_config
                        )
                        p_audio = PyAudio()
                        tts_stream = p_audio.open(
                            format=paInt16,
                            channels=1,
                            rate=16000,
                            output=True
                        )
                        tts_stream.write(tts_response.audio_content)
                        tts_stream.stop_stream()
                        tts_stream.close()
                        p_audio.terminate()
                    except Exception as error:
                        print(error)
                except Exception as error:
                    print(error)

                if re.search(r"\b(exit|quit)\b", transcript, re.I):
                    print("Exiting..")
                    break
                num_chars_printed = 0
