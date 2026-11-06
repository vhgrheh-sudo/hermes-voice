import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke bachche aaj har kshetra mein aage badh rahe hain. Khel mein, padhai mein aur kala mein unki pratibha duniya bhar mein dekhne ko milti hai. Mehnat aur sahi disha se woh aur aage badhenge.",
 "Prem aur karuna se hi parivar aur samaj judte hain. Ek doosre ki madad karna aur ek doosre ke dukh mein saath dena yahi insaaniyat hai. Yahi Bharat ki sanskriti ki sabse badi pehchaan hai.",
 "Communication skills are essential for success in every profession. Being able to express ideas clearly and listen carefully to others makes collaboration effective. Good communicators build trust and prevent misunderstandings in teams.",
 "Responsibility means taking ownership of our actions and decisions. Responsible people do not blame others for their mistakes but learn from them. This quality earns respect and opens doors to leadership opportunities.",
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
print("both long16 done", idx)
