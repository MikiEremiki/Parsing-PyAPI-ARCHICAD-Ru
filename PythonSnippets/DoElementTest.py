# Test Functions


def DrawCircle(x, y, r):  # Объявляем функцию "Создание окружности"
    element = APIObject()  # Создаем "архикадовский объект" с присущими ему свойствами этого класса
    element.head = APIObject()  # Делаем доступными все свойства "метода" head
    element.head.typeID = API_ArcID  # Используя свойства head присваиваем тип элемента - тип дуга, соответсвенно теперь
    # у element присутствуют свойства дуги
    element.whole = True  # Объявляем что дуга должна быть цельной, то есть окружностью
    element.origC = APIObject()  # Еще делаем, возможным использование свойств центра точки окружности
    element.origC.x = x  # Делаем связываение какие значения должны брать координаты центра окружности
    element.origC.y = y
    element.r = r  # и значение радиуса
    return CreateArc(element)  # Возвращаем GUID отрисованной дуги


def DrawWall(x1, y1, x2, y2):  # Повтрояем все тоже самое с функцией для стены
    element = APIObject()
    element.head = APIObject()
    element.head.typeID = API_WallID
    element.begC = APIObject()  # Только у стены есть свои свойства, как начало
    element.begC.x = x1
    element.begC.y = y1
    element.endC = APIObject()  # и конец
    element.endC.x = x2
    element.endC.y = y2
    return CreateWall(element)


def DrawText(x, y, text):  # Повтрояем все тоже самое с функцией для текста
    element = APIObject()
    element.head = APIObject()
    element.head.typeID = API_TextID
    element.head.hasMemo = True  # Объявляем что элемент имеет дополнительные свойства (API_​ElementMemo)
    element.loc = APIObject()
    element.loc.x = x
    element.loc.y = y
    memo = APIObject()  # Создаем специальный объект memo обладающий дополнительными свойствами
    memo.textContent = text  # В частности свойством для текста
    return CreateText(element, memo)


def MakeDrawing(scale):  # Повтрояем все тоже самое с функцией для чертежа
    element = APIObject()
    element.head = APIObject()
    element.head.typeID = API_DrawingID
    element.head.hasMemo = True
    memo = APIObject()
    drawingData = DrawingData()  # Создаем элемент обладающий свойствами чертежа
    drawingData.StartDrawing(scale)  # Все последующие строки пойдут внутрь чертежа
    with UndoScope("Create Drawing Elements"):
        DrawText(-0.45, 0.2, "Hello")
        DrawCircle(0, 0, 1)
        DrawCircle(0, 0, 2)
        DrawCircle(0, 0, 3)
        DrawCircle(0, 0, 4)
        DrawCircle(0, 0, 5)
    drawingData.StopDrawing()  # Закончили наполнение чертежа 1 текстом и 5 окружностями
    memo.drawingData = drawingData  # мы создали изначально переменную drawingData,
    # заполнили ее чем то между строками start и stop, теперь ее нужно передать в функцию CreateDrawing,
    # для этого нам нужен специальный объект обладающий нужными нам свойствами, а мы его объявляли ранее (memo)
    element.bounds = drawingData.GetBounds()  # Высчитываем границы чертежа точно по содержимому
    element.bounds.xMin -= 1  # Увеличиваем границу на 1 метр со всех сторон
    element.bounds.yMin -= 1
    element.bounds.xMax += 1
    element.bounds.yMax += 1
    element.nameType = APIName_CustomName  # Так как ранее мы объявили что element является типом - чертеж,
    # то можно выбрать тип имени чертежа. Выбрали специальное
    element.name = "Test Drawing"  # Записали это имя
    return CreateDrawing(element, memo)  # Создаем сам чертеж, расположение определяется содержимым
    # В качестве return как обычно GUID чертежа


def ChangeDrawingTest(guid):  # Функция изменения чертежа
    element = GetDrawing(guid)  # Получаем свойства от указанного чертежа по GUID
    element = element[0]  # Из чертежа нам нужны свойства только первого элемента, а это был текст.
    # Не самый очевидный способ конечно, до конца так и не ясно почему только первый элемент подвергается влиянию
    element.hasBorderLine = True  # Говорим что чертеж имеет линию границы
    element.borderLineType = 1  # Ее тип
    element.borderPen += 2  # Выбираем номер пера на 2 больше от того, что было
    element.borderSize *= 1.5  # Размер границы увеличиваем в 1.5 раза
    element.angle = 3.141592654 / 12  # 15 Degrees  Делаем поворот
    element.colorMode = APIColorMode_GrayScale  # Изменяем цветовой режим
    return ChangeDrawing(element)  # Изменяем элемент в чертеже


# Test Fixture

elements = []
elements.append(DrawCircle(5, 5, 5))
elements.append(DrawWall(0, 0, 10, 0))
elements.append(DrawWall(10, 0, 10, 10))
elements.append(DrawText(5, 5, "Hello, world!"))
Alert("{} Elements Made".format(len(elements)))  # Функция для вывода предупреждений
DeleteElements(elements)  # Функция для удаления всех элементов созданных ранее
elements.append(MakeDrawing(100))  # Содаем чертеж
Alert("Drawing Made".format(len(elements)))
ChangeDrawingTest(elements[-1])  # Изменяем этот чертеж

# Clean Up


del globals()["DrawCircle"]
del globals()["DrawWall"]
del globals()["DrawText"]
del globals()["MakeDrawing"]
del globals()["ChangeDrawingTest"]  # Cоответственно в globals записываются все системные функции
# и в том числе которые вополнялись через панель python. Чтобы они там не копились их можно и нужно подтирать.
del elements
