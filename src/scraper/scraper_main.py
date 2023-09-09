from one_page.web_5ka_sales import *
from one_page.decompose_to_db import *
from sqlalchemy import create_engine
from tqdm import tqdm

conn = create_engine('postgresql://itmoml:vcqsaw2007@90.156.210.226:5432/retail_feedback')

# links = pd.read_sql('select * from prod.links_5ka_sales_stores', conn)['txt_link_5ka_sales'].to_list()
links = [
    'https://5ka-sale.ru/citi-taganrog/6633-1-y-novyy-pereulok-20.html',
    'https://5ka-sale.ru/citi-lipeck/3364-ulica-kosmonavtov-28.html',
    'https://5ka-sale.ru/citi-moskva/1142-kolomenskaya-ulica-17.html',
    'https://5ka-sale.ru/citi-balashiha/3513-central-naya-ulica-50.html',
    'https://5ka-sale.ru/citi-tver/7778-pereulok-nikitina-10k2.html',
    'https://5ka-sale.ru/citi-moskva/1268-schelkovskoe-shosse-26b.html',
    'https://5ka-sale.ru/citi-megion/1652-prospekt-pobedy-4.html',
    'https://5ka-sale.ru/citi-novoural-sk/7467-ulica-pobedy-12.html',
    'https://5ka-sale.ru/citi-novoural-sk/2632-ulica-furmanova-41.html',
    'https://5ka-sale.ru/citi-vyksa/4293-prommikrorayon-10-26.html',
    'https://5ka-sale.ru/citi-moskva/1170-nagornaya-ulica-21k1.html',
    'https://5ka-sale.ru/citi-moskva/1366-borisovskiy-proezd-40a.html',
    'https://5ka-sale.ru/citi-poselok-pargolovo/2978-zarechnaya-ulica-33.html',
    'https://5ka-sale.ru/citi-poselok-gorodskogo-tipa-malysheva/7335-ulica-timiryazeva-21.html'
]
scraper = Scraper5kaWebsite()

for link in tqdm(links):
    page = scraper.parse_page(link)
    decomposer = Decomposer(page, conn)
    try:
        decomposer()
    except Exception as e:
        print(e)
        break
