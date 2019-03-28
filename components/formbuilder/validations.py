import datetime
import re

class IsNumeric_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Is Not Numeric"

    def is_valid(self):
        try:
            nr = float(self.value)
        except ValueError:
            return False
        return True

class IsPercentage_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Is not a percentage value (0-100)"

    def is_valid(self):
        try:
            nr = float(self.value)
            if nr >= 0 and nr <= 100:
                return True
            else:
                return False
        except ValueError:
            return False
        return True


class NotEmpty_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Cannot be empty"

    def is_valid(self):
        if self.value == "" or self.value is None:
            return False
        else:
            return True


class ValidDate_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Invalid date [Should be in format dd/MM/yyyy]"

    def is_valid(self):
        try:
            dt = datetime.datetime.strptime(self.value, "%d/%m/%Y")
            return True
        except ValueError:
            return False

class IsFutureDate_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Must be a future date"

    def is_valid(self):
        try:
            dt = datetime.datetime.strptime(self.value, "%d/%m/%Y")
            if dt > datetime.datetime.now():
                return True
            return False
        except ValueError:
            return False

class IsPastDate_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Must be a date in the past"

    def is_valid(self):
        try:
            dt = datetime.datetime.strptime(self.value, "%d/%m/%Y")
            if dt < datetime.datetime.now():
                return True
            return False
        except ValueError:
            return False

class IsEmail_Validation(object):
    def __init__(self, value):
        self.value = value
        self.message = "Not a valid email"


    def is_valid(self):
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.value)

        if match == None:
            return False
        return True
