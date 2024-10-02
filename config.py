from dotenv import load_dotenv
import os


load_dotenv()

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
ASSEMBLYAI_API_KEY = os.environ.get('ASSEMBLYAI_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SPEECHTEXTAI_API_KEY = os.environ.get('SPEECHTEXTAI_API_KEY')
