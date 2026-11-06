import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Desh bhakti ka matlab hai apne desh se prem karna aur uske liye kuch karna. Chahe woh sipahi ho ya kisan, doctor ho ya teacher, har vyakti apne kaam se desh ki seva karta hai. Ekta aur akhandta desh ki sabse badi taakat hai.",
 "Samay sabse kimti dhan hai. Jo samay ka sahi upyog karta hai woh safal hota hai aur jo samay barbaad karta hai woh pachta hai. Isliye har din ka plan banana aur samay par kaam karna bahut zaroori hai.",
 "Curiosity is the spark that drives discovery and invention throughout history. When we ask why and how things work we open doors to new knowledge and possibilities. Encouraging curiosity in children is one of the best gifts we can give them for their future.",
 "Patience is a virtue that helps us face life's challenges with calm and wisdom. Good things take time and rushing never gives the best results. Those who wait patiently and work steadily eventually achieve their goals and inspire others with their example.",
]
voices_or=["hi_IN-pratham","hi_IN-priyamvada","en_US-amy","en_US-ryan"]
voices_sp=[("aditya","simba-3.2"),("alok","simba-3.5"),("geffen_32","simba-3.2")]
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
print("both long9 done", idx)
