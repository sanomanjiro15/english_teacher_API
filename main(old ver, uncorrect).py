from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse

from helper import Helper
from models import AnswerRequestBody, LetterRequestBody

# Endpoints:
# word/guess,   word/check,    word/result
# letter/guess,   letter/check,    letter/result

app = FastAPI()  # create API service
helper = Helper()  # database, questionszzz


@app.get("/word/guess")
def guess_word():
    return helper.generate_question_word()


@app.post("/word/check")
def guess_word_check(user_answer: AnswerRequestBody):
    return helper.check_answer(user_answer.question_id, user_answer.answer)

@app.get("/word/result")
def result_guess_word(answer: AnswerRequestBody):
    return helper.get_correct_result(answer.question_id)

@app.get("/letter/guess")
def guess_letter():
    qu = helper.generate_guess_letter()
    question_id = helper.get_question_id()

    helper.db[question_id] = qu['correct_answer']

    return {"question_id": question_id,
            "word": qu['word']}


@app.post("/letter/check")
def guess_letter_check(user_answer: AnswerRequestBody):
    return helper.check_guess_letter(user_answer.question_id, user_answer.answer)

@app.get(f"/letter/result")
def result_guess_word(answer: AnswerRequestBody):
    return helper.result_guess_letter(answer.question_id)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)