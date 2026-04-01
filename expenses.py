##Instead of just using dictionaries, using a Class allows you to bake validation directly into the data object.


import datetime

class Expense:
    def __init__(self, date, amount, category, description):
        self.date = self._validate_date(date)
        self.amount = self._validate_amount(amount)
        self.category = category
        self.description = description

    def _validate_date(self, date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return datetime.date.today().isoformat()

    def _validate_amount(self, amount):
        try:
            val = float(amount)
            return val if val > 0 else 0.0
        except ValueError:
            return 0.0

    def to_dict(self):
        return self.__dict__
