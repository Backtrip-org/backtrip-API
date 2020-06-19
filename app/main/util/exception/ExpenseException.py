class ExpenseNotFoundException(Exception):
    def __init__(self, expense_id):
        self.value = "Expense with id {} not found.".format(expense_id)

    def __str__(self):
        return repr(self.value)