import os
import sys
import xlsxwriter  # Импортируем модуль для записи в Excel

scriptDir = os.path.dirname(sys.argv[0])  # Получаем путь директории в которой находится скрипт
outputFile = os.path.join(scriptDir, "Test.xlsx")  # Добавляем к пути имя файла, в него будем записывать данные


def ExportPropertiesToExcel(elemGuid, fileName):  # Объявляем функцию, которая экспортирует свойства в Эксель
    workbook = xlsxwriter.Workbook(fileName)  # Создаем excel файл
    worksheet = workbook.add_worksheet("Properties")  # Добавляем лист
    definitionDictionary = GetElementPropertyDefinitionDictionary(elemGuid, API_PropertyDefinitionFilter_All)
    # получаем все свойства элемента по GUID и с указанным фильтром

    headlineFormat = {'bold': True, 'bottom': True, 'align': 'center'}  # Создает форматирование первой строки
    headline = workbook.add_format(headlineFormat)  # Добавляем этот формат для применения к нужным ячейкам

    # Устанавливаем ширину колонок\столбцов
    worksheet.set_column('A:B', 55)
    worksheet.set_column('C:C', 10)

    # Записваем текст в первые три ячеки первой строки
    worksheet.write(0, 0, "PROPERTY", headline)
    worksheet.write(0, 1, "VALUE", headline)
    worksheet.write(0, 2, "DEFAULT", headline)

    # Записываем данные об элементе во вторую строку
    worksheet.write(1, 0, "Element GUID")
    worksheet.write(1, 1, elemGuid)
    worksheet.write(1, 2, False)

    row = 2  # Устанавливаем значение "указателя" на 2, чтобы делать смещение каждой новой записи
    for d in definitionDictionary.values():  # Проходимся по всем значениям из полученного словаря
        property = GetElementProperty(elemGuid, d.guid)  # Получаем свойство из элемента
    # и по указанному уникальному id самого свойства (d.guid)
        value = property.value  # Извлекаем значение этого свойства
        if isinstance(value, list):  # Является ли даннонное значение типом list
            value = repr(value)  # Тогда преобразовываем list в запись в виде str

        # Проводим запись по строчно
        worksheet.write(row, 0, d.name)  # Имя свойства
        worksheet.write(row, 1, value)  # Значение
        worksheet.write(row, 2, property.isDefault)  # Записывает True-False
        if property.definition.collectionType == API_PropertySingleChoiceEnumerationCollectionType:
            # Проверяем является ли свойство, которое выбирается из списка значений
            valList = []
            for en in property.definition.possibleEnumValues:
                valList.append(en)  # Добавляем все возможные свойства для выбора в список
            worksheet.data_validation(row, 1, row, 1,
                                      {'validate': 'list',
                                       'source': valList})
            # Добавляем в ячейку значения с проверкой данных, этот список

        row += 1  # Сдвигаем указатель на следующую строку

    workbook.close()  # Закрываем книгу


ExportPropertiesToExcel(ClickElement(), outputFile)

# Этот код служит для понимания, чем являются свойства и как их читать
# count = 3  # Три выбрано для того, чтобы номер совпадал с номером строки в Excel
# guid_click = ClickElement()
# definitionDictionary = GetElementPropertyDefinitionDictionary(guid_click, API_PropertyDefinitionFilter_All)
# for d in definitionDictionary.values():
#     property = GetElementProperty(guid_click, d.guid)
#     value = property.value
#     if isinstance(value, list):
#         value = repr(value)
#         print(d.name)
#         print(d.guid)
#         print(type(value))
#         print(type(repr(value)))
#         print(count)
#     if property.definition.collectionType == API_PropertySingleChoiceEnumerationCollectionType:
#         valList = []
#         for en in property.definition.possibleEnumValues:
#             valList.append(en)
#     count += 1
#     if count == 200:
#         break
