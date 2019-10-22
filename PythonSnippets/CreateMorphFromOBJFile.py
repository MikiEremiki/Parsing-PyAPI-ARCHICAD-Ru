import os  # Импортируются библиотки для взаимодействия с системой
import sys
import fileinput

scriptDir = os.path.dirname(sys.argv[0])  # В переменной хранится путь где лежит исполняющийся скрипт python
file = os.path.join(scriptDir, "Bunny.obj")  # Присоеденяем к пути из scriptDir строку с названием файла

if os.path.isfile(file) is False:  # Проверяем, является ли файлом данный путь
    sys.exit("File does not exists: {}".format(file))  # Если нет завершаем выполнение скрипта и выводим сообщение


def create_morph_from_ojb_file(file_path, scale):
    materials = GetAttributeDictionary(API_MaterialID)  # Получили словарь всех материалов

    material = APIObject()  # Создали "пустой/неизвестный" архикадовский объект
    material.attributeIndex = list(materials)[0]  # Присвоили первый ключ из словаря materials
    material.overridden = True  # Включаем замену покрытия

    body = ModelerBody()  # Этой функции нет, к сожалению не знаю что делает,
    # но предполагаю, что это специальная процедура, позволяющая оперировать морфами, так как дальше идет метод Create()
    body.Create()  # Начало создания тела

    vertices = []
    polygons = []

    fileinput.close()  # Специально закрываем файл, который могли открыть до этого
    for line in fileinput.input(file_path):  # Цикл делает чтение по строчно, и разбивает строки на точки и полигоны,
        # затем к телу добавляет в нужной последовательности точки и полигоны
        if line[0] == "#":
            continue

        line = line.strip()
        while "  " in line:
            line = line.replace("  ", " ")
        parts = line.split(" ")

        if parts[0] == "v":
            vertices.append(body.AddVertex(scale * float(parts[1]),
                                           scale * float(parts[3]),
                                           scale * float(parts[2])))

        if parts[0] == "f":
            v = []
            e = []

            for i in range(1, len(parts)):
                subparts = parts[i].split("/")
                v.append(int(subparts[0]) - 1)

            last = len(v) - 1
            for i in range(0, last):
                e.append(body.AddEdge(v[i], v[i + 1]))
            e.append(body.AddEdge(v[last], v[0]))
            polygons.append(body.AddPolygon(e, 0, material))

    fileinput.close()  # Закрываем наш файл, с которого считывали информацию
    body.Finish()  # Конец создания тела

    pens = GetAttributeDictionary(API_PenID)  # Получили словарь всех перьев

    morph_pars = APIObject()  # Создали "пустой/неизвестный" архикадовский объект
    morph_pars.edgeType = APIMorphEdgeType_SoftHiddenEdge  # пока ни на что не влияет, но предполагаю,
    # что на отображение ребер
    morph_pars.castShadow = False  # Отбрасывание теней
    morph_pars.receiveShadow = False  # Не понятно, что делает
    morph_pars.coverFillPen = list(pens)[0]  # Перо штриховки поверхности, но не активна сама штриховка
    morph_pars.uncutLinePen = list(pens)[1]  # Перо линий контура
    morph_pars.cutLinePen = list(pens)[2]  # Перо линии сечения
    morph_pars.useDistortedCoverFill = False  # Не понятно, что делает
    morph_memo = APIObject()  # Создали "пустой/неизвестный" архикадовский объект
    morph_memo.morphBody = body  # Применили метод morphBody
    # по всей видимости создать единый морф из тела точек и полигонов
    del body  # Удаляем тело
    return CreateMorph(morph_pars, morph_memo)  # Правда, сама функция для создания морфа вот эта, но возмжно
# что это именно отрисовка морфа в проекте.


create_morph_from_ojb_file(file, 100)
