from itertools import count
import requests
from pprint import pp, pprint
from progress.bar import Bar
import time

class User:
    url_vk = 'https://api.vk.com/method/'
    url_yd = 'https://cloud-api.yandex.net/v1/disk/'
    def __init__(self, token_vk, token_yd, id_vk, version_vk, file_path_pk, file_path_yd):
        self.params_vk = {
            'access_token': token_vk,
            'v': version_vk,
            'owner_id': id_vk
        }
        self.token_yd = token_yd
        self.file_path_pk = file_path_pk
        self.file_path_yd = file_path_yd

    def get_headers(self):
        return {
            'Context-Type': 'application/json',
            'Authorization': f'OAuth {self.token_yd}'
        }

    def get_photo_vk(self):
        list_name = []
        photos_url = f'{self.url_vk}photos.get'
        params_profile = {
            'album_id': 'profile',
            'extended': 'likes'
        }
        # profile = requests.get(photos_url, params={**self.params_vk, **params_profile}).json()['response']
        count_profile = int(requests.get(photos_url, params={**self.params_vk, **params_profile}).json()['response']['count'])
        count_profile_1 = count_profile -1
        number_profile = 0
        while number_profile != count_profile:
            time.sleep(1)
            file_name_path_profile = requests.get(photos_url, params={**self.params_vk, **params_profile}).json()['response']['items'][count_profile_1]['likes']['count']
            file_url_profile = requests.get(photos_url, params={**self.params_vk, **params_profile}).json()['response']['items'][count_profile_1]['sizes'][-1]['url']
            api_profile = requests.get(file_url_profile, params={**self.params_vk, **params_profile})
            file_name_profile = str(file_name_path_profile) + '.jpg'
            list_name.append(file_name_profile)
            path_profile = self.file_path_pk + '/' +  file_name_profile
            with open(path_profile, 'wb') as file_profile:
                file_profile.write(api_profile.content)
            count_profile_1 = count_profile_1 - 1
            number_profile = number_profile + 1

        params_wall = {
            'album_id': 'wall',
            'extended': 'likes'
        }
        # wall = requests.get(photos_url, params={**self.params_vk, **params_wall}).json()['response']
        count_wall = int(requests.get(photos_url, params={**self.params_vk, **params_wall}).json()['response']['count'])
        count_wall_1 = count_wall - 1
        number_wall = 0
        while number_wall != count_wall:
            time.sleep(1)
            file_name_path_wall = requests.get(photos_url, params={**self.params_vk, **params_wall}).json()['response']['items'][count_wall_1]['likes']['count']
            file_url_wall = requests.get(photos_url, params={**self.params_vk, **params_wall}).json()['response']['items'][count_wall_1]['sizes'][-1]['url']
            api_wall = requests.get(file_url_wall, params={**self.params_vk, **params_wall})
            file_name_wall = str(file_name_path_wall) + '.jpg'
            list_name.append(file_name_wall)
            path_wall = self.file_path_pk + '/' +  file_name_wall
            with open(path_wall, 'wb') as file_wall:
                file_wall.write(api_wall.content)

            count_wall_1 = count_wall_1 - 1
            number_wall = number_wall + 1
        return list_name

    def _get_upload_link(self, path):
        url = f'{self.url_yd}resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, params = params, headers = headers)
        return response.json().get('href')

    def upload(self):
        list_name = self.get_photo_vk()
        list_name.sort()
        len_name = len(list_name)
        count_name = 0
        count = 0
        bar = Bar('Processing', max = len_name)
        for i in range(len_name):
            while count_name != len_name:
                time.sleep(0.5)
                file_name = str(list_name[count])
                headers = self.get_headers()
                path_yd_1 = self.file_path_yd + file_name
                path_yd = self.file_path_pk + '/' + file_name
                upload_link = self._get_upload_link(path_yd_1)
                response = requests.put(upload_link, data=open(path_yd, 'rb'), headers = headers)
                url_inf = f'{self.url_yd}resources'
                headers_inf = self.get_headers()
                path_inf = self.file_path_yd + file_name
                params_inf = {
                    'path': path_inf,
                    'fields': 'size,name'
                    }
                res = requests.get(url_inf, headers = headers_inf, params = params_inf)
                bar.next()
                print()
                pprint(res.json())
                count_name = count_name + 1
                count = count + 1
        bar.finish()


if __name__ == '__main__':
    id_vk = input('Введите ID VK: ')
    token_vk = input(str('Введите токкен VK: '))
    token_yd = input(str('Введите токкен ЯНДЕКС ДИСКА: '))
    file_path_pk = input(r'Введите путь куда сохранить файл НА ПК(C:/Project): ')
    file_path_yd = input(str('Введите путь куда сохранить файл НА ПК("/image/" or "/"): '))
    client = User(token_vk, token_yd, id_vk, '5.131', file_path_pk, file_path_yd)
    client.upload()
