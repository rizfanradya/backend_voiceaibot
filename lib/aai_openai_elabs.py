import assemblyai as aai
from utils.config import ASSEMBLYAI_API_KEY, OPENAI_API_KEY, ELEVENLABS_API_KEY
import openai
from elevenlabs.client import ElevenLabs
from elevenlabs import (
    VoiceSettings,
    stream
)


def assemblyai_openai_elevenlabs():
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    # config = aai.TranscriptionConfig(language_code="id", speech_model=aai.SpeechModel.nano)
    # transcriber = aai.Transcriber(config=config)

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

            # openai
            try:
                openai.api_key = OPENAI_API_KEY
                openai_client = openai
                response_openai = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                          "role": "user",
                          "content": transcript.text
                        }
                    ]
                )
                results = response_openai.choices[0].message.content
                print("ChatGPT Response:", results)

                # elevenlabs
                try:
                    audio_stream = ElevenLabs(api_key=ELEVENLABS_API_KEY)
                    response_elevenlabs = audio_stream.text_to_speech.convert(
                        # voice_id="pNInz6obpgDQGcFmaJgB",
                        voice_id="EXAVITQu4vr4xnSDxMaL",
                        output_format="mp3_22050_32",
                        text=results,
                        model_id="eleven_multilingual_v2",
                        voice_settings=VoiceSettings(
                            stability=0.8,
                            similarity_boost=1.0,
                            style=0.0,
                            use_speaker_boost=True,
                        ),
                    )
                    stream(response_elevenlabs)
                    assemblyai_openai_elevenlabs()
                except Exception as ele_error:
                    print(ele_error)
            except Exception as openai_error:
                print(openai_error)
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
