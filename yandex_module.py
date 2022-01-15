from headers import *

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
        resp = requests.put(url, params=params, headers = headers)
        if resp.status_code != 201 and resp.status_code != 409:
            terminate('Creating folder failed', resp.status_code)

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
            else:
                terminate('File uploading failed', resp.status_code)
        else:
            terminate('Getting URL to upload file is failed', resp.status_code)


    def upload(self, target_folder, jsonfile='photos.json'):
        with open(jsonfile, "r") as read_file:
            data = json.load(read_file)
        for i in data:
            self.uploadfile(i.get('file_name'), target_folder)
