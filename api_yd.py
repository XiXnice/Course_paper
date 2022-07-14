import requests
from progress.bar import Bar
import json

class API_YD:
    url_yd = 'https://cloud-api.yandex.net/v1/disk/'
    def __init__(self, file_path_yd, token_yd, file_path_pk):
                self.file_path_yd = file_path_yd
                self.file_path_pk = file_path_pk
                self.token_yd = token_yd

    def get_headers(self):
        return {
            'Context-Type': 'application/json',
            'Authorization': f'OAuth {self.token_yd}'
        }

    def _get_upload_link(self, path):
        url = f'{self.url_yd}resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, params = params, headers = headers)
        return response.json().get('href')

    def upload(self, list_name):
        list_name = list_name
        list_name.sort()
        len_name = len(list_name)
        count_name = 0
        count = 0
        inf_image = []
        headers = self.get_headers()
        bar = Bar('Processing', max = len_name)
        for i in range(len_name):
            while count_name != len_name:
                print(list_name[count])
                file_name = str(list_name[count])
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
                res = res.json()
                bar.next()
                count_name = count_name + 1
                count = count + 1
                inf_image.append(res)
        bar.finish()
        with open('inf_image.json', 'w') as f:
                    json.dump(inf_image, f)
