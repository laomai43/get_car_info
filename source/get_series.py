from source.get_brands import *
from source.get_models import *
from source import dbhelper
import multiprocessing


def get_cars_from_url(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    es = soup.find_all('ul', {'id': 'selCarResult'})[0]
    es = es.find_all('li', {'class': 'am-fl'})
    result = []
    for e in es:
        # print(e)
        href = e.a['href']
        model = e.find('p', {'class': 'p_title'}).text
        img = e.img['src']
        price = e.find('p', {'class': 'price'}).span.text
        if price.find('暂无报价') >= 0:
            price = '0,0'
        elif price.find('-') < 0:
            price = price + ',' + price
        else:
            price = price.replace('-', ',')
        result.append(','.join([href, model, price, img]))
    return result


my_session = dbhelper.DBSession()


def work_brand(brand):
    my_insert = dbhelper.Series.__table__.insert().prefix_with("IGNORE")
    for series_info in get_cars_from_url(brand.url):
        series_info = series_info.split(',')
        my_series = dbhelper.Series(brand_id=brand.id, NAME=series_info[1], url=series_info[0], img=series_info[-1])
        my_session.execute(my_insert, my_series.__dict__)
    return 0


def get_series():
    pool = multiprocessing.Pool(4)
    pool.map(work_brand, my_session.query(dbhelper.Brand).all())
    pool.close()
    pool.join()
    my_session.commit()
    my_session.close()


if __name__ == '__main__':
    get_series()
