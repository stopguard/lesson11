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


class TargetValidationError(Exception):
    def __init__(self, target):
        self.txt = f'[{target}] не существует среди точек назначения'


class OfficeEquipment:
    model_dict = {'1': {'model': '-'}}

    def __init__(self, model):
        self.model = type(self).model_dict.get(model, None)['model']
        if not self.model:
            raise ModelValidationError(type(self), model)
        self.values = ()

    def __str__(self):
        return str(*[f'{param}: {val}; ' for param, val in self.values])


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
                  '2': {'model': 'Canon', 'form': 'PC', 'OS': 'Windows 10'}}

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


class Desk(Furniture):
    model_dict = {'1': {'model': 'Экспро', 'material': 'Chipboard', 'type': 'computer'},
                  '2': {'model': 'Росвега', 'material': 'wooden', 'type': 'desktop'}}


class Chair(Furniture):
    model_dict = {'1': {'model': 'Постформика', 'material': 'skin', 'type': 'armchair'},
                  '2': {'model': 'Индстайл', 'material': 'metal', 'type': 'office'}}


class Storage:
    eq_types = {'1': Printers, '2': MFU, '3': PC}
    furnitures = {'1': Desk, '2': Chair}
    targets = {}
    services = {}

    def __init__(self, name):
        self.office_eq_list = []
        self.furnitures = []
        self.damaged = []
        self.crushed = []
        self.name = name
        if type(self) == Storage:
            Unit.targets[str(len(Unit.targets) + 1)] = [name, self]
            ServiceCenter.targets[str(len(ServiceCenter.targets) + 1)] = [name, self]

    def get_office_eq(self, model, eq_type, quantity=1):
        if not (eq_type in self.eq_types):
            raise ModelValidationError('оргтехника', eq_type)
        for number in range(quantity):
            self.office_eq_list.append(type(self).eq_types[eq_type](model))

    def get_furniture(self, model, furniture, quantity=1):
        if not (furniture in self.furnitures):
            raise ModelValidationError('мебель', furniture)
        for number in range(quantity):
            self.office_eq_list.append(type(self).furnitures[furniture](model))

    def move_office_eq(self, target, model, eq_type, quantity=1):
        if not (eq_type in self.eq_types):
            raise ModelValidationError('оргтехника', eq_type)
        if not (target in self.targets):
            raise TargetValidationError(target)
        x = 0
        for number in range(quantity):
            for eq in self.office_eq_list[:]:
                if eq.model == self.eq_types[eq_type].model_dict[model]:
                    self.targets[target][1].office_eq_list.add(eq)
                    self.office_eq_list.remove(eq)
                    x += 1
                    break
        if x < quantity:
            print(f'Перемещено: {x} из {quantity}.\n'
                  f'На складе недостаток позиции [{self.eq_types[eq_type].model_dict[model]}]')
        else:
            print(f'Успешно перемещена позиция [{self.eq_types[eq_type].model_dict[model]}] '
                  f'в количестве {quantity} в подразделение {self.targets[target][0]}')

    def move_furniture(self, target, model, furniture, quantity=1):
        if not (furniture in self.furnitures):
            raise ModelValidationError('мебель', furniture)
        if not (target in self.targets):
            raise TargetValidationError(target)
        x = 0
        for number in range(quantity):
            for furn in self.furnitures[:]:
                if furn.model == self.furnitures[furniture].model_dict[model]:
                    self.targets[target][1].furnitures.add(furn)
                    self.furnitures.remove(furn)
                    x += 1
                    break
        if x < quantity:
            print(f'Перемещено: {x} из {quantity}.\n'
                  f'На складе недостаток позиции [{self.furnitures[furniture].model_dict[model]}]')
        else:
            print(f'Успешно перемещена позиция [{self.furnitures[furniture].model_dict[model]}] '
                  f'в количестве {quantity} в подразделение {self.targets[target][0]}')

    def repair(self):
        for eq in self.damaged[:]:
            if eq.__class__.__bases__ == OfficeEquipment:
                Storage.services['1'].office_eq_list.append(eq)
                self.damaged.remove(eq)
            else:
                Storage.services['1'].furnitures.append(eq)
                self.damaged.remove(eq)
            print(f'Позиция [{eq.__class__.__bases__}: {eq.model}] отправлена на ремонт.')

    def utilize(self):
        for i, eq in enumerate(self.crushed[::-1]):
            print(f'Позиция [{eq.__class__.__bases__}: {self.crushed.pop(i).model}] отправлена на ремонт.')
            del eq


class Unit(Storage):
    eq_types = {'1': Printers, '2': MFU, '3': PC}
    furnitures = {'1': Desk, '2': Chair}
    targets = {}
    services = {}

    def __init__(self, name):
        super().__init__(name)
        self.office_eq_list = []
        self.furnitures = []
        self.damaged = []
        self.crushed = []
        Storage.targets[str(len(Storage.targets) + 1)] = [name, self]

    def return_damaged(self):
        self.targets['1'].damaged += self.damaged
        self.damaged = []
        self.targets['1'].crushed += self.crushed
        self.crushed = []


class ServiceCenter(Storage):
    eq_types = {'1': Printers, '2': MFU, '3': PC}
    furnitures = {'1': Desk, '2': Chair}
    targets = {}
    services = {}

    def __init__(self, name):
        super().__init__(name)
        self.office_eq_list = []
        self.furnitures = []
        Storage.services[str(len(Storage.services) + 1)] = [name, self]

    def return_(self):
        self.targets['1'].office_eq_list += self.office_eq_list
        self.office_eq_list = []
        self.targets['1'].furnitures += self.furnitures
        self.furnitures = []


def crush_item():
    for unit in Storage.targets:
        for i in range(len(unit[1].office_eq_list) - 1, -1, -1):
            rand = randint(0, 100)
            if rand < 10:
                unit[1].damaged.append(unit[1].office_eq_list.pop(i))
            elif rand < 20:
                unit[1].crushed.append(unit[1].office_eq_list.pop(i))


office = Unit('Офис')
engeneers = Unit('Монтажный отдел')
storage = Storage('Склад')
service = ServiceCenter('Сервис-центр')
print('Склад', Storage.targets)
print('Склад', Storage.services)
print('Юнит', Unit.targets)
print('Юнит', Unit.services)
print('Сервис', ServiceCenter.targets)
print('Сервис', ServiceCenter.services)
