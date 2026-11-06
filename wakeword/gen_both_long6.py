import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke bachche aaj duniya bhar mein naam roshan kar rahe hain. Khel, vigyaan, ganit aur kala har kshetra mein unki pratibha dekhne ko milti hai. Shiksha aur sahi guidance se woh aage badhkar desh ka gaurav badhayenge.",
 "Parivar mein buzurgon ka samman karna hamari sanskriti ka hissa hai. Unke aashirwad se hi hum aage badhte hain aur jeevan ki sahi disha milti hai. Unki kahaniyan aur anubhav hamare liye gyaan ka khazana hote hain.",
 "Technology is changing education in remarkable ways. Online classes make learning accessible to students in remote areas who could not attend physical schools. Interactive tools help teachers explain difficult concepts in simple and engaging ways to young learners.",
 "Environment protection is everyone's responsibility. Planting trees, saving water and keeping our surroundings clean are small actions that make a big difference. If every person takes these steps the earth will remain beautiful and healthy for future generations.",
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
print("both long6 done", idx)
