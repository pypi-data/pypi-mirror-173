"""
This file contains code for the application "Excel Column to Decimal Converter".
Author: GlobalCreativeApkDev
"""


# Importing necessary libraries


import sys
import copy
import os


# Creating static variable


LETTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Creating static functions


def all_letters(string: str) -> bool:
    for i in string:
        if i not in LETTERS:
            return False
    return True


def get_index(string: str, c: str) -> int:
    for i in range(len(string)):
        if string[i] == c:
            return i
    return -1


def to_excel_column(number):
    # type: (int) -> ExcelColumn
    string: str = ""
    while number > 0:
        remainder = number % len(LETTERS)
        string = str(LETTERS[remainder - 1]) + string
        number //= len(LETTERS)

    return string


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary class


class ExcelColumn:
    """
    This class contains attributes of an Excel column.
    """

    def __init__(self, value):
        # type: (str) -> None
        if not (all_letters(value)):
            raise Exception("Invalid excel column: " + str(value))

        self.value: str = value

    def __str__(self):
        # type: () -> str
        return str(self.value)

    def next(self):
        # type: () -> ExcelColumn
        new_dec_value = self.to_decimal() + 1
        return to_excel_column(new_dec_value)

    def previous(self):
        # type: () -> ExcelColumn
        if self.to_decimal() < 1:
            raise Exception(str(self.value) + " is already the first Excel column!")

        new_dec_value = self.to_decimal() - 1
        return to_excel_column(new_dec_value)

    def to_decimal(self):
        # type: () -> int
        dec_value: int = 0
        for i in range(len(self.value) - 1, -1, -1):
            dec_value += (get_index(LETTERS, self.value[i]) + 1) * len(LETTERS) ** i

        return dec_value

    def clone(self):
        # type: () -> ExcelColumn
        return copy.deepcopy(self)


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    print("Welcome to 'EXCEL_COLUMN_TO_DECIMAL_CONVERTER' by 'GlobalCreativeApkDev'.")
    print("This library is used to convert Excel column to decimal.")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_using: str = input("Do you want to continue using 'EXCEL_COLUMN_TO_DECIMAL_CONVERTER'? ")
    while continue_using == "Y":
        # Clearing command line window
        clear()

        column: ExcelColumn = ExcelColumn("A")  # initial value
        excel_column: str = input("Please enter excel column: ")
        while True:
            try:
                column = ExcelColumn(excel_column)
                break
            except Exception:
                excel_column = input("Sorry, invalid input! Please enter another excel column: ")

        print("Excel column " + str(column) + " is column number " + str(column.to_decimal()) + "!")
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_using = input("Do you want to continue using 'EXCEL_COLUMN_TO_DECIMAL_CONVERTER'? ")

    return 0


if __name__ == '__main__':
    main()
