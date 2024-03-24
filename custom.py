# -----------------------------
# Class with custom methods
# (С) 2020 Russia, Kirov - Light3iro
# -----------------------------
import re
class method:

    @staticmethod
    def in_array(str = str(), arraySearch = []):
        """
        Function for checking whether an element is found in an array
        :param str: The string that is being searched in the array
        :param arraySearch: Array in which search for a string
        :return: True if a string is found in the array
        """
        for element in arraySearch:
            if element == str:
                return True

    @staticmethod
    def is_array(array = []):
        """
        Function for checking whether a variable is an array
        :param array: Array that is being checked
        :return: True if the variable is an array, else False
        """
        if type(array) == dict or type(array) == list:
            return True
        else:
            return False

    @staticmethod
    def emptyArray(array = []):
        """
        Function for checking an array for emptiness
        :param array: Array that is being checked
        :return: True if the array is empty
        """
        return ((array is None) or (len(array)) == 0)


    @staticmethod
    def empty(variable):
        """
        Function for checking a variable, or a list of variables for emptiness
        :param variable: Variable that will be checked for emptiness
        :return: True If the variable is empty, otherwise False
        """
        result = bool(True)
        if len(variable) > 1:
            for variables in variable:
                if variables:
                    result = False
                    break;
        else:
            result = True if (not variable or variable is None) else False
        return result

    @staticmethod
    def tryConvertToInt(variable = str()):
        """
        Function for trying to convert a variable to a int
        :param variable: Variable to be converted
        :return: True if the variable was converted, otherwise False
        """
        try:
            if int(variable):
                return True
        except:
            return False

    @staticmethod
    def getTextByCount(count = int(), arText = []):

        nums = [2, 0, 1, 1, 1, 2]
        return arText[ 2 if count % 100 > 4 and count % 100 < 20 else nums[min(count % 10, 5)]]

    @staticmethod
    def convertToFloat(number = str()):
        try:
            number = re.sub(r'%|\+|\.|\(|\)', '', number).replace(',', '.')
            return float(number)
        except:
            return False

# -----------------------------
# Class for executing queries
# (С) 2020 Russia, Kirov - Light3iro
# -----------------------------
class Request:

    import requests

    HEADERS = dict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    })

    @classmethod
    def getResponse(cls, url = str()):
        """
        Function for sending a get request to a site
        :param url: Link to send the request
        :return: Object of the executed request
        """
        response = cls.requests.get(url, headers=cls.HEADERS)
        if response:
            return response