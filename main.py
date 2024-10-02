from audio import generate_audio
from nlp import natural_language_processing
from transcription import transcription, record_audio

if __name__ == "__main__":
    record_audio(duration=5)

    transcribe = transcription(audio_file="recorded.wav")
    transcribe_result = transcribe['results']['transcript']
    print(f"transcribe : {transcribe_result} \n")

    nlp = natural_language_processing(transcribe_result)
    print(f"natural language processing : {nlp} \n")

    generate_audio(nlp)
