class GDPR:
    user = object
    trips = list()
    steps = list()
    messages = list()
    expenses = list()
    reimbursements = list()

    def __init__(self, user, trips, steps, messages, expenses, reimbursements):
        self.user = user
        self.trips = trips
        self.steps = steps
        self.messages = messages
        self.expenses = expenses
        self.reimbursements = reimbursements

