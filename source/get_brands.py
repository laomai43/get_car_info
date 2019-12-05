import bs4
import requests
import source.dbhelper as helper
from source import config


def get_brands():
    url= config.brand_url
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    es = soup.find_all('div', {'class': 'pingpai_content'})[0]
    es = es.find_all('li', {'class': 'am-fl'})

    session = helper.DBSession()
    inserter = helper.Brand.__table__.insert().prefix_with("IGNORE")
    for e in es:
        brand = helper.Brand(name=e.a.img['alt'], img=e.a.img['src'], url=e.a['href'])
        session.execute(inserter, brand.__dict__)
    session.commit()
    session.close()


def get_brands_titles():
    return ','.join(['brand_url', 'brand_name', 'brand_img'])


if __name__ == '__main__':
    get_brands()
    # print(type(helper.Brand.__table__))
