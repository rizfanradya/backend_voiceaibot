import pyaudio
from rev_ai.models import MediaConfig
from rev_ai.streamingclient import RevAiStreamingClient
import six

access_token = "02lFdZhFJJR-Eg74Bgitj0Ud9UXb6HFoss3vupOeyKKvJ9S0U_2X4xo4OZaErkr9KZmdsTp_17_TBj68GpLMRVExLImVg"


class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = six.moves.queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
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
                except six.moves.queue.Empty:
                    break
            yield b''.join(data)


rate = 44100
chunk = int(rate/10)
example_mc = MediaConfig('audio/pcm', 'interleaved', rate, 'S16LE', 1)
streamclient = RevAiStreamingClient(access_token, example_mc)

with MicrophoneStream(rate, chunk) as stream:
    try:
        response_gen = streamclient.start(stream.generator())
        for response in response_gen:
            print(response)
    except KeyboardInterrupt:
        print("Pengguna menghentikan proses.")
    except Exception as error:
        print(f"Kesalahan: {error}")
    finally:
        streamclient.end()
