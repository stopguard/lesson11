r"""
Реализовать класс «Дата», функция-конструктор которого должна принимать дату в виде строки формата «день-месяц-год».
    В рамках класса реализовать два метода.
        Первый — с декоратором @classmethod.
            Он должен извлекать число, месяц, год и преобразовывать их тип к типу «Число».
        Второй — с декоратором @staticmethod,
            должен проводить валидацию числа, месяца и года (например, месяц — от 1 до 12).
"""


class DateValidationError(Exception):
    """Ошибка корректности даты"""
    def __init__(self, value):
        self.txt = f'DateValidationError: [{value}] не является корректной датой'


class MyDate:
    """Самодельный формат даты"""
    splitters = {'/', ',', '.', '-', ' '}     # разрешённые разделители

    def __init__(self, date_string: str):
        """Конструктор даты, преобразовывает строку в самодельный формат даты"""
        raw_date = self.str_conv(date_string)           # преобразование строки в кортеж чисел - сырую даты
        valide_date = self.date_validation(raw_date)    # валидация сырой даты
        if valide_date:                                 # если сырая дата валидна
            self.date = {'day': raw_date[0], 'month': raw_date[1], 'year': raw_date[2]}     # получаем из нее атрибут
        else:
            raise DateValidationError(date_string)      # иначе выводим ошибку

    def __str__(self):
        """Перегрузка строки приведением формата даты"""
        return f'{self.date["day"]:02}.{self.date["month"]:02}.{self.date["year"]:02}г.'

    @classmethod
    def str_conv(cls, date_string: str):
        """Разбивает строку по валидным разделителям и преобразовывает подстроки в числа"""
        date_list = []                          # заготовка сырой даты
        for spl in cls.splitters:               # ищем разделитель и бьём строку на список по нему
            if spl in date_string:
                date_list = date_string.split(spl)
                break
        if not date_list:                       # если разделитель не был найден выводим ошибку
            raise DateValidationError(date_string)
        for i, number in enumerate(date_list):  # проходим по списку
            if number.isdigit():                    # если элемент цифровой, преобразовываем в число
                date_list[i] = int(date_list[i])
            else:                                   # иначе выводим ошибку
                raise DateValidationError(date_string)
        return tuple(date_list)                 # возвращаем сырую дату

    @staticmethod
    def date_validation(r_date: tuple):
        """Валидация сырой даты перед преобразованием"""
        febr_days = 28 if r_date[2] % 4 else 29     # получение последнего дня февраля
        # список количеств дней в месяцах
        days_dict = {1: 31, 2: febr_days, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        if len(r_date) == 3 and 0 < r_date[0] <= days_dict.get(r_date[1], 0):   # если день и месяц валидны
            return True                                                             # возвращаем истину
        return False                                                            # иначе ложь


# ИСПОЛНЯЕМАЯ ЧАСТЬ
while True:     # вводим дату пока не лопнем... или не отправим пустую строку
    date_str = input("Введите дату в формате дд мм гггг\n"
                     f"Возможные разделители: {MyDate.splitters}\n"
                     "Для завершения ничего не вводите, нажмите [Enter]\n>>> ")
    if not date_str:    # перехват команды на выход из программы
        print('\nЗавершение работы.')
        break
    try:                # перехват ошибки ввода даты
        date_date = MyDate(date_str)
    except DateValidationError as err:
        print(f'\n{err.txt}\n')
    else:
        print(f'\nДата получена успешно: {date_date}\n')
