from dataclasses import dataclass
from fastapi import FastAPI, Request, Response
from openai import OpenAI
from pydantic import BaseModel
from dataModel import RequestChat, ReponseOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 환경 변수에서 API 키 읽기
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

app = FastAPI()
id = None

chatList =[]
# chatList.clear()

def responsGet(response : Response):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": "지식백과"},
            {"role": "user", "content": f"{response}"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    response = res.choices[0].message.content

    return { "response" : response }

@app.post("/chat")
async def chatBack(chat : RequestChat):
    reply = responsGet(chat.messages)
    response = reply['response']
    
    saveChat(chat, response)
    
    print(chatList)
    return { "content" : reply }

def saveChat(chat, response):
    found = False

    for chatOne in chatList:
        if chatOne["id"] == chat.id:
            chatOne["chat"]["messages"].append(chat.messages)
            chatOne["chat"]["response"].append(response)
            print("도착")
            found = True
            break

    if not found:
        saveMessage = { "id": chat.id, "chat": { "messages": [ chat.messages ], "response": [ response ] } }
        chatList.append(saveMessage)