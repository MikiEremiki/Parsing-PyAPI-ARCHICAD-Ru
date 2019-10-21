elemInfos = {}  # Объявили словарь

print('{:-^40}'.format('CHECKING FOR DUPLICATE IDs'))  # Выводим в консоль строку с 40 символами
for elemGuid in GetSelectedElements():  # Перебираем каждый виделенный элемент
	elemInfos.setdefault(GetInfoString(elemGuid), set()).add(elemGuid)  # Для каждого элемента записываем в словарь
# в качестве ключа ID, а в качестве занчений множество (set) из GUID

print('Duplicated IDs:')
for key, values in elemInfos.items():  # перебираем каждую пару ключ-значение
	if len(values) > 1:  # Если длина значений, или кол-во GUID больше чем 1
		print(key)  # значит печатаем ключ (одинаковые ID выбранных элементов элементов)
print('{:-^40}'.format(''))
