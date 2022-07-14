import requests

class API_VK:
    url_vk = 'https://api.vk.com/method/'
    def __init__(self, token_vk, id_vk, version_vk, file_path_pk):
        self.params_vk = {
            'access_token': token_vk,
            'v': version_vk,
            'owner_id': id_vk
        }
        self.file_path_pk = file_path_pk

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
