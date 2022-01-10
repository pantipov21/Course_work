from pprint import pprint
import sys
import json
sys.path.append('/usr/lib/python3/dist-packages')
import requests


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.




class CourseWork:
    def __init__(self, vk_id, album='profile'):
        self.vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
        self.res_list = list()
        self.album = album
        self.vk_id = vk_id

    def search_groups(q, sorting=0):
        params = {
            'q': q,
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
            'sort': sorting,
            'count': 300
        }
        return requests.get('https://api.vk.com/method/groups.search', params=params).json()['response']['items']

    def search_users(q, sorting=1):
        params = {
            'q': q,
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
            'sort': sorting,
            'online': 1
        }
        return requests.get('https://api.vk.com/method/users.search', params).json()['response']['items']

    def get_id(self):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': f'{self.vk_token}',
            'v': '5.131'
        }
        return requests.get(url, params=params).json().get('response')[0].get('id')

    def save_result_file(self):
        with open("photos.json", "w") as write_file:
            json.dump(self.res_list, write_file)

    def get_photos(self, count):
        params = {
            'access_token': f'{self.vk_token}',
            'v': '5.131',
            'owner_id': self.vk_id,
            'album_id': self.album,
            'extended': 1,
            'count': count,
            'photo_sizes': 1
        }
        return requests.get('https://api.vk.com/method/photos.get', params).json()

    def download_image(self, url, filename):
        f = open(filename, "wb")
        ufr = requests.get(url)
        f.write(ufr.content)
        f.close()
        print(f'{filename} downloaded on local drive.')

    def handle_photos(self, d):
        tmp_rec = dict()
        fn = list()

#        count = d.get('response').get('count')
        res = d.get('response').get('items')

        for i in res:
            url_max = ''
            max_square = -1

            size = '0'
            tmp_rec.clear()

            likes = i.get('likes').get('count')
            creation_date = i.get('date')

            for j in i.get('sizes'):
                h = j.get('height')
                w = j.get('width')
                if h * w >= max_square:
                    size = j.get('type')
                    max_square = h * w
                    url_max = j.get('url')

            # запомнить данные
            if likes not in fn:
                fn.append(likes)
                photo_name = str(likes)+'.jpg'
            else:
                photo_name = str(likes)+'_'+str(creation_date)+'.jpg'

            tmp_rec['file_name'] = photo_name
            tmp_rec['size'] = size
            self.res_list.append(tmp_rec.copy())

            # скачать фотографию
            self.download_image(url_max, photo_name)
        self.save_result_file()

    def execute(self, photos_quantity=5):
        result = self.get_photos(photos_quantity)
        if result != -1:
            self.handle_photos(result)


class CourseWorkYandex():
    def __init__(self, token):
        self.token = token

    def create_folder(self, folder_name):
        headers = {
            "Authorization": f'OAuth {self.token}'
        }
        params = {
            "path": folder_name
        }
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        resp = requests.put(url, params=params, headers=headers)

    def uploadfile(self, filename, dirname):
        print(f'Uploading {filename} to the folder {dirname}', end='')
        self.create_folder(dirname)
        print('.', end='')
        url = "https://cloud-api.yandex.net:443/v1/disk/resources/upload"
        params = {"path": f'{dirname+"/"+filename}',
                  "overwrite": "true"}
        headers = {
            "Authorization": f'OAuth {self.token}'
        }

        print('.', end='')
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            print('.', end='')
            resp = requests.put(resp.json().get('href'), data=open(filename, 'rb'))
            if resp.status_code == 201:
                print("File uploaded successfully")

    def upload(self, target_folder, jsonfile='photos.json'):
        with open(jsonfile, "r") as read_file:
            data = json.load(read_file)
        for i in data:
            self.uploadfile(i.get('file_name'), target_folder)


if __name__ == '__main__':
#
# Загрузка фотографий с VK, выбор фотографий максимальных размеров,
# построение списка словарей и сохранение их в json-файл, согласно задания.
#
    vk_id = input("Enter VK id: ")
    cw = CourseWork(vk_id) #здесь вторым параметром можно поставить название альбома, отличное от
                            # profile по умолчанию
    cw.execute()# метод execute по умолчанию скачивает 5 фотографий.

#
# Создание каталога на Яндекс.диске и загрузка в него всех фотографий
# из json-файла
#
    cwya = CourseWorkYandex('put here token from Yandex.Disk')
    cwya.upload('py48_Antipov')

# See PyCharm help at https://www.jetbrains.com/help/py2charm/
