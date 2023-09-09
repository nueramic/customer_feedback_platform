import os

import pandas as pd
from sqlalchemy import create_engine
from extract_ai_response import CallAiRecognition
from tqdm import tqdm


class AIUpdateDB:

    def __init__(self):
        self.conn = create_engine(os.getenv("DB_URL"))
        self.openai_key = os.getenv("OPENAI_API_KEY")

        self.ids_feedback = pd.read_sql(
            'select id_feedback from prod.ai_responses_tobe_parse', self.conn)['id_feedback'].to_list()

    def recognize_every_feedback(self):
        # with Pool() as pool:
        #     pool.map(self.recognize_feedback, self.feedbacks)

        for id_feedback in tqdm(self.ids_feedback):
            self.recognize_feedback(id_feedback)

    def recognize_feedback(self, id_feedback):
        return CallAiRecognition(id_feedback, self.conn, self.openai_key)()


ab = AIUpdateDB()
ab.recognize_every_feedback()
