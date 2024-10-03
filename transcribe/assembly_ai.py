import assemblyai as aai
from utils.config import ASSEMBLYAI_API_KEY
from nlp.open_ai import nlp_openai
from audio.elevenlabs_ai import audio_elevenlabs


def transcribe_assembly_ai():
    aai.settings.api_key = ASSEMBLYAI_API_KEY   
    # config = aai.TranscriptionConfig(language_code="id", speech_model=aai.SpeechModel.nano)
    # transcriber = aai.Transcriber(config=config)

    final_transcript = []

    def on_open(session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)

    def on_error(error: aai.RealtimeError):
        print("An error occurred:", error)

    def on_close():
        print("Closing Session")

    def on_data(transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print("Final transcript:", transcript.text)
            final_transcript.append(transcript.text)
            nlp = nlp_openai(transcript.text)
            print("ChatGPT Response:", nlp)
            audio_elevenlabs(nlp)
        else:
            print(transcript.text, end="\r")

    transcriber = aai.RealtimeTranscriber(
        sample_rate=16000,
        on_data=on_data,
        on_error=on_error,
        on_open=on_open,
        on_close=on_close,
        end_utterance_silence_threshold=1000
    )
    transcriber.connect()
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
    transcriber.stream(microphone_stream)
    transcriber.close()
    return " ".join(final_transcript)
