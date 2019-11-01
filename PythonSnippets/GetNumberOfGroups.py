groupGuidSet = set()  # Создаем набор

# Получаем список всех элементов, которые являются "связанными/фиктивными"
for elemGuid in GetElementList(API_ZombieElemID):  # Проходимся по этим элементам
    # elemHead = GetElementHeader(elemGuid)
    # elemTypeName = GetElementTypeName(elemHead.typeID)
    # print(elemHead.typeID, elemTypeName, "=", elemHead.layer)
    groupGuid = GetGroupOfElement(elemGuid)
    # print(groupGuid)
    if groupGuid != APINULLGuid:
        groupGuidSet.add(groupGuid)

print("Number of Groups: %d" % len(groupGuidSet))
