import whisper
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def sec2ts(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def transcribe_to_srt(audio_path, srt_path=None, model_size="small"):
    # Load Whisper model
    model = whisper.load_model(model_size)
    # voice
    result = model.transcribe(audio_path, language='ko')
    segments = result["segments"]
    if srt_path is None:
        srt_path = os.path.splitext(audio_path)[0] + ".srt"
    # Save SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()
            f.write(f"{i}\n{sec2ts(start)} --> {sec2ts(end)}\n{text}\n\n")
    print(f"Saved SRT! Path: {srt_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("How? -> python whisper_korean_srt.py [voice_file_path]")
    else:
        transcribe_to_srt(sys.argv[1])