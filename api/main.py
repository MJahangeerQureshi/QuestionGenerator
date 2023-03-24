"""
FastAPI endpoint for using QuestionGenerater on given input text
Args:
    Data (BaseModel): text to generate questions from
Returns:
    questions (list): list of generated questions
"""
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from generator import QuestionGenerater

app = FastAPI()
gen = QuestionGenerater(20)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextData(BaseModel):
    """
    Model for input text data
    """
    input_text: str


@app.post("/suggest_questions/")
async def generateArticle(Data: TextData) -> list:
    """
    FastAPI endpoint for using QuestionGenerater on given input text
    Args:
        Data (BaseModel): text to generate questions from
    Returns:
        questions (list): list of generated questions
    """
    data = Data.dict()
    questions = gen(data["input_text"])
    return questions