class DataProcessing:
    def __init__(self):
        pass

    def validate_identification_number(self, text):
        return self.check_iin(text) or self.check_bin(text)

    @staticmethod
    def check_iin(iin):
        """ Метод для проверки валидности ИИН """
        year = int(iin[:2])
        month = int(iin[2:4])
        day = int(iin[4:6])
        if month not in range(1, 13) \
                or (month in [1, 3, 5, 7, 8, 10, 12] and day not in range(1, 32)) \
                or (month in [4, 6, 9, 11] and day not in range(1, 31)) \
                or (year % 4 == 0 and month == 2 and day not in range(1, 30)) \
                or (year % 4 != 0 and month == 2 and day not in range(1, 29)):
            return False
        b1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        b2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
        a = []
        i, k, control = 0, 0, 0
        while i < 12:
            a.append(int(iin[i:i + 1]))
            if i < 11:
                control += a[i] * b1[i]
                control = control % 11
            i += 1
        if control == 10:
            control = 0
            while k < 11:
                control += a[k] * b2[k]
                control = control % 11
                k += 1
        if control != a[11]:
            return False
        else:
            return True

    @staticmethod
    def check_bin(bin_):
        """ Метод для проверки валидности БИН """
        if int(bin_[2:4]) not in range(1, 13) or bin_[4] in ['0', '1', '2', '3'] or bin_[5] not in ['0', '1', '2', '4']:
            return False
        else:
            return True
