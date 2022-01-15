from headers import *

VK_TEST_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
VK_VERSION = '5.131'

class CourseWork:
    def __init__(self, vk_id, album='profile'):
        self.vk_token = VK_TEST_TOKEN
        self.res_list = list()
        self.album = album
        self.vk_id = vk_id

    def search_groups(self, q, sorting=0):
        params = {
            'q': q,
            'access_token': VK_TEST_TOKEN,
            'v': VK_VERSION,
            'sort': sorting,
            'count': 300
        }
        res = requests.get('https://api.vk.com/method/groups.search', params)
        if res.status_code == 200:
            return res.json()['response']['items']
        else:
            terminate('Groups search failed', res.status_code)

    def search_users(self, q, sorting=1):
        params = {
            'q': q,
            'access_token': VK_TEST_TOKEN,
            'v': VK_VERSION,
            'sort': sorting,
            'online': 1
        }
        res = requests.get('https://api.vk.com/method/users.search', params)
        if res.status_code == 200:
            return res.json()['response']['items']
        else:
            terminate('Users search failed', res.status_code)

    def get_id(self):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': f'{self.vk_token}',
            'v': VK_VERSION
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json().get('response')[0].get('id')
        else:
            terminate('Getting user id failed', res.status_code)


    def save_result_file(self):
        with open("photos.json", "w") as write_file:
            json.dump(self.res_list, write_file)

    def get_photos(self, count):
        params = {
            'access_token': f'{self.vk_token}',
            'v': VK_VERSION,
            'owner_id': self.vk_id,
            'album_id': self.album,
            'extended': 1,
            'count': count,
            'photo_sizes': 1
        }
        res = requests.get('https://api.vk.com/method/photos.get', params)
        if res.status_code == 200:
            return res.json()
        else:
            terminate('Getting list of photos failed', res.status_code)


    def download_image(self, url, filename):
        ufr = requests.get(url)
        if ufr.status_code == 200:
            f = open(filename, "wb")
            f.write(ufr.content)
            f.close()
            print(f'{filename} downloaded on local drive.')
        else:
            terminate('Download request failed', ufr.status_code)



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
