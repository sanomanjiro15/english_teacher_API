import random
import numpy as np
from fastapi.responses import JSONResponse


class Helper:
    def __init__(self):
        self.question_id = 1000
        self.db = {}

        with open("db_ru_en.txt", encoding='utf-8') as f:
            data = f.readlines()

        self.dictionary = {}
        for line in data:
            ru, en = line.split("-")
            self.dictionary[en.strip()] = ru.strip()

    #   =================== GENERATE ======================

    def generate_question_word(self):
        rus = list(self.dictionary.values())
        en_word = random.choice(list(self.dictionary.keys()))
        ru_word = self.dictionary[en_word]
        rus.remove(ru_word)
        var = [ru_word] + random.sample(rus, 3)
        np.random.shuffle(var)

        question_id = self.get_question_id()
        self.db[question_id] = ru_word
        # print({"question_id": question_id, "variance": var, "english": en_word})

        return JSONResponse(content={"question_id": question_id, "variance": var, "english": en_word},
                            media_type="application/json")

    def generate_question_letter(self):
        en_word = random.choice(list(self.dictionary.keys()))
        index = random.randint(0, len(en_word))
        correct_answer = en_word[index]

        question_id = self.get_question_id()
        self.db[question_id] = correct_answer

        list_en = list(en_word)
        list_en[index] = '*'
        join_en_word = "".join(list_en)

        return JSONResponse(content={"question_id": question_id, "en_word": join_en_word},
                            media_type="application/json")

    #   =================== CHECK ======================

    def check_answer(self, question_id, answer):
        if question_id in self.db:
            correct_answer = self.db[question_id]
            return JSONResponse(content={"is_correct": correct_answer == answer},
                                media_type="application/json")
        else:
            return JSONResponse(status_code=400, content={"error": "entered question_id not existing"})

    #   =================== READ ======================

    def get_correct_result(self, question_id):
        if question_id in self.db:
            correct_answer = self.db[question_id]
            return JSONResponse(content={"correct_answer": correct_answer},
                                media_type="application/json")
        else:
            return JSONResponse(status_code=400, content={"error": "entered question_id not existing"})

    def get_question_id(self):
        self.question_id += 1
        return self.question_id
