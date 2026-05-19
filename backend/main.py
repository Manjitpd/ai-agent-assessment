from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="AI Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_store = {}


class StartRequest(BaseModel):
    session_id: str
    task: str


class ReplyRequest(BaseModel):
    session_id: str
    answer: str

GREETING_WORDS = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good evening",
]

CASUAL_CHAT_WORDS = [
    "how are you",
    "what's up",
    "how’s it going",
    "are you okay",
    "how are things",
]    


def detect_intent(message: str):

    text = message.lower().strip()

    # Greeting
    if any(word in text for word in GREETING_WORDS):
        return "greeting"

    # Casual Chat
    if any(word in text for word in CASUAL_CHAT_WORDS):
        return "casual_chat"

    # Default
    return "task"

@app.get("/")
async def home():
    return {
        "success": True,
        "message": "AI Agent Backend Running"
    }


@app.post("/start")
async def start_conversation(data: StartRequest):

    user_input = data.task.strip()

    intent = detect_intent(user_input)

    # Greeting
    if intent == "greeting":

        return {
            "success": True,
            "type": "greeting",
            "agent": "Assistant",
            "message": "Hello 👋 How can I help you today?"
        }

    # Casual Chat
    if intent == "casual_chat":

        return {
            "success": True,
            "type": "casual_chat",
            "agent": "Assistant",
            "message": "I'm doing great 😊 Thanks for asking! How can I assist you today?"
        }

    # Start workflow
    conversation_store[data.session_id] = {
        "task": user_input,
        "step": 1,
        "tone": "",
        "length": ""
    }

    return {
        "success": True,
        "type": "workflow",
        "agent": "Backend Agent",
        "message": "What tone do you want? (Formal/Casual)"
    }


@app.post("/reply")
async def handle_reply(data: ReplyRequest):

    session = conversation_store.get(data.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    step = session["step"]

    if step == 1:

        session["tone"] = data.answer
        session["step"] = 2

        return {
            "success": True,
            "agent": "Backend Agent",
            "message": "Do you want short or detailed content?"
        }

    elif step == 2:

        session["length"] = data.answer
        session["step"] = 3

        prompt = f"""
        Create high quality content.

        Task: {session['task']}
        Tone: {session['tone']}
        Length: {session['length']}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert AI content writer.
                    Return clean markdown formatted output.
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        final_output = response.choices[0].message.content

        del conversation_store[data.session_id]

        return {
            "success": True,
            "agent": "AI Writer",
            "message": final_output,
            "completed": True
        }

    return {
        "success": True,
        "message": "Conversation completed"
    }