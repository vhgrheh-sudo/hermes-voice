#!/usr/bin/env python3
"""Multi-TTS wake positives: Edge (unlimited, no key) + optional Nvidia/Gemini/Voxtral/Fish.
Edge is primary (free, Indian en-IN/hi-IN voices). Others are limited-quota, use sparingly.
Usage: python3 generate_edge.py --phrase "hey hermes" --samples 800 --out work/generated_samples
"""
import argparse, asyncio, subprocess
from pathlib import Path
import edge_tts
VOICES = ["hi-IN-SwaraNeural","hi-IN-MadhurNeural","en-IN-NeerjaNeural","en-IN-PrabhatNeural",
          "en-US-JennyNeural","en-US-GuyNeural","en-US-AriaNeural","en-GB-SoniaNeural","en-AU-NatashaNeural"]
RATES = ["-20%","-10%","+0%","+10%","+20%"]; PITCHES = ["+30Hz","+0Hz","-20Hz"]
async def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--phrase", default="hey hermes")
    ap.add_argument("--samples", type=int, default=800); ap.add_argument("--out", default="work/generated_samples")
    a = ap.parse_args(); outdir = Path(a.out); outdir.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(25); idx = 0; tasks = []
    async def one(text, voice, rate, pitch, out):
        if out.exists(): return
        tmp = out.with_suffix(".mp3")
        try:
            await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(tmp))
            subprocess.run(["ffmpeg","-y","-i",str(tmp),"-ar","16000","-ac","1","-sample_fmt","s16",str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            tmp.unlink(missing_ok=True)
        except Exception: pass
    for v in VOICES:
        for r in RATES:
            for pi in PITCHES:
                out = outdir / f"edge_{idx:05d}.wav"; idx += 1
                async def t(out=out, v=v, r=r, pi=pi):
                    async with sem: await one(a.phrase, v, r, pi, out)
                tasks.append(t())
                if idx >= a.samples: break
            if idx >= a.samples: break
        if idx >= a.samples: break
    await asyncio.gather(*tasks)
    # quiet/far copies so model works without shouting
    for i, w in enumerate(list(outdir.glob("*.wav"))[:400]):
        out = outdir / f"quiet_{i:05d}.wav"
        if not out.exists():
            subprocess.run(["ffmpeg","-y","-i",str(w),"-af","volume=0.35","-ar","16000","-ac","1",str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"done {len(list(outdir.glob('*.wav')))} in {outdir}")
if __name__ == "__main__": asyncio.run(main())
