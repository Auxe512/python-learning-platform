from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from judge import judge
from ai import get_hint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class SubmitRequest(BaseModel):
    code: str


@app.post("/submit")
async def submit(req: SubmitRequest):
    results = await judge(req.code)
    hint = await get_hint(req.code, results)
    return {"results": results, "hint": hint}
