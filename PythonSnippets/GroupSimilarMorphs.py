morphDict = {}  # Объявляем словарь

for morphGuid in GetElementList(API_MorphID):  # Провходимся по всем морфам, пристутствующим в проекте
    morph = GetElement(morphGuid)  # Получаем элемент, чтобы можно было обратится к его свойствам
    material = morph[0].material.attributeIndex  # Записываем индекс покрытия этого элемента
    morphDict.setdefault(material, []).append(morphGuid)
    # Добавляем в словарь GUID морфа, в качестве ключа выступает покрытие

with UndoScope("Create Groups for Morphs"):  # Специальная конструкция для записи всех действий в одну опреацию,
    # которую в Архикаде можно отменить
    for similarMorphs in morphDict.values():  # Проходимся по всем значениям из словаря
        CreateElementGroup(similarMorphs)  # Создаем группу для переданных элементов (в данном случае морфов)

print("{} Groups Created".format(len(morphDict.values())))  # Выводим кол-во созданных групп
