from audio import generate_audio
from nlp import openai_nlp
from transcription import transcription, record_audio

if __name__ == "__main__":
    record_audio(duration=5)
    transcribe = transcription(audio_file="recorded.wav")
    print(transcribe['results']['transcript'])
    generate_audio(transcribe['results']['transcript'])
