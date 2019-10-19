morphLayer = SearchAttributeByName(API_LayerID, "Конструктив - Колонны")  # Функция SearchAttributeByName
# (поиск атрибута по имени) возвращает индекс атрибута/реквизита указанного в качестве второй переменной
count = 0

with UndoScope("Изменение слоя морфов"):  # Специальный класс который объединяется применяемые функции в одну операцию
	for morphGuid in GetElementList(API_MorphID):  # Получаем список всех элементов, в данном случае морфов
		morphHeader = GetElementHeader(morphGuid)  # Получаем список основных параметров элемента morphGuid 
		# и записываем их в "переменную" morphHeader
		if morphHeader.layer != morphLayer.index:  # Если слой элемента не является слоем на котором мы хотим его видеть
			morphHeader.layer = morphLayer.index  # То переписать/назначить нужный нам слой
			# Так как это мы только изменили layer для "переменной", то нужно теперь применить это к элементу в ARCHICAD
			ChangeElementHeader(morphHeader)  # Применяем это изменение к элементу, дополнительно функция возвращает GUID
			count += 1

print("Changed {} Morph(s)".format(count))
