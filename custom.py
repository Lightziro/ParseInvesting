# -----------------------------
# Class with custom methods
# (С) 2020 Russia, Kirov - Light3iro
# -----------------------------
class method:
    # / Function for checking whether an element is found in an array / #
    # / @params string str - The string that is being searched in the array / #
    # / @params array arraySearch - Array in which search for a string # /
    # / @return bool True - If a string is found in the array / #
    def in_array(self, str = str(), arraySearch = []):
        for element in arraySearch:
            if element == str:
                return True

    # / Function for checking whether a variable is an array / #
    # / @params array array - Array that is being checked # /
    # / @return bool - True if the variable is an array, else False / #
    def is_array(self, array = []):
        if type(array) == dict or type(array) == list:
            return True
        else:
            return False

    # / Function for checking an array for emptiness / #
    # / @params array array - Array that is being checked # /
    # / @return bool - True if the array is empty / #
    def emptyArray(self, array):
        return ((array is None) or (len(array)) == 0)

    # / Function for checking a variable, or a list of variables for emptiness / #
    # / @params string variable - Variable to be converted # /
    # / @return bool - True if the variable was converted, otherwise False / #
    def empty(self, variable):
        result = bool(True)
        if len(variable) > 1:
            for variables in variable:
                if variables:
                    result = False
                    break;
        else:
            result = True if (not variable or variable is None) else False
        return result

    # / Function for trying to convert a variable to a int / #
    # / @params string variable - Variable to be converted # /
    # / @return bool - True if the variable was converted, otherwise False / #
    def tryConvertToInt(self, variable = str()):
        try:
            if int(variable):
                return True
        except:
            return False

