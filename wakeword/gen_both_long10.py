import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke bachche aaj kal technology mein bahut aage hain. Chhoti umar se hi woh computer aur mobile chalane lagte hain aur nayi cheezein seekhne mein tez hain. Sahi guidance milne par woh duniya bhar mein naam roshan kar sakte hain.",
 "Buzurgon ki dekhbhaal karna hamara kartavya hai. Unhone apna jeevan samaj aur parivar ke liye samarpit kiya hai. Unke saath samay bitana aur unki baatein sunna hamare liye seekh ka srot hai.",
 "Creativity is the ability to imagine something new and bring it into the world. Artists writers and inventors use creativity to solve problems and express emotions. Every person has creative potential waiting to be discovered and developed with practice.",
 "Discipline is the bridge between goals and achievement in life. Without discipline even the best plans fail to produce results. Daily habits and consistent effort are more important than occasional bursts of motivation in the long run.",
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
print("both long10 done", idx)
