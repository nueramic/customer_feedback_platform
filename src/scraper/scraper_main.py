from one_page.web_5ka_sales import *
from one_page.decompose_to_db import *
from sqlalchemy import create_engine
from tqdm import tqdm

conn = create_engine('postgresql://itmoml:vcqsaw2007@90.156.210.226:5432/retail_feedback')

links = pd.read_sql('select * from prod.links_5ka_sales_stores', conn)['txt_link_5ka_sales'].to_list()

scraper = Scraper5kaWebsite()

for link in tqdm(links[44 + 33:]):
    page = scraper.parse_page(link)
    decomposer = Decomposer(page, conn)
    try:
        decomposer()
    except Exception as e:
        print(e)
        break
