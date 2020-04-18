from xml.etree import ElementTree as et


def get_dict_from_xml(file_name, find_items):
    """
    Поиск всех элементов по имени тега. Возвращает словарь, у которого ключи представляют id элемента,
    а значениями словари с названиями тегов и значениями тегов дочерних элементов.
    """
    elements = et.parse(file_name).findall(find_items)
    return {i.get('id'): {i[j].tag: i[j].text for j in range(len(i))} for i in elements}


def get_elem(key, value, elements):
    """Возвращает искомый элемент."""
    if key == 'id':
        return elements[value]
    else:
        elem = None
        for i in elements.values():
            if i[key] == value:
                elem = i
                break
        if elem:
            return elem


def about_elem(elem, verbose_names):
    """Возвращает строку с информацией об элементе"""
    return ''.join(f'{verbose_names[i[0]]}: {i[1].strip()}\n' for i in elem.items()).strip()


def count_elements(key, value, elements):
    """Возвращает количество элементов по тегу и значению"""
    k = 0
    for i in elements.values():
        if i[key] == value:
            k += 1
    return k


def average_values(key, average_key, elements):
    """Возвращает словарь с ключами по которым определяется среднее значение, значениями которых является среднее"""
    dict_averages = {}
    for i in elements.values():
        j = i[key]
        if j not in dict_averages:
            dict_averages[j] = {'count': count_elements(key, j, elements), 'sum': float(i[average_key])}
        else:
            dict_averages[j]['sum'] += float(i[average_key])
    return {i[0].strip(): i[1]['sum'] / i[1]['count'] for i in dict_averages.items()}


def check_kwargs(elem, check_keys):
    """Проверка на совпадение ключей в элементах"""
    result = True
    for i in check_keys.items():
        if elem[i[0]].strip() != i[1].strip():
            result = False
            break
    return result


def max_element(elements, max_key, **kwargs):
    """Возвращает максимальный элемент"""
    return max((i for i in elements.values() if check_kwargs(i, kwargs)), key=lambda x: float(x.get(max_key)))


def main():
    books = get_dict_from_xml('books.xml', 'Book')
    verbose_names = {'EAN': 'Штрих-код',
                     'ISBN': 'Номер книги',
                     'Author': 'Автор',
                     'Title': 'Название',
                     'Publisher': 'Издатель',
                     'Printing': 'Тираж',
                     'Year_of_publishing': 'Год выпуска',
                     'Format': 'Формат',
                     'Price': 'Цена'
                     }

    def by_id():
        id_book = input('Введите id книги: ')
        try:
            print('\nИнформация о книге: ', about_elem(get_elem('id', id_book, books), verbose_names), sep='\n')
        except Exception:
            print('\nКнига не найдена')

    def by_isbn():
        isbn = input('Введите ISBN книги: ')
        try:
            print('\nИнформация о книге: ', about_elem(get_elem('ISBN', isbn, books), verbose_names), sep='\n')
        except Exception:
            print('\nКнига не найдена')

    def count_book():
        year = input('Введите год издания книг: ')
        print(f'\nКоличество книг с годом издания {year}: ', count_elements('Year_of_publishing', year, books))

    def average_publisher():
        print(''.join(f'{i[0]}: {i[1]:.2f}\n' for i in average_values('Publisher', 'Price', books).items()))

    def most_exp():
        publisher = input('Введите издателя: ')
        year = input('Введите год издания: ')
        try:
            print(f'\nСамая дорогая книга издателя {publisher} за {year} год:',
                  about_elem(max_element(books, 'Price', Publisher=publisher, Year_of_publishing=year), verbose_names),
                  sep='\n'
                  )
        except Exception:
            print('Книга не найдена')

    cmd = [by_id, by_isbn, count_book, average_publisher, most_exp, exit]
    menu = """
Выберите действие:
Поиск книги по id – 0
Поиск книги по isbn – 1
Посчитать количествол книг за год издания – 2
Вывести среднюю стоимость книг по издателям – 3
Вывести самую дорогую книгу издателя за год издания – 4
Выйти – 5

    """
    while True:
        try:
            request_user = int(input(menu))
            cmd[request_user]()
        except Exception:
            continue


if __name__ == '__main__':
    main()
