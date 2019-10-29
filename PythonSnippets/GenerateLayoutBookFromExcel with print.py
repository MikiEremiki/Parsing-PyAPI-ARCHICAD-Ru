import os  # Импортиуем модули
import sys
import re
import xlrd

excelFileName = "LayoutB.xls"  # Записываем название файла Excel, из которого будем считывать данные
# Создаем путь по которому находится этот файл, в данном случае, он находится там же где и выполняемый скрипт
excelFilePath = os.path.join(os.path.dirname(sys.argv[0]), excelFileName)

# Если файла не существует, то завршить выполнение с сообщением, что файл не найден
if os.path.isfile(excelFilePath) is False:
    sys.exit("File does not exists: {}".format(excelFilePath))

xl_workbook = xlrd.open_workbook(excelFilePath)  # Открываем книгу
xl_sheet = xl_workbook.sheet_by_index(0)  # Ссылаемся на первый лист книги

layoutTree = GetNavigatorTree(API_LayoutMap)  # Получаем "дерево" книги макетов
subSetTree = [(list(layoutTree)[0], 0)]  # Создали список из одного кортежа содержащий два элемента (книгу макетов и 0)
print("subSetTree в начале: ", subSetTree)
print("=" * 10)


# Объявляем функцию, которой передаем "вкладку" навигатора и дополнительный аргумент типа set (но не обязательно)
def GetItemsFromTree(tree, typeSet=None):
    l = []  # Создаем список
    for k in tree.keys():  # Запускаем цикл, для прохода по всему дереву из переданной вкладки навигатора
        if typeSet is None or k.itemType in typeSet:  # Если тип элемента навигатора
            # входит в множество искомых типов элементов
            l.append(k)  # То добавить этот элемент к списку l
        l.extend(GetItemsFromTree(tree[k], typeSet))  # Рекурсивно добавляем к list другие найденные элементы навигатора
        # в подэлементах (папках, поднаборах, и т.д.)
    return l  # Результатом функции явялется возвращенный список всех найденных элементов


# В данном случае мы получаем все основные макеты из книги макетов
masters = GetItemsFromTree(layoutTree, {API_MasterLayoutNavItem})


# Функция возвращает всех "детей", входящих в корневой элемент, переданного ей дерева
# Если бы я в экселе не прописывал поднаборы, а только макеты, то (для книги макетов) они все будут созданы в "книге"
# Так как для книги макетов в любом случае возвращается корневая книга, если не передано во 2-ой аргумент ничего другого
def GetChildrenFromTree(tree, subSetTree):
    if not subSetTree:
        print("RETURN list(tree.keys()): ", list(tree.keys()))
        print("=" * 10)
        return list(tree.keys())
    for k in tree.keys():
        # name и uiId по крайней мере для книги, в корне книги макетов, одинаково
        if k.name == subSetTree[0][0].name and k.uiId == subSetTree[0][0].uiId:
            print(k, " : ", k.name)
            print("subSetTree[1:] ", subSetTree[1:])
            return GetChildrenFromTree(tree[k], subSetTree[1:])
    return []  # Если элементов не существует (актуально для видов и наборов издателя), то возвращает пустой список


def FindItemByName(items, name):  # передаем элементы и искомое имя
    """
    Функция поиска элемента по имени
    """
    for item in items:
        if item.name == name:  # Если находится имя, то возвращаем его
            return item
    PrintError('Bad Name: {}'.format(name))  # В противном случае говорим, что имя не верное и возвращаем None
    return None


def FindItemByIDName(items, ID, name):
    """
    Функция поиска элемента по ID и по имени
    """
    for item in items:
        if item.name == name and item.uiId == ID:
            return item
    return None


# Функция создания элемента навигатора
def CreateSubSetItem(ID, name, parent):
    """
    Функцию передаются ID, имя и имя "родителя" в котором необходимо создать поднабор
    """
    newSubSet = APIObject()  # Создаем новый объект архикада
    newSubSet.uiId = ID
    newSubSet.customUiId = True
    newSubSet.name = name
    newSubSet.customName = True
    newSubSet.itemType = API_SubSetNavItem  # Присваиваем ему тип подэлемента навигатора
    newSubSet.mapId = API_LayoutMap  # Присваиваем ему к какой карте/вкладке навигатора элемент будет принадлежать
    CreateNavigatorItem(newSubSet, parent)  # Создаем элемент
    return newSubSet  # Возвращаем этот созданный элемент


def CreateOrChangeLayoutItem(ID, name, masterName, parent, oldItem=None):
    """
    Функция создает или изменяет элемент макета
    """
    newLayout = APIObject() if oldItem is None else oldItem
    # Делаем проверку, если элемент уже существует, то используем его в качестве объекта
    newLayout.uiId = ID
    newLayout.customUiId = True
    newLayout.name = name
    newLayout.customName = True
    newLayout.itemType = API_LayoutNavItem
    newLayout.mapId = API_LayoutMap
    newLayout.db = APIObject()
    newLayout.db.typeID = APIWind_LayoutID
    # Находим основной макет, если не находим, то возвращается ошибка и не будут созданы макеты с этим основным макетом
    masterLayoutItem = FindItemByName(masters, masterName)
    newLayout.db.masterLayoutUnId = masterLayoutItem.db.databaseUnId  # Присваиваем макету основной макет
    if oldItem is None:  # Если существующий элемент (в данном случае макет) не найден
        parentChildren = GetChildrenFromTree(layoutTree, subSetTree)  # то получаем "родителя" данного элемента
        if not parentChildren:  # Если родителя быть не должно
            CreateNavigatorItem(newLayout, parent)  # То создаем элемент в корневой ветке родителя
        else:
            CreateNavigatorItem(newLayout, parent, parentChildren[-1])
            # Иначе создаем элемент в конце родительского элемента
    else:
        ChangeNavigatorItem(newLayout)  # Иначе обновляем этот макет
    return newLayout  # Возвращаем этот макет


def GetParent(actIndex):  # Получаем родителя
    global subSetTree  # Определям глобальную переменную, а точнее, что мы хотим ей воспользоваться
    for i in reversed(range(1, len(subSetTree))):  # Для первой итерации, когда родителем является корневой элемент
        # (сама книга), цикл не актуален. так как создает последовательность из одного элемента
        print("итерация ", i)
        print("sub[{}]: {}, {}".format(i, subSetTree[i][1], subSetTree))
        print("actInd", actIndex)
        print(subSetTree[i][0].name, " int: ", subSetTree[i][1])
        if subSetTree[i][1] >= actIndex:
            print("subSetTree[i][1] >= actIndex: ", subSetTree[i][1] >= actIndex)
            del subSetTree[i]
    print("return", subSetTree[-1][0].name)
    print("=" * 10)
    return subSetTree[-1][0]


newSubSetNumber, newLayoutNumber = 0, 0
# Проходимся по всем ячейкам таблицы, кроме 1 строки и 1 столбца
for row_idx in range(1, xl_sheet.nrows):
    for column_idx in range(1, xl_sheet.ncols):
        idCell = xl_sheet.cell(row_idx, column_idx)  # Присваиваем содержимое ячейки в idCell
        # Если значение в ячейке нет, то переходим к следующей итерации
        if idCell.value != '':  # Если значение, есть идем дальше
            # strip() удаляет/опускает/очищает пробелы в начале и в конце строки
            # Записываем значение ячейки в ID
            ID = idCell.value.strip()
            # В имя записываем значение из следующей ячейки в строке
            NAME = xl_sheet.cell(row_idx, column_idx + 1).value.strip()
            # В Master записываем имя основного макета из 4 ячейки по строке
            MASTER_NAME = xl_sheet.cell(row_idx, column_idx + 3).value.strip()
            # Получаем "родителя"
            print("Знач{}, номер столбца{}".format(idCell.value, column_idx))
            PARENT = GetParent(column_idx)
            print("PARENT", PARENT.name)
            print("=" * 10)
            # Определяем был ли уже такой элемент в навигаторе
            print("func get_children_from_tree")
            oldItem = FindItemByIDName(GetChildrenFromTree(layoutTree, subSetTree), ID, NAME)

            # Самое главное, что по MASTER_NAME мы определяем,
            # что тот элемент к которому мы перешли является макетом или поднабором
            if MASTER_NAME == '':  # Если записи про основной макет нет,
                # То создаем поднабор
                newSubSetNumber += 1  # Счетчик добавленных поднаборов
                if oldItem is None:  # Если старый элемент отсутсвует
                    subSetTree.append((CreateSubSetItem(ID, NAME, PARENT), column_idx))
                    print(NAME, "Элемента нет в книге и добавляем его к списку \"Родителей\"", subSetTree)
                    print("=" * 10)
                    # Добавляем к списку поднаборов запись о расположении этого поднабора, перед этим создав его
                else:  # Если старый/существующий элемент найден
                    print("olditem")
                    print(oldItem.name)
                    subSetTree.append((oldItem, column_idx))  # Добавляем его расположение к списку поднаборов
                    print(NAME, "Элемента уже есть и добавляем его к списку \"Родителей\"", subSetTree)
                    print("=" * 10)
            else:  # Если запись о основном макете найдена, то создаем макет или обновляем его
                newLayoutNumber += 1  # Счетчик добавленных макетов
                print(NAME, "Макет", subSetTree)
                print("=" * 10)
                CreateOrChangeLayoutItem(ID, NAME, MASTER_NAME, PARENT, oldItem)

            layoutTree = GetNavigatorTree(API_LayoutMap)
            break
print("Создано {} поднаборов и {} макетов из {}".format(newSubSetNumber, newLayoutNumber, excelFileName))
