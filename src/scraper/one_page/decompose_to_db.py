import json

import pandas as pd
from sqlalchemy.engine import Engine
from datetime import datetime


class Decomposer:

    def __init__(self, parsed_json: str, conn: Engine):
        self.parsed_json = json.loads(parsed_json)
        self.conn = conn
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __call__(self):
        id_parent_company = self.parsed_json.get("idParentCompany")
        txt_name_company = self.parsed_json.get("txtNameCompany")
        id_store = self.parsed_json.get("idStore")
        txt_address = self.parsed_json.get("txtAddress")
        txt_name = self.parsed_json.get("txtName")
        num_longitude = self.parsed_json.get("numLongitude")
        num_latitude = self.parsed_json.get("numLatitude")
        num_phone_number = self.parsed_json.get("numPhoneNumber")
        txt_web_link = self.parsed_json.get("txtWebLink")
        flg_handicapped_accessible = self.parsed_json.get("flgHandicappedAccess")
        id_platform = self.parsed_json.get("idPlatform")
        txt_name_platform = self.parsed_json.get("txtNamePlatform")
        txt_link_main_page = self.parsed_json.get("txtLinkMainPage")
        comments = self.parsed_json.get("comments")

        try:
            pd.DataFrame({
                'id_parent_company': [id_parent_company],
                'txt_name_company': [txt_name_company]
            }).to_sql('company', self.conn, schema='prod', index=False, if_exists='append', )

        except Exception as e:
            print(e)

        try:
            pd.DataFrame({
                'id_store': [id_store],
                'id_parent_company': [id_parent_company],
                'txt_address': [txt_address],
                'txt_name': [txt_name],
                'num_longitude': [num_longitude],
                'num_latitude': [num_latitude],
                'num_phone_number': [num_phone_number],
                'txt_web_link': [txt_web_link],
                'flg_handicapped_accessible': [flg_handicapped_accessible]
            }).to_sql('store', self.conn, schema='prod', index=False, if_exists='append')
        except Exception as e:
            print(e)

        try:
            pd.DataFrame({
                'id_platform': [id_platform],
                'txt_name_platform': [txt_name_platform],
                'txt_link_main_page': [txt_link_main_page],
            }).to_sql('platform', self.conn, schema='prod', index=False, if_exists='append')
        except Exception as e:
            print(e)

        id_feedback = []
        id_user = []
        user_link = []
        user_name = []
        txt_feedback = []
        cnt_likes = []
        cnt_dislikes = []
        dt_feedback = []

        for comment in comments:
            id_feedback.append(comment.get('idFeedback'))
            id_user.append(comment.get('idUser'))
            user_link.append(comment.get('UserLink'))
            user_name.append(comment.get('UserName'))
            txt_feedback.append(comment.get('txtFeedback'))
            cnt_likes.append(comment.get('cntLikes'))
            cnt_dislikes.append(comment.get('cntDislikes'))
            dt_feedback.append(comment.get('dtFeedback'))

        try:
            user_df = pd.DataFrame({
                'id_user': id_user,
                'id_platform': [id_platform] * len(comments),
                'txt_userlink': user_link,
                'txt_username': user_name,
            })
            user_df.to_sql('user_info', self.conn, schema='prod', index=False, if_exists='append')

        except Exception as e:
            print(e)

        try:
            feedback_df = pd.DataFrame({
                'id_feedback': id_feedback,
                'id_user': id_user,
                'id_platform': [id_platform] * len(comments),
                'id_store': [id_store] * len(comments),
                'txt_feedback': txt_feedback,
                'cnt_likes': cnt_likes,
                'cnt_dislikes': cnt_dislikes,
                'dt_feedback': dt_feedback,
                'num_rate': [None] * len(comments),
                'num_max_rate': [None] * len(comments),
                'dtime_uploaded': [self.now] * len(comments)
            })
            feedback_df.to_sql('feedback', self.conn, schema='prod', index=False, if_exists='append')

        except Exception as e:
            print(e)
