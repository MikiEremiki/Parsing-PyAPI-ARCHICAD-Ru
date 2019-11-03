elemTypeDict = {}  # Обявляем словарь
elemList = GetElementList(API_ZombieElemID)  # Получаем список всех элементов (а точнее GUID) типа Zombie,
# по сути это все элементы
print("{} elements".format(len(elemList)))  # Выводим кол-во всех элементов

for elemGuid in elemList:  # Проходимся по всем этим элементам
    elemType = GetElementType(elemGuid)  # Получаем тип (номер типа) элемента
    elemTypeDict.setdefault(elemType, 0)  # Записываем в качестве ключа номер типа элемента
    elemTypeDict[elemType] += 1  # Значение увеличиваем на единицу

for elemType in elemTypeDict.keys():  # Проходимся по ключам из словаря
    print("\t{} {}".format(elemTypeDict[elemType], GetElementTypeName(elemType)))  # Вывод в общем то все видели
    # первым идет значение, по ключу, вторым идет локализованное имя от ключа
