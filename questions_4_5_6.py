"""
Начать работу над проектом «Склад оргтехники».
    Создать класс, описывающий склад. А также класс «Оргтехника», который будет базовым для классов-наследников.
    Эти классы — конкретные типы оргтехники (принтер, сканер, ксерокс).
    В базовом классе определить параметры, общие для приведённых типов.
    В классах-наследниках реализовать параметры, уникальные для каждого типа оргтехники.
Разработать методы, которые отвечают за приём оргтехники на склад и передачу в определённое подразделение компании.
    Для хранения данных о наименовании и количестве единиц оргтехники, а также других данных,
    можно использовать любую подходящую структуру (например, словарь).
Реализовать механизм валидации вводимых пользователем данных.
    Например, для указания количества принтеров, отправленных на склад, нельзя использовать строковый тип данных.
"""
from random import randint


class ModelValidationError(Exception):
    def __init__(self, cls, model):
        self.txt = f'Среди предметов [{cls}] не существует модели [{model}]'

    def __str__(self):
        return self.txt


class TargetValidationError(Exception):
    def __init__(self, target):
        self.txt = f'[{target}] не существует среди точек назначения'

    def __str__(self):
        return self.txt


class OfficeEquipment:
    model_dict = {'1': {'model': '-'}}

    def __init__(self, model):
        self.model = type(self).model_dict.get(model, None)['model']
        if not self.model:
            raise ModelValidationError(type(self), model)
        self.values = ()

    def __str__(self):
        return str(*[f'{param}: {val}; ' for param, val in self.values])

    @classmethod
    def model_str(cls):
        return '\n'.join([f'{key}: {model["model"]}' for key, model in cls.model_dict.items()])


class Printers(OfficeEquipment):
    model_dict = {'1': {'model': 'HP', 'print_type': 'laser', 'colors': 'monochrome', 'format': 'A3'},
                  '2': {'model': 'Canon', 'print_type': 'inkjet', 'colors': 'color', 'format': 'A4'}}

    def __init__(self, model):
        super().__init__(model)
        self.print_type = type(self).model_dict.get(model, None)['print_type']
        self.colors = type(self).model_dict.get(model, None)['colors']
        self.format = type(self).model_dict.get(model, None)['format']
        self.values = (self.model, self.print_type, self.colors, self.format)


class MFU(OfficeEquipment):
    model_dict = {
        '1': {'model': 'Kyocera', 'print_type': 'laser', 'colors': 'monochrome', 'format': 'A4', 'res': 800},
        '2': {'model': 'Epson', 'print_type': 'laser', 'colors': 'color', 'format': 'A3', 'res': 1200}}

    def __init__(self, model):
        super().__init__(model)
        self.print_type = type(self).model_dict.get(model, None)['print_type']
        self.colors = type(self).model_dict.get(model, None)['colors']
        self.format = type(self).model_dict.get(model, None)['format']
        self.resolution = type(self).model_dict.get(model, None)['res']
        self.values = (self.model, self.print_type, self.colors, self.format, self.resolution)


class PC(OfficeEquipment):
    model_dict = {'1': {'model': 'Lenovo', 'form': 'notebook', 'OS': 'Windows 8.1'},
                  '2': {'model': 'Dell', 'form': 'PC', 'OS': 'Windows 10'}}

    def __init__(self, model):
        super().__init__(model)
        self.form = type(self).model_dict.get(model, None)['form']
        self.OS = type(self).model_dict.get(model, None)['OS']
        self.values = (self.model, self.form, self.OS)


class Furniture:
    model_dict = {'1': {'model': '-', 'material': '-', 'type': '-'}}

    def __init__(self, model):
        self.model = type(self).model_dict.get(model, None)['model']
        if not self.model:
            raise ModelValidationError(type(self), model)
        self.material = type(self).model_dict.get(model, None)['material']
        self.type_ = type(self).model_dict.get(model, None)['type']
        self.values = (self.model, self.material, self.type_)

    def __str__(self):
        return str(*[f'{param}: {val}; ' for param, val in self.values])

    @classmethod
    def model_str(cls):
        return '\n'.join([f'{key}: {model["model"]}' for key, model in cls.model_dict.items()])


class Desk(Furniture):
    model_dict = {'1': {'model': 'Экспро', 'material': 'Chipboard', 'type': 'computer'},
                  '2': {'model': 'Росвега', 'material': 'wooden', 'type': 'desktop'}}


class Chair(Furniture):
    model_dict = {'1': {'model': 'Постформика', 'material': 'skin', 'type': 'armchair'},
                  '2': {'model': 'Индстайл', 'material': 'metal', 'type': 'office'}}


class Storage:
    eq_types = {'1': Printers, '2': MFU, '3': PC}
    furn_types = {'1': Desk, '2': Chair}
    targets = {}
    services = {}
    all_obj = {}

    def __init__(self, name):
        self.office_eq_list = []
        self.furnitures = []
        self.damaged = []
        self.crushed = []
        self.name = name
        Storage.all_obj[str(len(Storage.all_obj) + 1)] = [name, self]
        if type(self) == Storage:
            Unit.targets[str(len(Unit.targets) + 1)] = [name, self]
            ServiceCenter.targets[str(len(ServiceCenter.targets) + 1)] = [name, self]

    def __str__(self):
        self_dict = {}
        result = f'Содержимое объекта [{self.name}]:\n'
        for item in self.office_eq_list:
            self_dict.setdefault('Оргтехника', {})
            self_dict['Оргтехника'][f'{item.__class__.__name__} {item.model}'] = \
                self_dict['Оргтехника'].setdefault(f'{item.__class__.__name__} {item.model}', 0) + 1
        for item in self.furnitures:
            self_dict.setdefault('Мебель', {})
            self_dict['Мебель'][f'{item.__class__.__name__} {item.model}'] = \
                self_dict['Мебель'].setdefault(f'{item.__class__.__name__} {item.model}', 0) + 1
        for item in self.damaged:
            self_dict.setdefault('Ремонтопригодное', {})
            self_dict['Ремонтопригодное'][f'{item.__class__.__name__} {item.model}'] = \
                self_dict['Ремонтопригодное'].setdefault(f'{item.__class__.__name__} {item.model}', 0) + 1
        for item in self.crushed:
            self_dict.setdefault('Невосстановимое', {})
            self_dict['Невосстановимое'][f'{item.__class__.__name__} {item.model}'] = \
                self_dict['Невосстановимое'].setdefault(f'{item.__class__.__name__} {item.model}', 0) + 1
        for key1, items in self_dict.items():
            result += f'\n{key1}'
            for key2 in sorted(self_dict[key1]):
                result += f'\n{key2:.<20}: {self_dict[key1][key2]}'
        return result

    @staticmethod
    def view_obj():
        target_list = '\n'.join([f'{key}: {trgt[0]}' for key, trgt in Storage.all_obj.items()])
        target = input(f'Просмотр содержимого.\n'
                       f'Выберите объект:\n'
                       f'{target_list}\n'
                       f'>>> ')
        if not (target in Storage.all_obj):
            raise TargetValidationError(target)
        print(Storage.all_obj[target][1])

    def get_office_eq(self):
        types_list = '\n'.join([f'{key}: {eq.__name__}' for key, eq in self.eq_types.items()])
        eq_type = input(f'Закуп: [Оргтехника]\n'
                        f'Выберите тип:\n'
                        f'{types_list}\n'
                        f'>>> ')
        if not (eq_type in self.eq_types):
            raise ModelValidationError('оргтехника', eq_type)
        model = input(f'Закуп: [Оргтехника] > [{type(self).eq_types[eq_type].__name__}]\n'
                      f'Выберите модель:\n'
                      f'{type(self).eq_types[eq_type].model_str()}\n'
                      f'>>> ')
        quantity = input('Введите количество:\n>>> ')
        for number in range(int(quantity)):
            self.office_eq_list.append(type(self).eq_types[eq_type](model))
        print(self)

    def get_furniture(self):
        types_list = '\n'.join([f'{key}: {furn.__name__}' for key, furn in self.furn_types.items()])
        furniture = input(f'Закуп: [Мебель]\n'
                          f'Выберите тип:\n'
                          f'{types_list}\n'
                          f'>>> ')
        if not (furniture in self.furn_types):
            raise ModelValidationError('мебель', furniture)
        model = input(f'Закуп: [Мебель] > [{type(self).furn_types[furniture].__name__}]\n'
                      f'Выберите модель:\n'
                      f'{type(self).furn_types[furniture].model_str()}\n'
                      f'>>> ')
        quantity = input('Введите количество:\n>>> ')
        for number in range(int(quantity)):
            self.furnitures.append(type(self).furn_types[furniture](model))
        print(self)

    def move_office_eq(self):
        types_list = '\n'.join([f'{key}: {eq.__name__}' for key, eq in self.eq_types.items()])
        target_list = '\n'.join([f'{key}: {trgt[0]}' for key, trgt in self.targets.items()])
        target = input(f'Поставка: [Оргтехника].\n'
                       f'Выберите адресата:\n'
                       f'{target_list}\n'
                       f'>>> ')
        if not (target in self.targets):
            raise TargetValidationError(target)
        eq_type = input(f'Поставка для [{self.targets[target][0]}]: [Оргтехника]\n'
                        f'Выберите тип:\n'
                        f'{types_list}\n'
                        f'>>> ')
        if not (eq_type in self.eq_types):
            raise ModelValidationError('оргтехника', eq_type)
        model = input(f'Поставка для [{self.targets[target][0]}]: [Оргтехника] > '
                      f'[{type(self).eq_types[eq_type].__name__}]\n'
                      f'Выберите модель:\n'
                      f'{type(self).eq_types[eq_type].model_str()}\n'
                      f'>>> ')
        quantity = int(input('Введите количество:\n>>> '))
        x = 0
        for number in range(quantity):
            for eq in self.office_eq_list[:]:
                print(eq.model)
                if eq.model == self.eq_types[eq_type].model_dict[model]["model"]:
                    self.targets[target][1].office_eq_list.append(eq)
                    self.office_eq_list.remove(eq)
                    x += 1
                    break
        if x < quantity:
            print(f'Перемещено: {x} из {quantity}.\n'
                  f'На складе недостаток позиции [{self.eq_types[eq_type].model_dict[model]["model"]}]')
        else:
            print(f'Успешно перемещена позиция [{self.eq_types[eq_type].model_dict[model]["model"]}] '
                  f'в количестве {quantity} в подразделение {self.targets[target][0]}')
        print(self)

    def move_furniture(self):
        types_list = '\n'.join([f'{key}: {furn.__name__}' for key, furn in self.furn_types.items()])
        target_list = '\n'.join([f'{key}: {trgt[0]}' for key, trgt in self.targets.items()])
        target = input(f'Поставка: [Мебель].\n'
                       f'Выберите адресата:\n'
                       f'{target_list}\n'
                       f'>>> ')
        if not (target in self.targets):
            raise TargetValidationError(target)
        furniture = input(f'Поставка для [{self.targets[target][0]}]: [Мебель]\n'
                          f'Выберите тип:\n'
                          f'{types_list}\n'
                          f'>>> ')
        if not (furniture in self.furn_types):
            raise ModelValidationError('мебель', furniture)
        model = input(f'Поставка для [{self.targets[target][0]}]: [Мебель] > '
                      f'[{type(self).furn_types[furniture].__name__}]\n'
                      f'Выберите модель:\n'
                      f'{type(self).furn_types[furniture].model_str()}\n'
                      f'>>> ')
        quantity = int(input('Введите количество:\n>>> '))
        x = 0
        for number in range(quantity):
            for furn in self.furnitures[:]:
                if furn.model == self.furn_types[furniture].model_dict[model]["model"]:
                    self.targets[target][1].furnitures.append(furn)
                    self.furnitures.remove(furn)
                    x += 1
                    break
        if x < quantity:
            print(f'Перемещено: {x} из {quantity}.\n'
                  f'На складе недостаток позиции [{self.furn_types[furniture].model_dict[model]["model"]}]')
        else:
            print(f'Успешно перемещена позиция [{self.furn_types[furniture].model_dict[model]["model"]}] '
                  f'в количестве {quantity} в подразделение {self.targets[target][0]}')
        print(self)

    def repair(self):
        for eq in self.damaged[:]:
            if eq.__class__.__base__ == OfficeEquipment:
                Storage.services['1'][1].office_eq_list.append(eq)
                self.damaged.remove(eq)
            else:
                Storage.services['1'].furnitures.append(eq)
                self.damaged.remove(eq)
            print(f'Позиция [{eq.__class__.__base__.__name__}: {eq.model}] отправлена на ремонт.')
        print(self)

    def utilize(self):
        for i, eq in enumerate(self.crushed[::-1]):
            print(f'Позиция [{eq.__class__.__base__.__name__}: {self.crushed.pop(i).model}] списана.')
            del eq
        print(self)

    @classmethod
    def eq_str(cls):
        return '\n'.join([f'{key}: {type_.__name__}' for key, type_ in cls.eq_types.items()])

    @classmethod
    def furn_str(cls):
        return '\n'.join([f'{key}: {type_.__name__}' for key, type_ in cls.furn_types.items()])


class Unit(Storage):
    eq_types = {'1': Printers, '2': MFU, '3': PC}
    furn_types = {'1': Desk, '2': Chair}
    targets = {}
    services = {}

    def __init__(self, name):
        super().__init__(name)
        self.office_eq_list = []
        self.furnitures = []
        self.damaged = []
        self.crushed = []
        Storage.targets[str(len(Storage.targets) + 1)] = [name, self]

    @staticmethod
    def return_damaged():
        export_list = '\n'.join([f'{key}: {trgt[0]}' for key, trgt in Storage.targets.items()])
        exporter = input(f'Возврат повреждённого имущества на склад\n'
                         f'Выберите подразделение из которого требуется возврат на склад:\n'
                         f'{export_list}\n'
                         f'>>> ')
        if not (exporter in Storage.targets):
            raise TargetValidationError(exporter)
        Unit.targets['1'][1].damaged += Storage.targets[exporter][1].damaged
        Storage.targets[exporter][1].damaged = []
        Unit.targets['1'][1].crushed += Storage.targets[exporter][1].crushed
        Storage.targets[exporter][1].crushed = []
        print(Storage.targets[exporter][1])


class ServiceCenter(Storage):
    eq_types = {'1': Printers, '2': MFU, '3': PC}
    furn_types = {'1': Desk, '2': Chair}
    targets = {}
    services = {}

    def __init__(self, name):
        super().__init__(name)
        self.office_eq_list = []
        self.furnitures = []
        self.damaged = []
        self.crushed = []
        Storage.services[str(len(Storage.services) + 1)] = [name, self]

    def return_items(self):
        Unit.targets['1'][1].office_eq_list += self.office_eq_list
        Unit.targets['1'][1].furnitures += self.furnitures
        self.office_eq_list = []
        self.furnitures = []
        print(self)


def crush_item():
    for _, unit in Storage.targets.items():
        if unit[1].office_eq_list:
            for i in range(len(unit[1].office_eq_list) - 1, -1, -1):
                rand = randint(0, 100)
                if rand < 10:
                    unit[1].damaged.append(unit[1].office_eq_list.pop(i))
                elif rand < 15:
                    unit[1].crushed.append(unit[1].office_eq_list.pop(i))
            if unit[1].furnitures:
                for i in range(len(unit[1].furnitures) - 1, -1, -1):
                    rand = randint(0, 100)
                    if rand < 10:
                        unit[1].damaged.append(unit[1].furnitures.pop(i))
                    elif rand < 15:
                        unit[1].crushed.append(unit[1].furnitures.pop(i))


print('\n' * 30)
office = Unit('Офис')
engeneers = Unit('Монтажный отдел')
storage = Storage('Склад')
service = ServiceCenter('Сервис-центр')
actions_dict = {'1': ['Закупить оргтехнику', Unit.targets['1'][1].get_office_eq],
                '2': ['Закупить мебель', Unit.targets['1'][1].get_furniture],
                '3': ['Поставить оргтехнику в подразделение', Unit.targets['1'][1].move_office_eq],
                '4': ['Поставить мебель в подразделение', Unit.targets['1'][1].move_furniture],
                '5': ['Вернуть повреждённое имущество на склад', Unit.return_damaged],
                '6': ['Отправить повреждённое имущество в ремонт', Unit.targets['1'][1].repair],
                '7': ['Утилизировать не подлежащее восстановлению имущество', Unit.targets['1'][1].utilize],
                '8': ['Забрать имущество из сервиса', Storage.services['1'][1].return_items],
                '9': ['Просмотреть содержимое объекта', Unit.targets['1'][1].view_obj]
                }
actions = '\n' + '\n'.join([f'{key}: {trgt[0]}' for key, trgt in actions_dict.items()]) + '\n>>> '
while True:
    action = input(f'\nВведите номер действия или exit для выхода{actions}')
    if action.lower() == 'exit':
        break
    try:
        actions_dict[action][1]()
        if int(action) < 9:
            crush_item()
    except (ModelValidationError, TargetValidationError) as err:
        print('Неудачный ввод:', err)
    # except (ValueError, KeyError) as err:
    #     print('Неудачный ввод:', err)
