import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ki nadiyan pavitra mani jaati hain. Ganga, Yamuna aur Saraswati jaise nadiyon ke kinare prachin kaal se hi sabhyata phal phool rahi hai. In nadiyon ka paani khet khalihan aur jeevan ko samriddh banata hai.",
 "Bachchon ke saath khelna unke sharirik aur mansik vikas ke liye bahut zaroori hai. Khelo se woh team bhawna, netritva aur sahyog seekhte hain. Roz kam se kam ek ghanta khelna sehat ke liye bhi faydemand hai.",
 "Books open doors to new worlds and ideas for every reader. A single book can teach us about history science or human emotions in a way that no other medium can match. Reading regularly is one of the best habits we can develop in our lives.",
 "Kindness costs nothing but means everything to the person who receives it. A simple smile or a helpful word can brighten someone's entire day. When we are kind to others we create a happier and more caring society for everyone to live in.",
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
print("both long7 done", idx)
