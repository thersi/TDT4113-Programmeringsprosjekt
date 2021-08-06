""" Template for Project 1: Morse code """

import time

from GPIOSimulator_v1 import *

from GPIOSimulator_v1 import GPIOSimulator

GPIO = GPIOSimulator()

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}

# Used later to avoid random errors in GPIO and compared to input from keyboard
# 8 of each as this is approx how long a press lasts
ZERO_STRING = "00000000"
ONES_STRING = "11111111"

T = 0.25  # Approx how long a short press lasts( Equivalent to '.')
dot = T
line = 3 * T

# pauses
med = 3 * T
long = 12 * T  # Felt this interval needed to be longer than 7


class MorseDecoder():
    """ Morse code class """

    def __init__(self):
        """ initialize your class """

        # Sets the current symbol and word to empty strings that can later be added on
        self.current_symbol = ""
        self.current_word = ""

        # Creates a boolean that checks if the space bar is currently pressed
        self.pressed = False

        # Variables that later check how long a button is pressed for
        self.time_start_press = 0
        self.time_start_release = 0

    def reset(self):
        """ reset the variable for a new run """''
        self.current_symbol = ""
        self.current_word = ""
        GPIO.cleanup()  # Reseter GPIO

    def read_one_signal(self):
        """ read a signal from Raspberry Pi """
        # Gets input fom keyboard via GPIO simulator
        return GPIO.input(PIN_BTN)

    def decoding_loop(self):
        """ the main decoding loop """
        while True:  # Need an infinite loop to check state of button
            status = ""  # USed to compare to the strings defined earlier
            for i in range(8):
                status += str(self.read_one_signal())

            if status == ONES_STRING:  # Here the button is pressed, if the status equals string must mean space button is pressed.
                self.pressed = True  # Created boolean that can clarify that button is pressed
                status = ""  # Reset for new symbol
                self.time_start_press = time.time()  # Sets the start time aka when the button is first pressed.

                while self.pressed:  # As long as button is pressed
                    status += str(
                        self.read_one_signal())  # Bitsaddd to a string to see if they can be compared to the strings defined earlier
                    check = status[-8:] == ZERO_STRING  # Fetches the 8 last bits of input and compares
                    if check:  # If True, we run the process_signal method and find time
                        if time.time() - self.time_start_press > line:  # Check if the button is held down long enough for the '-' to be created
                            self.process_signal("-")
                            print("The word is now: " + self.current_word.strip())
                        else:
                            self.process_signal(".")
                            print("The word is now: " + self.current_word.strip())
                        self.pressed = False  # Confirms the button is no longer being pressed
                        self.time_start_release = time.time()

                if not self.pressed and status[-8:] == ZERO_STRING:  # If button is released and correctly compared
                    while not self.pressed:  # Here the button is released
                        status += str(self.read_one_signal())
                        if status[-8:] == ONES_STRING:  # Fetches the 8 last bits of input and compares
                            difference = time.time() - self.time_start_release
                            if long > difference >= med:  # Finds time difference and compares it to the time set for a symbol end
                                self.handle_symbol_end()
                                print("END OF SYMBOL DUE TO PAUSE \n")
                            if difference >= long:  # Finds time difference and compares it to the time set for a word end
                                print("END OF WORD - RESET \n")
                                self.handle_word_end()

                            status = ""
                            self.time_start_release = 0  # resets time
                            self.pressed = True  # this exits the loop

    def process_signal(self, signal):
        """ handle the signals using corresponding functions """
        if signal == "." or signal == "-":
            self.update_current_symbol(signal)  # upodates symbol with correct input signal
        elif signal == "2":
            self.handle_symbol_end()  # Determines that the symbol is done if signal is equal to 2

        elif signal == "3":
            self.handle_word_end()  # Determines that the word is done if signal is equal to 3

    def update_current_symbol(self, signal):
        """ append the signal to current symbol code """
        self.current_symbol += str(signal)  # Adds the string version of signal to the current symbol string.
        print("The symbol is now: " + self.current_symbol.strip())

    def handle_symbol_end(self):
        """ process when a symbol ending appears """
        if self.current_symbol in MORSE_CODE.keys():
            self.handle_LED()
            symbol = MORSE_CODE.get(
                self.current_symbol)  # collects the current letter from MORSE_CODE using the symbol as a key
            self.update_current_word(symbol)
            self.current_symbol = ""  # resets current symbol
        elif not self.current_symbol in MORSE_CODE.keys():
            print("Symbol not Morse")
            self.current_symbol = ""

    def update_current_word(self, symbol):
        self.current_word += MORSE_CODE.get(self.current_symbol)  # Adds letter value to word using symbol as a key

    def handle_word_end(self):
        """ process when a word ending appears """
        self.handle_symbol_end()
        print("The final word is: " + self.current_word.strip() + "\n -------------------------------------------- \n")
        self.reset()

    def handle_reset(self):  # Resets the current_symbol and current_word
        """ process when a reset signal received """
        self.current_symbol = ""
        self.current_word = ""

    def handle_LED(self): #This function is used to call on the correct LED lights
        symbol_check = [c for c in self.current_symbol]
        for sym in symbol_check:
            if sym == ".":
                print("\n")
                GPIO.output(4, 1)  # Sets blue light to represent a morse dot
                time.sleep(dot)  # Remains on for the duration of a dot
                GPIO.output(4, 0)
                print("\n")
            elif sym == "-":
                print("\n")
                GPIO.output(3, 1)  # Sets red light to represent morse line/dash
                GPIO.output(2, 1)
                GPIO.output(1, 1)
                time.sleep(line)  # Remains on for the duration of a morse dash
                GPIO.output(3, 0)
                GPIO.output(2, 0)
                GPIO.output(1, 0)
                print("\n")


def main():
    morse = MorseDecoder()
    morse.decoding_loop()


if __name__ == "__main__":
    main()
