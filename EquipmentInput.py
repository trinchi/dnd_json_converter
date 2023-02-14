from __future__ import annotations


class EquipmentInput:
    index: str
    name: str
    amount: int

    def __init__(self):
        self.index = ""
        self.name = ""
        self.amount = 1

    @classmethod
    def from_input_list(cls, equipment_input_list: list) -> list[EquipmentInput]:
        input_list = []
        for equipment_input in equipment_input_list:
            equipment_input_obj = EquipmentInput()

            if 'index' in equipment_input:
                equipment_input_obj.index = equipment_input['index']

            if 'name' in equipment_input:
                equipment_input_obj.name = equipment_input['name']

            if 'amount' in equipment_input and isinstance(equipment_input['amount'], int):
                equipment_input_obj.amount = equipment_input['amount']

            input_list.append(equipment_input_obj)

        return input_list
