print('{:-^30}'.format('BEGIN'))

guid = ClickElement()

element_head = GetElementHeader(guid)  # Получаю доступ к свойствам head
element_type = GetElementTypeName(element_head.typeID)  # Получаю локализованное имя типа элемента
print(guid)
print(element_type, "typeID: ", element_head.typeID)

if guid is not None:
    element = GetElement(guid)
    print("Элемент является: ", element)
    if element is not None:
        print("Можно вывести список всех свойств")
        print(type(element))
        # if isinstance(element, tuple):
        #         #     element[0].List()
        #         #     element[1].List()
        #         # else:
        #         #     element.List()
    else:
        print("Нельзя вывести список всех свойств")

print('{:-^30}'.format('END'))
