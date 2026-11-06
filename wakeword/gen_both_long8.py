import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ke tyoharon mein holi, diwali, eid aur christmas sabhi ek saath manaye jaate hain. Har dharm aur samuday ke log ek doosre ke tyoharon mein shaamil hote hain aur khushi baantte hain. Yahi Bharat ki ekta ki pehchaan hai.",
 "Gyaan ka deepak humein andhere se roshni ki taraf le jaata hai. Jo vyakti seekhne ki aadat banata hai woh har samasya ka hal nikaal sakta hai. Padhna, sunna aur samajhna teenon hi gyaan ke zariye hain.",
 "Teamwork makes difficult tasks easier and more enjoyable for everyone involved. When people work together they combine their strengths and cover each other's weaknesses. Successful teams communicate clearly and respect each other's ideas and opinions.",
 "Gratitude is a powerful feeling that brings happiness to our lives. Thanking others for their help and appreciating what we have makes us more positive. People who practice gratitude regularly are generally healthier and more satisfied with their lives.",
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
print("both long8 done", idx)
