import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ki mitti mein woh khushboo hai jo kahin aur nahi milti. Yahan ki hawa, paani aur ped paudhe sabse alag hain. Isi liye Bharat ko dharti ka swarg kaha jaata hai.",
 "Seekhne ki umar ka koi ant nahi hota. Insaan jab tak jeevit hai tab tak woh kuch na kuch seekhta rehta hai. Nayi cheezein seekhna jeevan ko romanchak aur samriddh banata hai.",
 "Leadership is about guiding others towards a common goal with honesty and courage. Good leaders listen to their team members and make decisions that benefit everyone. They take responsibility for failures and share credit for successes with their team.",
 "Empathy means understanding and sharing the feelings of others. When we put ourselves in someone else's shoes we become more compassionate and helpful. Empathy is the foundation of strong friendships and healthy relationships.",
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
print("both long12 done", idx)
