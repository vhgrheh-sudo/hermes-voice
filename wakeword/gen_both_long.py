import requests, subprocess
from pathlib import Path
okey=open("/tmp/orchard_key.txt").read().strip()
skey=open("/tmp/speechify_key.txt").read().strip()
oh={"Authorization":f"Bearer {okey}"}
sh={"Authorization":f"Bearer {skey}","Content-Type":"application/json"}
texts=[
 "Bharat ki sanskriti bahut samriddh aur vividh hai. Har rajya ki apni alag pehchaan hai aur har jagah ke log ek doosre ka samman karte hain. Festivals ke samay poora desh ek saath khushi manata hai aur har gali mein roshni aur sangit ka mahaul hota hai. Yahi ekta Bharat ko vishwa mein alag banaati hai.",
 "Vigyaan ne hamare jeevan ko bahut badal diya hai. Pehle jahan dinon lag jaate the wahaan ab kuch hi seconds mein kaam ho jaata hai. Mobile phone aur internet ne duniya ko chhota kar diya hai aur har khabar kuch hi pal mein har jagah pahunch jaati hai. Is takneek ka sahi upyog hi humein aage badhayega.",
 "Education is the foundation of every successful society. When children receive good education they grow up to be responsible citizens who contribute to the nation. Teachers play a very important role in shaping the minds of young students and guiding them towards the right path in life and career.",
 "Nature is our greatest teacher and we should learn from it every day. The changing seasons teach us about patience and hope and the cycle of life. Trees provide us with oxygen and shade while rivers give us water and life. Protecting nature is protecting our own future and the future of generations to come.",
]
voices_or=["hi_IN-pratham","hi_IN-priyamvada","en_US-amy","en_US-ryan"]
voices_sp=[("aadi","simba-3.5"),("abhay","simba-3.5"),("geffen_32","simba-3.2")]
idx=len(list(Path("/tmp/long_speech").glob("*.wav")))
total_chars=0
for text in texts:
    total_chars+=len(text)
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
print("both long done", idx, "chars_per_text", len(texts[0]))
