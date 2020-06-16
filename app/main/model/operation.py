from .. import db


class Operation:
    emitter_id = 0
    payee_id = 0
    amount = 0.0

    def __init__(self, emitter_id, payee_id, amount):
        self.emitter_id = emitter_id
        self.payee_id = payee_id
        self.amount = amount
