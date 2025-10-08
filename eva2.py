from DataStructures.List import array_list as lt # Importo mi implementación de lista para guardar la información

# Problema 1 eva2 de prueba

def best_par(list, target):
    if lt.size(list) < 2:
        return None
    lt.shell_sort(list, lt.default_sort_criteria)
    left = 0
    right = lt.size(list)-1

    best_pair = (lt.get_element(list, left), lt.get_element(list, right))
    best_diff = float("inf")

    while left < right: # Ojo mejor usar < y no <=
        s = lt.get_element(list, left)+lt.get_element(list, right)
        diff = abs(target-s) # El orden de esto no importa
        if diff < best_diff:
            best_pair = (lt.get_element(list, left), lt.get_element(list, right))
            best_diff  = diff
        if diff == 0:
            return best_pair
        if s > target:
            right -=1
        if s < target:
            left +=1
    return best_pair

# [1,2,3,4], busco el 8
# Entonces si 1+4 = 5 < 8, es decir tengo que aumentar, luego para aumentar me muevo a la derecha

list1 = lt.new_list()

lt.add_last(list1, 1)
lt.add_last(list1, 4)
lt.add_last(list1, 3)
lt.add_last(list1, 2)

list2 = lt.new_list()

list3 = lt.new_list()
lt.add_last(list3, 1)

list4 = lt.new_list()
lt.add_last(list4, -2)
lt.add_last(list4, 7)

list5 = lt.new_list()

lt.add_last(list5, 1)
lt.add_last(list5, 9)
lt.add_last(list5, -3)
lt.add_last(list5, 10)


list6 = lt.new_list()

lt.add_last(list6, 2)
lt.add_last(list6, 5)
lt.add_last(list6, 11)
lt.add_last(list6, -2)
lt.add_last(list6, 7)

list7 = lt.new_list()

lt.add_last(list7, 1)
lt.add_last(list7, 4)
lt.add_last(list7, 6)
lt.add_last(list7, 8)

print(best_par(list1, 6))
print(best_par(list2, 6))
print(best_par(list3, 6))
print(best_par(list4, 4))
print(best_par(list5, 6))
print(best_par(list6, 9))
print(best_par(list7, 11))
