def PrintTree(tree, level=0):  # Функция для вывода всего дерева (tree), которое в нее передается.
    # Аргумент level для создания отступов, чтобы получалась древовидная структура
    levelStr = '\t' * level
    for k in tree.keys():  # Цикл который пробегается по всем ключам одного уровня
        print(levelStr + k.name)  # Печаем имя ключа с отсутпом
        PrintTree(tree[k], level + 1)  # Рукурсивный подход, для перехода на следующий уровень дерева
        # (или для перехода к следующим элементам)


def TreeSearch(tree, search):  # Эту функцию добавил от себя. Она осуществляет поиск по имени
    for k in tree.keys():
        if k.name in search:  # Как только находит
            print(k.name)  # Выводим его в консоль с нулевым отступом
            PrintTree(tree[k], level=1)  # И вызываем рекурсивную функцию печати внутри входящего "дерева"
        TreeSearch(tree[k], search)  # Ищем дальше, для случая если задано несколько аргументов для поиска


# PrintTree(GetNavigatorTree(API_LayoutMap))  # Функция GetNavigatorTree получает элементы навигатора
# из указанной карты (API_LayoutMap) в виде словаря
# TreeSearch(GetNavigatorTree(API_LayoutMap), ("Фасады", "Основные Макеты"))
