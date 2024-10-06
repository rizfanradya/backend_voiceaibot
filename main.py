from lib.elevenlabs import audio_elevenlabs
from lib.aai_openai_elabs import assemblyai_openai_elevenlabs
from lib.gcloud_openai_elabs import googlecloud_openai_elevenlabs
from lib.gcloud_only import googlecloud_only

if __name__ == "__main__":
    try:
        audio_elevenlabs(
            "Thank you for calling, how may I assist you?"
        )

        # assemblyai_openai_elevenlabs()
        # googlecloud_openai_elevenlabs()
        googlecloud_only()
    except KeyboardInterrupt:
        print("\nClose Session...")
