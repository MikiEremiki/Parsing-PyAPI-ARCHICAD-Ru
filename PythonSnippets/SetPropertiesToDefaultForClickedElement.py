elem = ClickElement()  # Указываем элемент

with UndoScope("Set Element Properties to Default"):
    for d in GetElementPropertyDefinitionDictionary(elem, API_PropertyDefinitionFilter_UserDefined).values():
        # Проходимя по всем значениям (пользовательским, так как установлен фильтр)
        if d.canValueBeEditable and not d.defaultValue.hasExpression:
            # Если значение является редактируемым (canValueBeEditable) и содержит ли оно значение по умолчанию или нет
            p = GetElementProperty(elem, d.guid)  # То получаем доступ к свойству по его guid
            if not p.isDefault:  # Проверям, что не стоит значение по умолчанию
                p.isDefault = True  # Меняем его на значение по умолчанию
                SetElementProperty(elem, p)  # Устанавливаем/применяем этой свойство элементу
                print("Changed \"{}\" property to it's default value.".format(d.name))
                # Выводим это свойство в консоль
