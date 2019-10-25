# Не достатком скрипта, является довольно долгая скорость работы.

materials = GetAttributeDictionary(API_MaterialID)  # Получаем список реквизитов покрытий

# Создаем архикадовские покрытие для использования в скрипте
material1 = APIObject()
material1.attributeIndex = list(materials)[0]  # Назначаем первый из словаря материал
material1.overridden = True  # Этот переопределенный атрибут, я так понял должен быть всегда,
# если происходит задание покрытия отличное по умолчанию, как у нас

material2 = APIObject()
material2.attributeIndex = list(materials)[1]
material2.overridden = True

w = 2

for x in range(8):
    for y in range(8):
        body = ModelerBody()  # Создаем тело, функции ModellerBody в документации нет, тут только догадываться,
        # по сути это, чтобы у объекта с именем body появились соответсвующие функции, для моделирования тела.
        body.Create()  # Начинаем "запись" тела. В нашем случае квадрата

        # Создаем точки углов квадрата 2х2 м
        v1 = body.AddVertex(x * w, y * w, 0)
        v2 = body.AddVertex(w + x * w, y * w, 0)
        v3 = body.AddVertex(w + x * w, w + y * w, 0)
        v4 = body.AddVertex(x * w, w + y * w, 0)

        # Создаем стороны квадрата
        e1 = body.AddEdge(v1, v2)
        e2 = body.AddEdge(v2, v3)
        e3 = body.AddEdge(v3, v4)
        e4 = body.AddEdge(v4, v1)

        # Указываем направление нормали
        n1 = body.AddNormal(0, 0, 1)

        # В зависимости от четный ли квадрат или нет, применяем одно или другое покрытие
        if (x + y) % 2 == 1:
            f1 = body.AddPolygon([e1, e2, e3, e4], n1, material1)
        else:
            f1 = body.AddPolygon([e1, e2, e3, e4], n1, material2)

        body.Finish()  # Заканчиваем запись квадрата

        morphPars = APIObject()   # Объявляем объект архикадовский

        # Это я добавил от себя, чтобы с плана тоже было графическое разделение по квадратам

        # morphPars.head = APIObject()
        # morphPars.head.typeID = API_MorphID
        # if (x + y) % 2 == 1:
        #     morphPars.useCoverFillType = True
        #     morphPars.coverFillType = 94
        morphMemo = APIObject()  # еще один объект
        morphMemo.morphBody = body  # но для него задаем свойство morphBody = body
        # (иначе как я понял значение по умолчанию None, как и для многих других свойств)

        CreateMorph(morphPars, morphMemo)  # Создаем Морф, функция возвращает GUID, как и все остальные которые создают
        # какой-либо элемент
