import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke bachche aaj duniya bhar ke khelon mein padak jeet rahe hain. Olympic mein, cricket mein aur anya khelon mein Bharat ka naam roshan ho raha hai. Khelo India jaise abhiyaan isme madad kar rahe hain.",
 "Pita ka saaya har bachche ke liye suraksha ka kavach hota hai. Pita apne bachche ko sahi raasta dikhata hai aur mushkil samay mein sahara deta hai. Unke balidan ko kabhi nahi bhoolna chahiye.",
 "Critical thinking helps us evaluate information and make better decisions. Instead of accepting everything at face value we analyze evidence and consider different perspectives. This skill is valuable in every area of life and work.",
 "Compassion is the ability to feel for others and act to reduce their suffering. Compassionate people make communities stronger and more caring. Practicing compassion daily creates a ripple effect of kindness.",
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
print("both long19 done", idx)
