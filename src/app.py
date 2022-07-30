from util import designer
from curses import wrapper, window


class AppUI(designer.TUI):
    """
    +------------------------+
    | App Layout             |
    |          +-------------+
    |          |             |
    +----------+             |
    |          |             |
    |          +-------------+
    |          |             |
    +----------+-------------+
    """
@wrapper
def draw(stdscr: window):
    for b in AppUI.boxes():
        bwin = stdscr.subwin(*b)
        bwin.box()
    stdscr.refresh()
    stdscr.getch()

    return lambda *_: None

draw()
