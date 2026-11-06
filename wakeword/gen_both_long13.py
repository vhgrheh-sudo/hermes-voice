import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Sacchi dosti samay ke saath aur mazboot hoti jaati hai. Ek sachcha dost sukh mein hi nahi dukh mein bhi saath deta hai. Aisi dosti jeevan bhar ka sahara hoti hai.",
 "Kitaabein hamari sabse acchi dost hoti hain. Woh humein nayi duniya ki sair karati hain aur purane samay ki kahaniyan sunati hain. Roz thoda padhna gyaan badhata hai aur soch ko vistrit karta hai.",
 "Hard work and smart work both have their place in achieving success. Hard work builds the foundation while smart work helps us reach goals faster. The best approach combines both qualities to maximize our chances of success in any field.",
 "Respect is earned through actions not demanded by words. When we treat others with dignity and fairness we earn their respect naturally. Respectful relationships are the basis of harmony in families workplaces and communities.",
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
print("both long13 done", idx)
