import requests
import json
from source.dbhelper import *
import multiprocessing
from source import config


def get_models_from_sid(sid='414'):
    cookies = {
        # 'JSESSIONID': '71167344A98B6257F955A43791F1CA60',
    }

    headers = {
        'Host': config.restful_url,
        # 'Accept': '*/*',
        # 'User-Agent': 'D1ev_iOS/1.9.2 (iPhone; iOS 13.1.3; Scale/3.00)',
        # 'Accept-Language': 'zh-Hans-CN;q=1',
    }

    data = {
        # 'appName': '\u7B2C\u4E00\u7535\u52A8',
        # 'appVer': '1.9.2',
        # 'channel': 'AppStore',
        # 'cityId': '',
        # 'deviceId': 'F0A8BEB7-2057-4EAB-B67A-819D3BEC5080',
        # 'deviceOs': 'ios',
        # 'deviceOsVer': '13.1.3',
        # 'deviceSysVar': 'iPhone 7 Plus',
        # 'jpushId': '161a3797c869d6d4490',
        # 'lat': '0',
        # 'lng': '0',
        # 'network': 'Wifi',
        # 'networkOperator': '\u4E2D\u56FD\u79FB\u52A8',
        'seriesId': sid,
        # 'sss': '1eb36f9aee66baa5792b3e33fdf59a20',
        # 'userId': ''
    }

    response = requests.post(config.request_url, headers=headers,
                             cookies=cookies, data=data)
    return response.text


def get_car_model_titles():
    return ['modelName', 'sellingPrice', 'guidancePrice', 'batteryLife', 'belisted',
            'productionStatus', 'modelId']


my_session = DBSession()


def work_series(my_series):
    sid = my_series.url.split('-')[1][:-1]
    info = get_models_from_sid(sid)
    j = json.loads(info).get('data')
    print(j)
    if j:
        for l in ['ingList', 'stopList', 'weiList']:
            for d in j[l]:
                mylist = list(map(lambda x: d[x], get_car_model_titles()))
                model = Model(name=mylist[0], sellingPrice=mylist[1], guidancePrice=mylist[2],
                              batteryLife=mylist[3], belisted=mylist[4], productionStatus=mylist[5],
                              series_id=my_series.id, id=mylist[6])
                model.sellingPrice = model.sellingPrice.replace('万', '').replace('元', '')
                model.guidancePrice = model.guidancePrice.replace('万', '').replace('元', '')
                if model.sellingPrice.find('--') >= 0:
                    model.sellingPrice = '0'
                if model.guidancePrice.find('--') >= 0:
                    model.guidancePrice = '0'
                print(model)
                # my_session.execute(inserter, model.__dict__)


if __name__ == '__main__':
    inserter = Model.__table__.insert().prefix_with("IGNORE")
    pool = multiprocessing.Pool(4)
    pool.map(work_series, my_session.query(Series).all())
    pool.close()
    pool.join()
    my_session.commit()
    my_session.close()
