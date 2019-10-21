import re  # Импортируем модуль регулярных выражений

elemInfos = {}  # Объявили словарь

# three capital letters (A-Z) followed by a '-' and 3 numbers
# 3 заглавных символа (от A до Z) за которыми следует '-' и 3 цифры
checkPattern = re.compile('^[A-Z]{3}-[0-9]{3}$')  # создаем эту строку (паттерн), для проверки ID элементов

print('{:-^40}'.format('CHECKING ID FORMAT'))
for elemGuid in GetSelectedElements():  # Перебираем все выделенные объекты
	elemInfos[elemGuid] = GetInfoString(elemGuid)   # В словарь записываем пары - ключ (GUID) : значение (id этого GUID)

print('Invalid formatted IDs:')
for key, value in elemInfos.items():  # Проходимся по всем парам из словаря
	print(checkPattern.match(value))
	if checkPattern.match(value) is None:  # Если паттерн является None, то id в контексте этого скрипта не корректен
		# Как именно работает match не доконца понял, но видимо перебирает все варианты из re.compile('')
		# и при первом совпадении выдаст специальный объект из библиотеки re, иначе None
		print((value, key))  # Выводим не корректные id c GUID
print('{:-^40}'.format(''))
