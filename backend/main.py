from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Generator import QuestionGenerater

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
    input_text: str


@app.post("/suggest_questions/")
async def generateArticle(Data: TextData):
    data = Data.dict()
    questions = gen(data["input_text"])
    return questions
