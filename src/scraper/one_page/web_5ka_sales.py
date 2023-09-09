import requests
from bs4 import BeautifulSoup
import re
import hashlib
import json
from datetime import datetime
from datetime import timedelta


class Scraper5kaWebsite:

    def __init__(self):
        pass

    @staticmethod
    def parse_page(page_link: str) -> str:
        """
        Парсит одну страницу одного магазина Пятерочка
        :param page_link: ссылка на страницу
        :return: dict
        """
        today = datetime.today()
        yesterday = str(today - timedelta(days=1))
        today = str(today)

        subpage1 = requests.get(page_link)
        soup1 = BeautifulSoup(subpage1.text, "html.parser")

        tmp_dict = {}  # основной json со всеми данными со страницы
        try:
            address = soup1.findAll('div', class_='card')
            address = address[0] if len(address) > 0 else None
            c = re.compile(r'<b>|</b>|<p>|</p>|<i[A-Za-z=\-\"\s]*>')
            adr = re.sub(c, '', str(address))

            address_to_write = list(map(lambda x: x.split(':'), adr.split('</i>')))[3][1] if address is not None else ''

            tmp_dict["idParentCompany"] = "1000-0000"
            tmp_dict["txtNameCompany"] = "X5 Retail"
            tmp_dict["idStore"] = hashlib.sha256(("пятерочка." + address_to_write).encode('utf-8')).hexdigest()
            tmp_dict["txtAddress"] = address_to_write.strip()
            tmp_dict["txtName"] = "пятерочка"
            tmp_dict["numLongitude"] = None
            tmp_dict["numLatitude"] = None
            tmp_dict["numPhoneNumber"] = 88005555505
            tmp_dict["txtWebLink"] = page_link
            tmp_dict["flgHandicappedAccessible"] = 0
            tmp_dict["idPlatform"] = "pltfrm-000000"
            tmp_dict["txtNamePlatform"] = "5ka-sale"
            tmp_dict["txtLinkMainPage"] = "https://5ka-sale.ru/"

            feedback_list = []  # Список с отзывами
            for i in range(len(soup1.findAll('div', class_='one_ot_text'))):

                txt_feedback = soup1.findAll('div', class_='one_ot_text')[i].text[:-8].strip()
                name = soup1.findAll('p', class_='com_author pull-left')[i].text.strip()

                id_feedback = hashlib.sha256((txt_feedback + name).encode('utf-8')).hexdigest()
                id_user = ('5ka-sale ' + name)

                cnt_likes = soup1.findAll('span', class_='add_plus')[i + 1].text.strip()
                cnt_dislikes = soup1.findAll('span', class_='add_minus')[i + 1].text.strip()

                date = soup1.findAll('p', class_='com_date pull-left')[i].text.strip()

                if 'Вчера в' in date:
                    date = date.replace('Вчера в', yesterday).strip()[:25]
                elif 'Сегодня в' in date:
                    date = date.replace('Сегодня в', today).strip()[:25]
                else:
                    date = date.replace('в', '').strip()[:25]

                feedback_dict = {
                    "idFeedback": id_feedback,
                    "idUser": id_user,
                    "UserLink": None,
                    "UserName": name,
                    "txtFeedback": txt_feedback,
                    "cntLikes": cnt_likes,
                    "cntDislikes": cnt_dislikes,
                    "dtFeedback": date
                }
                feedback_list.append(feedback_dict)

            tmp_dict["comments"] = feedback_list
        except Exception as e:
            print(f'{e}')
            raise e

        return json.dumps(tmp_dict, ensure_ascii=False)
