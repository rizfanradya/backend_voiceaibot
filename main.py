from audio.elevenlabs_ai import audio_elevenlabs
from nlp.hugging_face import nlp_hugging_face
from nlp.open_ai import nlp_openai
from transcribe.speech_text_ai import transcribe_speech_text, record_audio
from transcribe.assembly_ai import transcribe_assembly_ai


if __name__ == "__main__":
    audio_elevenlabs(
        "Thank you for calling, how may I assist you?"
    )

    # transcribe assemblyai
    transcribe_aai = transcribe_assembly_ai()
    print(f"transcribe : {transcribe_aai} \n")

    # transcribe speechtext
    # record_audio(duration=5)
    # transcribe_st_ai = transcribe_speech_text(audio_file="recorded.wav")
    # transcribe_st_ai_result = transcribe_st_ai['results']['transcript']
    # print(f"transcribe : {transcribe_st_ai_result} \n")

    # nlp huggingface
    # nlp = nlp_hugging_face(transcribe_aai)
    # print(f"natural language processing : {nlp} \n")

    # nlp openai
    nlp = nlp_openai(transcribe_aai)
    print(f"natural language processing : {nlp} \n")

    # audio elevenlabs
    audio_elevenlabs(nlp)
