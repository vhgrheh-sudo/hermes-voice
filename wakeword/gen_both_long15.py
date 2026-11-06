import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Desh ke jawan seema par khade hokar hum sabki suraksha karte hain. Unki kurbaani aur balidan kabhi bharpai nahi ho sakti. Hum sabko unka samman karna chahiye aur unke parivar ki dekhbhaal karni chahiye.",
 "Samay par kaam karne ki aadat jeevan mein bahut fayda deti hai. Jo kaam aaj ka hai use aaj hi kar lena chahiye, kal par taalna nahi chahiye. Isi se safalta milti hai aur man ko shanti milti hai.",
 "Learning never ends for those who are curious about the world. Every day brings new discoveries and ideas to explore. Keeping an open mind helps us grow and adapt to changing circumstances throughout our lives.",
 "Generosity makes the world a better place for everyone. Sharing our time money and resources with those in need brings happiness to both giver and receiver. Even small acts of kindness can have a big impact on someone's life.",
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
print("both long15 done", idx)
