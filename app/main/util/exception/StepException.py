class StepNotFoundException(Exception):
    def __init__(self, step_id):
        self.value = "Step with id {} does not exist.".format(step_id)

    def __str__(self):
        return repr(self.value)
