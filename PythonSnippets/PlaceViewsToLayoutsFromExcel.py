import os
import sys
import re
import xlrd

# Создаем путь к файлу Excel
excelFileName = "LayoutBook.xls"
excelFilePath = os.path.join(os.path.dirname(sys.argv[0]), excelFileName)


# Проверяем, что файл там есть
if os.path.isfile(excelFilePath) is False:
    sys.exit("File does not exists: {}".format(excelFilePath))


# Открываем книгу по этому пути
xl_workbook = xlrd.open_workbook(excelFilePath)
xl_sheet = xl_workbook.sheet_by_index(0)


layoutTree = GetNavigatorTree(API_LayoutMap)  # Получаем книгу макетов
viewTree = GetNavigatorTree(API_PublicViewMap)  # Получаем карту видов
layoutTreeRoot = list(layoutTree)[0]  # В эту переменную записываем корневой элемент книги макетов
subSetTree = [(layoutTreeRoot, 0)]  # Сюда записываем поднаборы имеющиеся на старте (и это так же сама книга)


def GetChildrenFromTree(tree, subSetTree):
    """
    Функция возвращает все элементы в указанном месте дерева, где должен быть расположен макет или чертеж
    """
    if not subSetTree:
        return list(tree.keys())
    if subSetTree[0][0] == layoutTreeRoot:
        return GetChildrenFromTree(tree[list(tree)[0]], subSetTree[1:])
    for k in tree.keys():
        if k.name.strip() == subSetTree[0][0].name.strip() and k.uiId.strip() == subSetTree[0][0].uiId.strip():
            return GetChildrenFromTree(tree[k], subSetTree[1:])
    for k in tree.keys():
        folderName = '{} {}'.format(subSetTree[0][0].uiId.strip(), subSetTree[0][0].name.strip())
        if folderName.strip() == k.name.strip():
            return GetChildrenFromTree(tree[k], subSetTree[1:])
    for k in tree.keys():
        if subSetTree[0][0].name.strip() == k.name.strip():
            return GetChildrenFromTree(tree[k], subSetTree[1:])
    return GetChildrenFromTree(tree, subSetTree[1:])


def GetParent(actIndex):
    global subSetTree
    for i in reversed(range(1, len(subSetTree))):
        if subSetTree[i][1] >= actIndex:
            del subSetTree[i]
    return subSetTree[-1][0]


def GetParentTree():
    """
    Функция возвращающая, поднабор, где должен был распологаться вид
    """
    treeStr = ''
    for parent in subSetTree[1:]:
        treeStr += '{} {}/'.format(parent[0].uiId, parent[0].name)
    return treeStr


def FindItemByIDName(items, ID, name):
    """
    Функция находит элемент навигатора по ID и имени
    """
    for item in items:
        if item.name.strip() == name and item.uiId.strip() == ID:
            return item
    for item in items:
        if '{} {}'.format(item.uiId.strip(), item.name.strip()) == name:
            return item
        if '{}{}'.format(item.uiId.strip(), item.name.strip()) == name:
            return item
    return None


def FindViewItemByIDName(viewIDName):
    """
    Функция ищет вид по ID и имени
    """
    view = FindItemByIDName(GetChildrenFromTree(viewTree, subSetTree), '', viewIDName)
    if view is None:
        PrintError('Could not found view: {}{}'.format(GetParentTree(), viewIDName))
    return view


def FindLayoutBookItemByIDName(ID, name):
    """
    Функция ищет макет по ID и имени
    """
    layoutBookItem = FindItemByIDName(GetChildrenFromTree(layoutTree, subSetTree), ID, NAME)
    if layoutBookItem is None:
        PrintError('Could not found layout book item: {}{} {}'.format(GetParentTree(), ID, NAME))
    return layoutBookItem


def CreateDrawingFromView(viewIDName, pos):
    """
    Функция создает чертеж в указанной позиции
    """
    element = APIObject()
    element.head = APIObject()
    element.head.typeID = API_DrawingID
    element.head.hasMemo = False
    element.drawingGuid = FindViewItemByIDName(viewIDName).guid  # GUID чертежа должен соответствовать GUID вида
    element.pos = APIObject()
    element.pos.x, element.pos.y = pos  # Указываем позицию вида
    CreateDrawing(element)


placedViewNumber = 0
for row_idx in range(1, xl_sheet.nrows):
    for column_idx in range(1, xl_sheet.ncols):
        idCell = xl_sheet.cell(row_idx, column_idx)

        if idCell.value != '':
            ID = idCell.value.strip()
            NAME = xl_sheet.cell(row_idx, column_idx + 1).value.strip()
            MASTER_NAME = xl_sheet.cell(row_idx, column_idx + 3).value.strip()
            PARENT = GetParent(column_idx)
            layoutBookItem = FindLayoutBookItemByIDName(ID, NAME)  # Определяем макет или поднабор по id и имени
            if MASTER_NAME == '':
                subSetTree.append((layoutBookItem, column_idx))  # Если в текущей строке  Excel нет макета,
                # значит это поднабор, следовательно добавлеям его в список поднаборов
            else:
                VIEW_IDNAME = xl_sheet.cell(row_idx, column_idx + 2).value.strip()  # Записываем название вида
                if VIEW_IDNAME != '':
                    with DatabaseSwitchGuard(layoutBookItem.db):  # Если вид задан, то переходим к его созданию,
                        # при этом сохраняем создание одного чертежа в одну операцию
                        layoutSettings = GetLayoutSettings(layoutBookItem)  # Получаем доступ к настройкам макета
                        CreateDrawingFromView(VIEW_IDNAME, (layoutSettings.sizeX / 2000, layoutSettings.sizeY / 2000))
                        # Создаем чертеж в центре макета
                        placedViewNumber += 1
            break
print("Placed {} views based on {}".format(placedViewNumber, excelFileName))
