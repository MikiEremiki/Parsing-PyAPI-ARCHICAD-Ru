roomNumberFormat = 'NEW ID {}'  # Формат имени зоны
startNumberingToRight = False  # Стратовая переменная
zoneGridEpsilon = 2


def find_step(l):
    """
    Функция находит шаг
    :param l: список значнеий одной из координат x или y
    """
    minD = 0  # Минимальное значение
    step = 0  # Начальный шаг
    sortedList = sorted(set(l))  # Отсортированный набор, при этом преобразованный в список
    for ii in range(len(sortedList) - 1):
        d = abs(sortedList[ii + 1] - sortedList[ii])   # Значение d может быть >= 0
        # Вычисляем разницу, по модулю, между вторым и первым по счету значениями из списка l
        if minD == 0 or d < minD:
            minD = d
        if d > zoneGridEpsilon and (step == 0 or d < step):
            step = d
    return minD + zoneGridEpsilon if step == 0 else step


def get_grid_index(pos, first, step):
    """
    Функция возращяет индекс "сетки"
    """
    return int((pos - first) / (1 if step == 0 else step))


def make_grid(zones, startingPos):
    """
    Функция создает сетку
    :param startingPos: координаты зоны на которой сделан щелчок
    """
    # Для каждой зоны из переданных зон записываем координаты x и y и в список
    x = [zone.pos.x for zone in zones]
    y = [zone.pos.y for zone in zones]

    minX, minY, stepX, stepY = min(x), min(y), find_step(x), find_step(y)  # Определяем минимальные x и y и шаги
    maxXIndex, maxYIndex = get_grid_index(max(x), minX, stepX), get_grid_index(max(y), minY, stepY)
    grid = [[None] * (maxXIndex + 1) for _ in range(maxYIndex + 1)]
    # Создаем список списков (grid) из сетки с группировкой зон по оси Х

    for ii in range(len(x)):
        xIndex, yIndex = get_grid_index(x[ii], minX, stepX), get_grid_index(y[ii], minY, stepY)
        grid[yIndex][xIndex] = zones[ii]
    # Записываем в соответствующий индекс сетки, соответствующую зону

    return (grid, min(maxXIndex, get_grid_index(startingPos.x, minX, stepX)),
            min(maxYIndex, get_grid_index(startingPos.y, minY, stepY)))


def get_selected_zones():
    """
    Функция возвращает выбранные зоны для дальнейшей обработки в виде списка
    """
    selectedZoneGuids = []  # Создаем список
    for elemGuid in GetSelectedElements():
        if GetElementType(elemGuid) == API_ZoneID:  # Если элемент является зоной, то добавляем его в список
            selectedZoneGuids.append(elemGuid)
    return selectedZoneGuids


def collect_zones():
    """
    Функция собирает зоны
    """
    zonesPerFloors, startingPos = {}, None  # Объявляем словарь и стартовую позицию
    selectedZoneGuids = get_selected_zones()  # Получаем выбранные зоны
    if not selectedZoneGuids:  # Если список оказался пустым, значит были выбраны не зоны или вообще ничего не выбрано
        PrintError("Please select at least one zone!")
        return zonesPerFloors, startingPos  # Возвращаем пустые переменные
    print("Please click one of the selected zones from where to start the numbering!")
    clickedZoneGuid = ClickElement()  # Указываем элемент, с которого начнется счет

    for zoneGuid in selectedZoneGuids:
        zone, memo = GetZone(zoneGuid)  # Получаем для доступа свойства зоны
        if zoneGuid == clickedZoneGuid:  # Если текущая зона в цикле, является зоной на которой был сделан щелчок
            startingPos = zone.pos  # То позиция зоны является стартовой (а это информация о координатах точки (x, y))
        floorKey = (zone.head.floorInd, zone.roomBaseLev)
        # Записываем информацию о номере этажа и отметке от нуля этого этажа в кортеж
        if floorKey in zonesPerFloors:  # Если эта информация о этаже и отметке содержится в словаре
            zonesPerFloors[floorKey].append(zone)  # То добавляем zone к этому ключу (floorKey)
        else:
            zonesPerFloors[floorKey] = [zone]  # Иначе значение к этому ключу записываем zone
    # В результате мы имеем словарь содержащий пары
    # ключ = (номер этажа и отметк) и значение = (список всех зон на этом этажет на этой отметке)
    return zonesPerFloors, startingPos  # Вернули эти значения


def change_zones(zonesPerFloors, startingPos):
    """
    Функция изменяет зоны
    """
    if zonesPerFloors and startingPos is None:  # Если значения пустые, то возвращаем ошибку
        PrintError("Wrong click!")
        return

    with UndoScope("Changing Zone Numbers"):
        for floorKey in zonesPerFloors.keys():  # Проходимся по ключам из словаря
            grid, xIndexStart, yIndexStart = make_grid(zonesPerFloors[floorKey], startingPos)
            # Вернули сетку с зонами и стартовые индексы с которых начанить переименование
            xIndex, yIndex = xIndexStart, yIndexStart
            gridHeight = len(grid)  # кол-во элементов сетки по длине
            gridWidth = len(grid[0])  # кол-во элементов сетки по ширине
            gridElemCount = gridWidth * gridHeight  # Кол-во элементов в сетке (на этаже)
            count = 0
            isDirRight = startNumberingToRight  # Направление правое или левое
            for _ in range(gridElemCount):  # Проходимся по всем элементам из сетки зон
                zone = grid[yIndex][xIndex]  # Выбираем зону по индексу
                if zone is not None:  # Если зона является зоной
                    count += 1
                    zone.roomNoStr = roomNumberFormat.format(count)  # Присваиваем имя зоны по нашему формату
                    ChangeZone(zone)  # Функция для изменения зоны

                xIndex += (1 if isDirRight else -1)
                # В зависимости от направления, мы или увеличиваем или уменьшаем индекс
                if xIndex == (gridWidth if isDirRight else -1):
                    yIndex = (yIndex + (1 if startNumberingToRight else -1)) % gridHeight
                    isDirRight = (yIndex - yIndexStart) % 2 == (0 if startNumberingToRight else 1)
                    xIndex = (0 if isDirRight else gridWidth - 1)
                # Определяем новые индексы x и y, разбирать лень, если честно, если кто-то не осилит пишите помогу)))

            print("{} zones will be changed on floor {}".format(count, floorKey[0]))


change_zones(*collect_zones())
