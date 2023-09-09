import pandas as pd
from sqlalchemy.engine import Engine
from src.ai_recognition.chat_gpt_requests import AnalyzeFeedback


class CallAiRecognition:

    def __init__(self, id_feedback: str, pg_conn: Engine, openai_api_key: str):
        """

        :param id_feedback:
        :param pg_conn:
        """

        self.id_feedback = id_feedback
        self.source_table_name = 'prod.feedback'
        self.pg_conn = pg_conn
        self.analyzer = AnalyzeFeedback(self.pg_conn, openai_api_key)

        self.feedback_info = {'id_feedback': '', 'text_feedback': '', 'rating': '', 'max_rating': ''}
        self.gpt_out = {}

    def get_data_from_db(self):
        data = pd.read_sql(
            f"select * from {self.source_table_name} where id_feedback = '{self.id_feedback}' limit 1",
            self.pg_conn)

        if data.shape[0] > 0:
            info = data.iloc[0, :].T.to_dict()

            self.feedback_info['id_feedback'] = self.id_feedback
            self.feedback_info['text_feedback'] = info.get('txt_feedback')
            self.feedback_info['rating'] = info.get('num_rate')
            self.feedback_info['max_rating'] = info.get('num_max_rate')

    def __call__(self):
        self.get_data_from_db()

        if isinstance(self.feedback_info.get('text_feedback'), str):
            if len(self.feedback_info.get('text_feedback')) > 10:
                self.analyzer.analyze_feedback(
                    self.feedback_info.get('id_feedback'),
                    self.feedback_info.get('text_feedback'),
                    self.feedback_info.get('rating'),
                    self.feedback_info.get('max_rating')
                )

                self.analyzer.save_to_table()
