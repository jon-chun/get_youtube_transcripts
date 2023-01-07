import whisper
import torch

my_device = "cuda" if torch.cuda.is_available() else "cpu"

print(f'Device: {my_device}')

# model = whisper.load_model("medium.en").to(device)
model = whisper.load_model("tiny.en", device=my_device)

mp3_file = "./data___mp3___Helix_Center___UCvShfJtvC2owV0AFi_qyykA/a-freudian-perspective-on-what-ails-the-world-today-pt-1-introduction-and-education___2015-12-06___UCvShfJtvC2owV0AFi_qyykA___YMRTnfNA84k.mp3"
transcription = model.transcribe(mp3_file, task="transcribe", language="en")
transcript_str = transcription["text"]
print(transcript_str)

transcript_file = "test_transcript.txt"
with open(transcript_file, 'w+', encoding='utf-8') as fp:
    # fp.write(result['text'])
    fp.write(transcript_str)