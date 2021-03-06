# 镜像地址：https://www.vilipix.com/ranking
import requests
import datetime
import json
import re
import os


def yesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = str(today-oneday)
    return yesterday.replace('-', '')


def change(name):
    mode = re.compile(r'[\\/:*?"<>|]')
    new_name = re.sub(mode, '_', name)
    return new_name


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
}


def download(url):
    resp = requests.get(url, headers=headers)
    all_data = json.loads(resp.text)['rows']
    num = 1
    param = re.findall(r'\d+', url)
    for data in all_data:
        title = param[0] + '_p' + str(int(int(param[-1])/30+1)) + '_' + str(num) +\
                ' ' + change(data['title']) + '.jpg'
        download_url = data['regular_url']
        print('saving:  ', title, download_url)
        try:
            r = requests.get(download_url, headers=headers, timeout=5)
            with open('./日榜/'+title, 'wb') as f:
                f.write(r.content)
        except Exception as eee:
            print(eee)
        finally:
            num += 1


def geturls():
    page = 0
    urls = []
    while True:
        date = yesterday()
        url = 'https://www.vilipix.com/api/illust?mode=daily&date={date}&limit=30&offset={p}' \
            .format(date=date, p=str(page * 30))
        r = requests.get(url, headers=headers)
        js = json.loads(r.text)
        if not js['rows']:
            return urls
        else:
            urls.append(url)
            page += 1


def detailurls(date):
    page = 0
    urls = []
    while True:
        url = 'https://www.vilipix.com/api/illust?mode=daily&date={date}&limit=30&offset={p}' \
                .format(date=date, p=str(page * 30))
        r = requests.get(url, headers=headers)
        js = json.loads(r.text)
        if not js['rows']:
            return urls
        else:
            urls.append(url)
            page += 1


def yesterday_ranking():
    start = datetime.datetime.now()
    for url in geturls():
        try:
            download(url)
        except Exception as e:
            print(e)
    end = datetime.datetime.now()
    print('totally spent ', (end-start).seconds, ' seconds')


def detail_daily_ranking(date):
    start = datetime.datetime.now()
    for url in detailurls(date):
        try:
            download(url)
        except Exception as e:
            print(e)
    end = datetime.datetime.now()
    print('download', date, 'spent ', (end-start).seconds, ' seconds')


def main():
    print(
        '请选择下载模式，注意日榜最新是昨天的日期。', '回车下载昨日日榜，', '输入日榜日期（格式如：20210406）下载指定日期日榜。',
        '批量下载：输入时间段进行批量下载，如 20210401,20210416 ，注意以英文逗号拆分。',
        sep='\n'
    )
    choice = input('请输入：')

    try:
        os.mkdir('日榜')
    except Exception as e:
        print(e)

    if choice == '':
        yesterday_ranking()

    elif ',' in choice:
        start_time = datetime.datetime.now()
        for i in range(int(choice.split(',')[0]), int(choice.split(',')[1])+1):
            detail_daily_ranking(str(i))
        end_time = datetime.datetime.now()
        t = end_time - start_time
        print('the whole process spent: ', t)

    else:
        detail_daily_ranking(choice)


if __name__ == '__main__':
    main()
