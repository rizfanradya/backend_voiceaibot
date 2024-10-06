from elevenlabs.client import ElevenLabs
from elevenlabs import (
    VoiceSettings,
    stream
)
from utils.config import ELEVENLABS_API_KEY


def audio_elevenlabs(text):
    try:
        audio_stream = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        response = audio_stream.text_to_speech.convert(
            # voice_id="pNInz6obpgDQGcFmaJgB",
            voice_id="EXAVITQu4vr4xnSDxMaL",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.8,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        stream(response)
    except Exception as error:
        print(error)
