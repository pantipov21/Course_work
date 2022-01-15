from vk_module import *
from yandex_module import *

if __name__ == '__main__':
#
# Загрузка фотографий с VK, выбор фотографий максимальных размеров,
# построение списка словарей и сохранение их в json-файл, согласно задания.
#
    vk_id = input("Enter VK id: ")
    cw = CourseWork(vk_id) #здесь вторым параметром можно поставить название альбома, отличное от
                            # profile по умолчанию
    cw.execute() # метод execute по умолчанию скачивает 5 фотографий.

#
# Создание каталога на Яндекс.диске и загрузка в него всех фотографий
# из json-файла
#
    cwya = CourseWorkYandex('token from Yandex.Disk Poligon')
    cwya.upload('py48_Antipov')

