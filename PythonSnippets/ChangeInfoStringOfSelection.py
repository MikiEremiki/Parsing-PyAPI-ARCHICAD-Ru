elementTables = {}  # Создали словарь

# first 3 letters of element type followed by a '-', floor number plus 2 numbers
# Первые 3 символа имени типа элемента, затем '-', номер этажа плюс 2 цифры (счетчик).
# Номер этажа не так очевиден. Например если есть 1 этаж с номером 1, то выведется нулевой этаж,
# соотвественно можно прибавлять 1, для одинаковости чтения номера этажа.
# Также стоит отметить, что этаж под первым нумеруется сразу с -1.
infoStringFormat = '{:.3}-{}{:02d}'  # Заготовка для замены id на данный формат.

for elemGuid in GetSelectedElements():  # перебираем все выбранные элементы и связываем их с elemGuid
	elemHead = GetElementHeader(elemGuid)  # получаем основные параметры элемента (тип, id, номер этажа и т.д.)
	elementTables.setdefault(elemHead.typeID, {}).setdefault(elemHead.floorInd, []).append(elemGuid)
# Может показаться сложным, но 1-ый setdefault записывается ключ в виде ID типа элемента из документации можно
# можно узнать, что для стен это '1', и создаем пару значений, 'номер типа эл.' : {}
# Затем второй setdefault, к внутреннему словарю добавляем пару значений, 'номер этажа' : []
# И в список записываем GUID данного элемента. И так с каждым выбранным элементом.
# Соответсвенно setdefault проверяет существует ли данный ключ, если да, то возвращает его, если нет, то создастся
# новая пара значений

with UndoScope("Changing Info Strings"):  # Как и в ApplyFavorite это специальная функция (в документация написано,
	# что class, не знаю как правильно) записывающая все что находится внутри нее в одну операцию ARCHICAD,
	# которую можно отменить
	for elemType in elementTables.keys():  # Начинаем перебирать элементы, сначла по типу
		elemTypeName = GetElementTypeName(elemType)  # Получаем локализованное название типа элемента (напр. 'Стена')
		for (floorInd, elemGuids) in elementTables[elemType].items():  # Начинаем перебор по этажам
			# В кортеж записываем номер этажа и все элементы расположенные на нем
			count = 0
			for elemGuid in elemGuids:
				count += 1
				infoString = infoStringFormat.format(elemTypeName, floorInd, count).upper()  # Создаем строковую
			# переменную и компануем ее сначала именем типа, потом через '-' номером этажа и номером порядковым от 01
				ChangeInfoString(elemGuid, infoString)  # Используем функцию, чтобы прописать эту строку в ID элемента.
			print("Changed {} info string(s) of {}(s) on floor {}".format(count, elemTypeName, floorInd)) # Ну и принт
		# просто для большей интерактивноси, видеть на каких этажах, какие выбранные типы и сколько их изменилось
