import re

class binary_string:
    def __init__(self, value, length):
        if type(value) == type(1):
            bin_val = bin(value)[2:]
            if len(bin_val) > length:
                self.value = bin_val[-length:]
            else:
                self.value = '0'*(length - len(bin_val)) + bin_val
        else:
            if re.search("[0,1]{{{}}}".format(len(value)), value):
                self.value = '0'*(length - len(value)) + value
            else:
                raise ValueError("Wrong binary string!")

class extended_binary_mask:
    def __init__(self, string):
        if re.search("[0,1,*]{{{}}}".format(len(string)), string):
            self.value = string
        else:
            raise ValueError("Wrong extended binary mask!")

def operation_for_delta(binary_string_el, extended_binary_mask_el):
    if len(binary_string_el.value) == len(extended_binary_mask_el.value) and type(binary_string_el) == type(binary_string(1, 1)) and type(extended_binary_mask_el) == type(extended_binary_mask('1')):
        res = ''
        for i in range(len(binary_string_el.value)):
            if extended_binary_mask_el.value[i] == '*':
                res += '*'
            elif binary_string_el.value[i] == extended_binary_mask_el.value[i]:
                res += binary_string_el.value[i]
            else:
                res += binary_string_el.value[i]
        return extended_binary_mask(res)     
    else:
        raise ValueError("Binary string length and extended binary mask length are not equal!")

def create_delta_set(extended_binary_mask_el):
    n = len(extended_binary_mask_el.value)
    V_n = list(range(2 ** n))
    result = []
    for el in V_n[1:]:
        if operation_for_delta(binary_string(el, n), extended_binary_mask_el).value == extended_binary_mask_el.value:
            result.append(el)
    return result
