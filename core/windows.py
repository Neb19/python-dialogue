
import curses
import time

from collections import OrderedDict

class Windows:
    """
    This class initialize the screen windows via curses library.
    There are several windows :
        messagesWindow : where text messages from users are displayed
        separationWindow : like its name
        inputWindow : where user can write message
    """


    """
    Initialize new Windows object. All settings are prepared in this method.
    Messages are mapped to a row line number on the screen in the messagesWindow window.
    """
    def __init__(self):
        self._screen = curses.initscr()
        self._num_rows, self._num_cols = self._screen.getmaxyx()
        self._messagesWindow_rows = self._num_rows - 4
        self._messagesWindow_message_first_row = self._messagesWindow_rows - 1
        self._messagesWindow = curses.newwin(self._messagesWindow_rows, self._num_cols, 0, 1)
        self._separationWindow = curses.newwin(1, self._num_cols, self._messagesWindow_rows + 1, 1)
        self._inputWindow = curses.newwin(3, self._num_cols, self._messagesWindow_rows + 2, 1)
        self._map_messages = {}

        # we have to init all values
        for i in range(0, self._messagesWindow_rows):
            self._map_messages[i] = ""

        # create separationWindow according to the width of the window
        for col in range(0, self._num_cols - 1):
            self._separationWindow.addstr(0, col, "-")


    """
    Run the display windows
    """
    def start_display(self):
        self._messagesWindow.refresh()
        self._separationWindow.refresh()
        self._inputWindow.refresh()


    """
    End the display windows
    """
    def end_display(self):
        curses.endwin()


    """
    Method to add text message in the messagesWindow view.
    map_messages dictionary are computed each time to order it.
    """
    def add_text(self, message:str):

        x = self._num_cols - 2 - len(message)
        for i in range(0,x):
            message = str(message) + " "

        for row, msg in self._map_messages.items():
            if row == self._messagesWindow_message_first_row:
                break
            self._map_messages[row] = self._map_messages[row + 1]

        self._map_messages[self._messagesWindow_message_first_row] = message

        for row, msg in self._map_messages.items():
            self._messagesWindow.addstr(row, 1, msg)

        self._messagesWindow.refresh()
        self._inputWindow.refresh()


    def get_input(self):
        self._inputWindow.addstr(0, 1, "message: ")
        data = self._inputWindow.getstr()
        self._inputWindow.clear()
        self._inputWindow.refresh()
        return data.decode('utf-8')


