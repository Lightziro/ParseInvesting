def in_array(str, arraySearch = []):
    for element in arraySearch:
        if element == str:
            return True

def is_array(array):
    if type(array) == dict or type(array) == list:
        return True
    else:
        return False
def emptyArray(array):
    return ((array is None) or (len(array)) == 0)

def empty(variable):
    result = bool(True)
    if len(variable) > 1:
        for variables in variable:
            if variables:
                result = False
                break;
    else:
        result = True if (not variable or variable is None) else False
    return result
