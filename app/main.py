
# inside directory with __init__.py, so a module of the package: app.main

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from app.movies import router as movies_routers

app = FastAPI()
app.include_router(movies_routers)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: list[ChoiceBase]

# main path
@app.get("/")
def root():
    return {"status" : "ok"}