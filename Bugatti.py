import requests
from bs4 import BeautifulSoup
import re
import os


def main():
    while 1:
        print('请输入车牌号：')
        host = 'http://www.zhongziso.com'
        car_name = input()
        flag_handle = 0
        for j in range(10):
            if flag_handle == 1:
                break
            print('开始搜索第' + str(j + 1) + '页：')
            while 1:
                try:
                    r = requests.get(host + '/list/' +
                                     car_name + '/' + str(j + 1), timeout=2)
                    break
                except:
                    continue
            soup = BeautifulSoup(r.content, 'html.parser',
                                 from_encoding='utf-8')
            nodes = soup.find_all('div', class_='text-left')[1:]

            if len(nodes) == 0:
                print('  无资源!\n')
                break
            else:
                count = 0
                for node in nodes:
                    print('  开始加载第' + str(j + 1) + '页第' +
                          (str(count + 1)) + '个资源：')
                    node = node.find('a')
                    while 1:
                        try:
                            r_target = requests.get(
                                host + node['href'], timeout=2)
                            break
                        except:
                            continue
                    soup = BeautifulSoup(
                        r_target.content, 'html.parser', from_encoding='utf-8')
                    text = re.sub('[\s]+', '', soup.find('h3',
                                                         class_='panel-title').get_text())
                    url = re.sub(
                        '[\s]+', '', soup.find('textarea', id='copytext').get_text())
                    url = url[:url.find('&dn;=') + 5] + car_name
                    hash = re.sub(
                        '[\s]+', '', soup.find('dl', class_=' dl-horizontal magnetmore').find_all('dd')[0].get_text())
                    hot = re.sub(
                        '[\s]+', '', soup.find('dl', class_=' dl-horizontal magnetmore').find_all('dd')[1].get_text())
                    size = re.sub(
                        '[\s]+', '', soup.find('dl', class_=' dl-horizontal magnetmore').find_all('dd')[2].get_text())
                    num = re.sub(
                        '[\s]+', '', soup.find('dl', class_=' dl-horizontal magnetmore').find_all('dd')[3].get_text())
                    creatDate = re.sub(
                        '[\s]+', '', soup.find('dl', class_=' dl-horizontal magnetmore').find_all('dd')[4].get_text())
                    lastDate = re.sub(
                        '[\s]+', '', soup.find('dl', class_=' dl-horizontal magnetmore').find_all('dd')[5].get_text())
                    tag = soup.find(
                        'dl', class_=' dl-horizontal magnetmore').find_all('dd')[6].get_text()
                    if text.find('u){}}()/*]]>*/') == -1:
                        text = text
                    else:
                        text = text[text.find('u){}}()/*]]>*/') + 14:]
                    count += 1
                    print(
                        '    *********************************************************')
                    print('    车牌：' + car_name)
                    print('    标题：' + text)
                    print('    地址：' + url)
                    print(
                        '    *********************************************************')
                    print('    哈希码：' + hash)
                    print('    热度：' + hot)
                    print('    大小：' + size)
                    print('    文件数量：' + num)
                    print('    创建时间：' + creatDate)
                    print('    最后访问时间：' + lastDate)
                    print('    标签：' + ' '.join(re.split('[-\s]+', tag)[:-1]))
                    print(
                        '    *********************************************************')
                    print('    请输入操作符：')
                    print('    1 要并退出做记录')
                    print('    2 不要并退出不做记录')
                    print('    3 要并继续做记录')
                    print('    4 不要并继续不做记录\n  ')
                    flag_handle = 0
                    while flag_handle == 0:
                        handle = input()
                        if handle == '1':
                            record(car_name, text, url, hash, hot, size, num,
                                   creatDate, lastDate, re.split('[-\s]+', tag)[:-1])
                            flag_handle = 1
                        elif handle == '2':
                            flag_handle = 1
                        elif handle == '3':
                            record(car_name, text, url, hash, hot, size, num,
                                   creatDate, lastDate, re.split('[-\s]+', tag)[:-1])
                            flag_handle = 2
                        elif handle == '4':
                            flag_handle = 2
                        else:
                            print('命令输入错误！请重新输入：')
                            continue
                    if flag_handle == 1:
                        break
                    else:
                        continue


def record(car_name, text, url, hash, hot, size, num, creatDate, lastDate, tag):
    if os.path.exists('record.txt'):
        f = open('record.txt', 'r')
        list = []
        p = re.compile('[^\t\n]+[\t\n]{1}')
        while 1:
            line = f.readline()
            if line:
                list_t = re.findall(p, line)
                list.append(list_t[3])
            else:
                break
        f.close()
        if (hash + '\t') in list:
            print('  车已存在!\n')
            return
        else:
            f = open('record.txt', 'a',errors = 'ignore')
            f.write(car_name + '\t' + text + '\t' + url + '\t' + hash + '\t' + hot +
                    '\t' + size + '\t' + num + '\t' + creatDate + '\t' + lastDate + '\t')
            f.write(';'.join(tag) + '\n')
            f.close()
            print('  记录成功！\n')

    else:
        f = open('record.txt', 'w',errors = 'ignore')
        f.write('车牌\t标题\t磁力链接\t哈希码\t热度\t大小\t文件数\t创建时间\t最后访问时间\t标签\n')
        f.write(car_name + '\t' + text + '\t' + url + '\t' + hash + '\t' + hot +
                '\t' + size + '\t' + num + '\t' + creatDate + '\t' + lastDate + '\t')
        f.write(';'.join(tag) + '\n')
        f.close()
        print('  记录成功！\n')

if __name__ == '__main__':
    main()
