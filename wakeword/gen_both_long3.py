import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bachchon ko achhi shiksha dena har maa baap ka sapna hota hai. Achhe school mein padhkar bachche sirf gyaan hi nahi haasil karte balki sanskar aur anushaasan bhi seekhte hain. Teachers unhe sahi raaste par le jaate hain aur unke vyaktitva ko nikhari mein madad karte hain.",
 "Kisan hamare desh ki jaan hai. Woh din raat mehnat karke hamare liye ann ugaata hai. Baarish aur mausam ki har mushkil se ladkar woh fasal taiyaar karta hai. Isliye humein kisan ka samman karna chahiye aur unhe sahi daam dena chahiye taaki woh bhi khushi se jee sakein.",
 "Dreams are the seeds of our future. Every great achievement in the world started as a small dream in someone's mind. With hard work and determination those dreams can become reality one day. Never stop believing in yourself and keep moving forward towards your goals every single day.",
 "Friendship is one of the most beautiful relationships in life. True friends stand by us in happiness and sadness and never leave us alone in difficult times. A good friend is like a treasure that becomes more precious with time. We should always value our friendships and keep them strong with honesty and trust.",
]
voices_or=["hi_IN-pratham","hi_IN-priyamvada","en_US-amy","en_US-ryan"]
voices_sp=[("aadi","simba-3.5"),("abhay","simba-3.5"),("alok","simba-3.2")]
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
print("both long3 done", idx)
