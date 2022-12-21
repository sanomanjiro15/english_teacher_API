from fastapi import FastAPI, Path
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from helper import Helper
from models import AnswerRequestBody, LetterRequestBody

# Endpoints:
# word/guess,   word/check,    word/result
# letter/guess,   letter/check,    letter/result

app = FastAPI(title="English Teacher",
              docs_url="/swagger",
              version="1.0")  # create API service
helper = Helper()  # database, questions


#   =================== WORD ======================


@app.get("/word/guess", tags=['word'])
def guess_word():
    return helper.generate_question_word()  # {"question_id": question_id, "variance": var, "english": en_word}


@app.get("/word/result/{question_id}", tags=['word'])
def guess_word_result(question_id: int):
    return helper.get_correct_result(question_id)


@app.post("/word/check", tags=['word'])
def guess_word_check(user_answer: AnswerRequestBody):
    return helper.check_answer(user_answer.question_id, user_answer.answer)


#   =================== LETTER ======================

@app.get("/letter/guess", tags=['letter'])
def guess_letter():
    return helper.generate_question_letter()


@app.get("/letter/result/{question_id}", tags=['letter'])
def guess_letter_result(question_id: int = Path(1000, gt=0, description="question id from response")):
    return helper.get_correct_result(question_id)


@app.post("/letter/check", tags=['letter'])
def guess_letter_check(user_answer: LetterRequestBody):
    return helper.check_answer(user_answer.question_id, user_answer.letter)


#   =================== RUN ======================

@app.get("/")
def root():
    return FileResponse("public/index.html")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)



