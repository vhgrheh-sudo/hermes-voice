import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke kisan din raat mehnat karte hain taaki hum sabko khaana mile. Baarish, dhoop aur thand har mausam mein woh khet mein khade rehte hain. Unka samman karna hum sabka kartavya hai.",
 "Bachchon ko achhe sanskar dena sabse zaroori kaam hai. Maa baap jaise vyavhaar karte hain bachche waisa hi seekhte hain. Isliye ghar ka mahaul hamesha prem aur anushaasan se bhara rehna chahiye.",
 "Technology has made communication faster and easier than ever before. We can now talk to anyone in the world instantly through video calls and messages. Staying connected with loved ones is one of the greatest benefits of modern technology.",
 "Perseverance means continuing to try even when things become difficult or discouraging. Many successful people faced multiple failures before finally achieving their goals. Never giving up is the key to turning dreams into reality.",
]
voices_or=["hi_IN-pratham","hi_IN-priyamvada","en_US-amy","en_US-ryan"]
voices_sp=[("aadi","simba-3.5"),("abhay","simba-3.5"),("geffen_32","simba-3.2")]
idx=len(list(Path("/tmp/long_speech").glob("*.wav")))
for text in texts:
    for v in voices_or:
        r=requests.post("https://api.orchardrun.com/v1/tts/generate", headers=oh, data={"text":text,"voice_id":v,"voice_type":"generic"}, timeout=60)
        if r.status_code==200:
            open("/tmp/or_long.wav","wb").write(r.content)
            subprocess.run(["ffmpeg","-y","-i","/tmp/or_long.wav","-ar","16000","-ac","1","-sample_fmt","s16",f"/tmp/long_speech/long{idx:04d}.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            idx+=1
    for vid,model in voices_sp:
        r=requests.post("https://api.speechify.ai/v1/audio/stream", headers=sh, json={"input":text,"voice_id":vid,"model":model}, timeout=60)
        if r.status_code==200:
            open("/tmp/sp_long.mp3","wb").write(r.content)
            subprocess.run(["ffmpeg","-y","-i","/tmp/sp_long.mp3","-ar","16000","-ac","1","-sample_fmt","s16",f"/tmp/long_speech/long{idx:04d}.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            idx+=1
print("both long14 done", idx)
