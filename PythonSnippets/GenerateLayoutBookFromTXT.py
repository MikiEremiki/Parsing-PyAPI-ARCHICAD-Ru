import os
import sys
import re

scriptDir = os.path.dirname(sys.argv[0])  # Получаем путь где лежит файл скрипта в виде str
file = os.path.join(scriptDir, "LayoutBook.txt")  # присоединяем к пути имя файла

# Делаем проверку, если файл не существует, завершаем выполнение
if os.path.isfile(file) is False:
    sys.exit("File does not exists: {}".format(file))

layoutTree = GetNavigatorTree(API_LayoutMap)  # Получаем дерево книги макетов
parentChildDict = dict()  # Объявляем словарь


def GetItemsFromTree(tree, typeSet):
    """
    Функция получает список всех однотипных элементов переданного "дерева"/словаря
    """
    l = []
    for k in tree.keys():
        if k.itemType == typeSet:
            l.append(k)
        l.extend(GetItemsFromTree(tree[k], typeSet))
    return l


def FindItemByName(items, name):
    """
    Функция поиска элемента по имени
    """
    for item in items:
        if item.name == name:
            return item
    return list(layoutTree)[0]
    # Если не найдено ни каких совпадающих элементов, то вовращается корневой элемент (сама книга в книге макетов)


def FindParentItemByName(name):
    """
    Функция поиска поднабора по имени
    """
    return FindItemByName(GetItemsFromTree(layoutTree, API_SubSetNavItem), name)


def FindChildItemByName(name):
    """
    Функция поиска макета по имени
    """
    return FindItemByName(GetItemsFromTree(layoutTree, API_LayoutNavItem), name)


masters = GetItemsFromTree(layoutTree, API_MasterLayoutNavItem)  # Получаем список всех основных макетов

with open(file, encoding='utf-8') as f:  # Так как мы в России, то у нас могут встречаться наименования на кириллице,
    # соотвественно необходимо указывать параметр encoding функции open
    for line in f.read().splitlines():  # Проходимся по файлу построчно

        regExpMatch = re.compile("^Subset (.*), Parent: (.*)$").match(line)
        # Создаем регулярное выражение, если оно по формату совпадает с текущей строкой,
        # то к regExpMatch присваиваются два объекта:
        # первый (group(1)) после "Subset "  =  (.*)
        # второй (group(2)) после ", Parent:"  =  (.*)

        if regExpMatch is not None:  # Если совпадение произошло
            subsetName = regExpMatch.group(1)  # Присваиваем отдельно первый объект регулярного выражения
            parentName = regExpMatch.group(2)  # И второй объект
            print("Subset {}, Parent: {}".format(subsetName, parentName))

            # Создаем архикадовский объект (поднабор) в книге макетов
            newSubSet = APIObject()
            newSubSet.name = subsetName
            newSubSet.itemType = API_SubSetNavItem
            newSubSet.mapId = API_LayoutMap
            CreateNavigatorItem(newSubSet, FindParentItemByName(parentName))  # Функция, которая непосредственно создает
        else:
            regExpMatch = re.compile('^(.*), Master: (.*), Parent: (.*)$').match(line)
            if regExpMatch is not None:
                layoutName = regExpMatch.group(1)
                masterName = regExpMatch.group(2)
                parentName = regExpMatch.group(3)
                print("{}, Master: {}, Parent: {}".format(layoutName, masterName, parentName))

                # Создаем архикадовский объект (макет) в книге макетов
                newLayout = APIObject()
                newLayout.name = layoutName
                newLayout.itemType = API_LayoutNavItem
                newLayout.mapId = API_LayoutMap
                # У макетов есть обязательная база данных, которая сожержит информацию об основном макете
                newLayout.db = APIObject()
                newLayout.db.typeID = APIWind_LayoutID
                masterLayoutItem = FindItemByName(masters, masterName)
                newLayout.db.masterLayoutUnId = masterLayoutItem.db.databaseUnId
                if parentName not in parentChildDict:  # Если имя родительского каталога не в словаре parentChildDict
                    # То создаем элемент в нужном месте книги макетов
                    CreateNavigatorItem(newLayout, FindParentItemByName(parentName))
                    parentChildDict[parentName] = list()
                    # И добавляем к словарю пару ключ-имя родителя и значение-пустой список
                else:  # Если имя родительского каталога в словаре parentChildDict
                    # То создаем элемент в книге макетов, в нужном "месте"(например, поднаборе),
                    # после последнего элемента в этом "месте"
                    CreateNavigatorItem(newLayout, FindParentItemByName(parentName),
                                        FindChildItemByName(parentChildDict[parentName][-1]))
                parentChildDict[parentName].append(layoutName)  # Добавляем к ключу имя макета

        if regExpMatch is not None:  # Если регулярное выражение не пустое, то есть было хоть какое-то совпадение,
            layoutTree = GetNavigatorTree(API_LayoutMap)  # то обновляем дерево (layoutTree)
