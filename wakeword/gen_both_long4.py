import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat mein holi ka tyohar bahut dhoom dham se manaya jaata hai. Log ek doosre par rang gulal lagate hain aur khushi mein nachte gaate hain. Yeh tyohar buraai par achhai ki jeet ka prateek hai. Har jagah mithaiyan banti hain aur ghar ghar mein mehmaan aate hain.",
 "Diwali par poora desh roshni se jagmag uthta hai. Log apne ghar sajate hain aur diye jalate hain. Laxmi puja karke samriddhi ki kaamna ki jaati hai. Bachche patakhon se khelte hain aur bade ek doosre ko mithai bhejte hain. Yeh tyohar andhere par roshni ki jeet dikhata hai.",
 "Music connects people across all barriers of language and culture. When we listen to a beautiful melody we feel emotions that words cannot describe. Singers and musicians work hard to perfect their art and bring joy to millions of listeners every day through their performances.",
 "Honesty is the best policy in life. A honest person earns respect and trust from everyone around him. Even if telling the truth is difficult in some situations, it always leads to long term happiness and peace of mind. Dishonesty may give temporary benefits but never lasting respect.",
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
print("both long4 done", idx)
