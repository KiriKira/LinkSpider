#-*- coding：utf-8 -*-


def cut(address, tup):
    for item in tup:
        if len(address.split(item, 1)) > 1:
            return address.split(item, 1)[0] + item, address.split(item, 1)[1]


def address_split(address):
    try:
        first_class, second = cut(address, ('省', '自治区', '行政区', '市'))
        second_class, third_class = cut(second, ('市', '行政单位', '州'))
        return first_class, second_class, third_class
    except TypeError:
        return address, '', ''
    except Exception as e:
        return address, str(e), ''

