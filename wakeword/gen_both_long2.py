import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Loktantra mein har nagrik ko apni baat rakhne ka adhikaar hai. Chunav ke dwara hum apne neta chunte hain jo hamari awaaz ko sadan tak pahunchate hain. Nyaypalika nagrikon ke adhikaaron ki raksha karti hai aur kaaloon sabke liye barabar hote hain. Isi liye loktantra ko janata ka raaj kaha jaata hai.",
 "Sehat ka khayal rakhna har vyakti ki zimmedari hai. Roz subah uthkar halki sair karna aur santulit bhojan lena sehat ke liye bahut faydemand hai. Paani bhi paryapt matra mein peena chahiye aur neend bhi poori honi chahiye. Swasth shareer mein hi swasth mann rehta hai.",
 "Books are our best friends in times of loneliness and learning. They take us to different worlds and teach us lessons that we can apply in our own lives. Reading for even fifteen minutes every day can change our thinking and improve our vocabulary. Libraries are treasure houses of knowledge open to everyone.",
 "Family is the most important part of our lives. It is the family that teaches us values and sanskar from childhood and supports us in every situation. Elders guide us with their experience while younger members bring new energy and ideas. A united family can face any difficulty together with love and cooperation.",
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
print("both long2 done", idx)
