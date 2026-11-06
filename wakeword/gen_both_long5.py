import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke gaon mein ab bhi log apni paramparik jeevan shaili jeete hain. Subah jaldi uthkar khet khalihan jaana aur shaam ko chaupal par ikattha hona unki dincharya hai. Mehmaan nawazi aur bhai chaare ka mahaul har jagah dikhai deta hai.",
 "Sheher ki bhaag daud bhari zindagi mein bhi logon ko khushi ke pal dhoondhne padte hain. Park mein sair karna, doston ke saath chai peena ya parivar ke saath samay bitana ye chhote pal jeevan ko khoobsurat banate hain.",
 "Science helps us understand the world around us and solve problems that affect our daily lives. From medicine to space exploration scientific research has given us cures for diseases and tools to explore distant planets. Supporting science is investing in our collective future.",
 "Honesty and hard work are the two pillars of success in any field. People who work sincerely and never give up on their goals eventually achieve great things in life. Patience is also very important because success rarely comes overnight and requires consistent effort over time.",
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
print("both long5 done", idx)
