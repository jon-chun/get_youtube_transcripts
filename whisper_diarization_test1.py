# https://lablab.ai/t/whisper-transcription-and-speaker-identification

from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="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")

DEMO_FILE = {'uri':'blabla', 'audio':'test.wav'}
dz = pipeline(DEMO_FILE)

with open('diarization.txt','w') as fp:
    fp.write(str(dz))