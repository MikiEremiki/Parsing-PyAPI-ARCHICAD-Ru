import os
import sys
import glob

# Получаем все PLN файлы из папки ToPublish рядом со скриптом
# и устанавливаем для публикации набор "1 - Виды", который будет опубликован во всех файлах
scriptDir = os.path.dirname(sys.argv[0])  # Получаем путь откуда запускался скрипт
filesToPublish = {}  # Объявляем словарь
for file in glob.glob(os.path.join(scriptDir, 'ToPublish', '*.pln')):
    # Для каждого файла, устанавливаем для публикации набор "1 - Виды"
    filesToPublish[file] = '1 - Виды'

# Открываем каждый файл и публикуем заданный набор
for file, pset in filesToPublish.items():  # file - ключ из словаря (сам файл pln), pset - значение равное имени набора
    print("Working on project {}".format(file))
    # Выводим в консоль путь с файлом из которого сейчас будет происходить публикация
    Open(file)  # Открываем этот файл
    PublishSet(pset, os.path.join(scriptDir, 'Published'))
    # Вызываем функцию публикации и создаем папку Published, если она не была опубликована
