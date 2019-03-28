class YesNo_Output(object):
    def __init__(self, value):
        self.value = value
    def output(self):
        if self.value in ['1', True, 'True']:
            return "Yes"
        if self.value in ['0', False, 'False']:
            return "No"
        return self.value
