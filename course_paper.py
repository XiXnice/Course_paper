from api_vk import API_VK
from api_yd import API_YD

id_vk = input('Введите ID VK: ')
token_vk = input(str('Введите токкен VK: '))
token_yd = input(str('Введите токкен ЯНДЕКС ДИСКА: '))
file_path_pk = input(r'Введите путь куда сохранить файл НА ПК(C:/Project): ')
file_path_yd = input(str('Введите путь куда сохранить файл НА ПК("/image/" or "/"): '))

if __name__ == '__main__':
    client_vk = API_VK(token_vk, id_vk, '5.131', file_path_pk)
    client_yd = API_YD(file_path_yd, token_yd, file_path_pk)
    list = client_vk.get_photo_vk()
    client_yd.upload(list)
