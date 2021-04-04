
import curses
import time

from collections import OrderedDict

class Windows:
    """
    This class initialize the screen windows via curses library.
    There are several windows :
        win_text : where text messages from users are displayed
        separation : like its name
        win_input : where user can write message
    """


    """
    Initialize new Windows object. All settings are prepared in this method.
    Messages are mapped to a row line number from the win_text window.
    """
    def __init__(self):
        self._screen = curses.initscr()
        self._num_rows, self._num_cols = self._screen.getmaxyx()
        self._win_text_rows = self._num_rows - 4
        self._win_text_message_first_row = self._win_text_rows - 1
        self._win_text = curses.newwin(self._win_text_rows, self._num_cols, 0, 1)
        self._separation = curses.newwin(1, self._num_cols, self._win_text_rows + 1, 1)
        self._win_input = curses.newwin(3, self._num_cols, self._win_text_rows + 2, 1)
        self._map_messages = {}

        # we have to init all values
        for i in range(0, self._win_text_rows):
            self._map_messages[i] = ""

        # create separation according to the width of the window
        for col in range(0, self._num_cols - 1):
            self._separation.addstr(0, col, "-")


    """
    Run windows displaying
    """
    def start_display(self):
        self._win_text.refresh()
        self._separation.refresh()
        self._win_input.refresh()


    """
    End windows displaying
    """
    def end_display(self):
        curses.endwin()


    """
    Method to add text message in the win_text view.
    map_messages dictionary are computed each time.
    """
    def add_text(self, message:str):

        x = self._num_cols - 2 - len(message)
        for i in range(0,x):
            message = str(message) + " "

        for row, msg in self._map_messages.items():
            if row == self._win_text_message_first_row:
                break
            self._map_messages[row] = self._map_messages[row + 1]

        self._map_messages[self._win_text_message_first_row] = message

        for row, msg in self._map_messages.items():
            self._win_text.addstr(row, 1, msg)

        self._win_text.refresh()
        self._win_input.refresh()


    def get_input(self):
        data = self._win_input.getstr()
        self._win_input.clear()
        self._win_input.refresh()
        return data.decode('utf-8')


"""
Test purposes
"""
if __name__ == "__main__":
    win = Windows()
    win.start_display()
    time.sleep(1)

    for i in range(0,3):
        win.add_text("test " + str(i))
        time.sleep(0.5)

    input_text = win.get_input()

    win.end_display()
    print(win._map_messages)
    print(input_text)

