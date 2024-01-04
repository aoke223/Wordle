################################################################################
from contextlib import redirect_stdout
import io
from typing import Callable  # use Callable as a type hint
import inspect
################################################################################

def printTest(function: Callable, *args: tuple, **kwargs: dict) -> None:
    ''' Function to streamline fruitful-function testing, allowing the user to
        pass in a function, arbitrary number of arguments, and an expected result.
        Example usage shown below:
            printTest(computeSum, 11, 22, 33, expected = 66)
            printTest(computeRatio, 1, 2, expected = 0.5)
            printTest(reverseString, "abcde", expected = "edcba")
    Parameters:
        - function: the name of a Callable function (the funtion name -- not a call)
        - (as part of *args): pass zero or more arguments that your function will need when called
        - "expected" (as part of **kwargs): the expected result of the function call
        - [optional (as part of **kwargs)]: 
            - "fruitful":  [default True]  if False, student function is expected to print, not return
            - "simple":    [default False] if True, uses "+" and "X" for correct and incorrect
            - "is_method": [default False] if True, function is expected to be a method within a class
    Returns:
        nothing
    '''
    # grab the frame object associated with the student's calling module, and then import
    # that module (outside of this module) so we can call the function to be tested
    calling_frame = inspect.stack()[-1][0]
    student_module = inspect.getmodule(calling_frame)

    try:    is_method = bool(kwargs["is_method"])
    except: is_method = False

    function_name = function.__name__

    # build the function call string for later evaluating
    function_call_string = f"{function.__name__}("        # looks like "computeSum("
    start_index = 0 if not is_method else 1               # avoid using self as argument
    for i in range(start_index, len(args)):
        function_call_string += f"{repr(args[i])}, "      # append each argument, then ", "
    function_call_string += ")"                           # append the closing paren
    function_call_string = function_call_string.replace(", )", ")")  # remove last ", " if any

    try:
        expected = kwargs["expected"] # grabs the expected keyword argument
    except:
        print(f"\nprintTest error for {function_call_string}:")
        print(f'\tmust provide an "expected" keywoard argument\n')
        return

    is_fruitful = True
    if "fruitful" in kwargs and kwargs["fruitful"] == False:
        is_fruitful = False

    try:
        if not is_fruitful:
            # student's function uses print rather than return
            f = io.StringIO()
            with redirect_stdout(f):
                if is_method:
                    eval(f"args[0].{function_call_string}")
                else:
                    eval(f"student_module.{function_call_string}")
            result = f.getvalue().strip() # result of student's print sans '\n'
        else:
            # fruitful function returns value
            if is_method:
                result = eval(f"args[0].{function_call_string}")
            else:
                result = eval(f"student_module.{function_call_string}") 
    except Exception as err:
        print(f"ERROR in evaluating {function_call_string}: {err}")
        return

    correct = "✓"; incorrect = "✗"
    if "simple" in kwargs and kwargs["simple"] == True:
        correct = "+"; incorrect = "X"
    is_correct = correct if result == expected else incorrect

    if is_method:
        # Consider:  <__main__.main.<locals>.Example object at 0x1003a7fa0
        # scrap "<__main__.main.<locals>." and just show object class type
        print(f"Testing <{repr(args[0]).split('.')[-1]}.{function_call_string}:")
    else:
        print(f"Testing {function_call_string}:")
    print(f" [{is_correct}]  Result   : {repr(result)}")
    print(f"      Expected : {repr(expected)}")

###################
def main() -> None:

    # see below for the defintion of the giveSum and printSum functions
    printTest(giveSum, 1, 2, 3, expected = 6)
    printTest(printSum, 1, 2, 3, expected = '6', fruitful = False)

    # see below for definition of the Example class
    e = Example(22)

    printTest(Example.getData, e, expected = 22, is_method = True)
    printTest(Example.getDataProductSum, e, 3, 4, expected = 70, is_method = True)
    printTest(Example.printData, e, expected = "22", fruitful = False, is_method = True)

##########################
if __name__ == "__main__":

    # define these only if executing main above

    def giveSum(a: int, b: int, c: int) -> int:
        return a + b + c
    def printSum(a: int, b: int, c: int) -> None:
        print(a + b + c)

    class Example:
        __slots__ = ('_data')
        def __init__(self, data: int) -> None:
            self._data = data
        def getData(self) -> int:
            return self._data
        def getDataProductSum(self, factor: int, offset: int) -> int:
            return (self._data * factor) + offset
        def printData(self) -> None:
            print(self._data)

    # call main only if executing 'python printTest.py';
    # does not call main if printTest is imported as a library
    main()
