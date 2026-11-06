import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Swaasthya hi sabse bada dhan hai. Roz subah uthkar sair karna, yoga karna aur sahi khaana khaana sehat ke liye bahut faydemand hai. Paani bharpoor peena chahiye aur raat ko jaldi sona chahiye taaki sharir ko aaraam mile.",
 "Parivar ke saath khaana khaane se pyaar aur apnapan badhta hai. Ek saath baithe hue sabhi apni baatein share karte hain aur ek doosre ko samajhte hain. Yahi samay sabse kimti hota hai.",
 "Music and dance are important parts of every culture around the world. Traditional dances tell stories of history and community while modern music reflects current feelings and trends. Both bring people together and create lasting memories.",
 "Honesty builds trust which is the foundation of every strong relationship. People who are truthful earn respect and loyalty from friends family and colleagues. Even when honesty is difficult it is always the right choice in the long term.",
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
print("both long11 done", idx)
