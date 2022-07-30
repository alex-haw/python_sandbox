import curses, curses.panel, curses.ascii, curses.textpad
import random
import string
import sys
from loguru import logger
from pathlib import Path
logger.remove()
@curses.wrapper
def main(scr: curses.window):
    scr.leaveok(True)
    
    scr.box()
    bcr: curses.window = scr.subpad(*[n - 4 for n in scr.getmaxyx()], 2, 2)
    pcr: curses.window = scr.subpad(*[n - 6 for n in scr.getmaxyx()], 3, 3)
    # pcr.box()
    scr.refresh()
    pcr.scrollok(True)
    curses.raw()
    j = 0
    pcr.leaveok(False)
    t = curses.textpad.Textbox(pcr, True)
    i = 0
    with open(sys.argv[1], '+w') as wl:
        for l in wl.readlines():
            ly = min(i, pcr.getmaxyx()[0])
            lx = int(pcr.getmaxyx()[1])
            pcr.addnstr(ly, 0, l, lx-4)
            i+=1
    pcr.refresh()
    i = 0
    def logln(l):
        nonlocal i
        ly = min(i, pcr.getmaxyx()[0]-5)
        lx = int(pcr.getmaxyx()[1]/2)
        pcr.addnstr(ly, lx, l, lx-4)
        pcr.refresh()
        i+=1
    logger.add(logln, format="{message}")
    for f in Path().cwd().glob("*"):
        logln(f.as_posix())
    
    do_save = False
    bcr.box()
    bcr.refresh()
    fstr = "[ " + sys.argv[1] + " ]"
    bcr.addstr(0,int(bcr.getmaxyx()[1]/2 - len(sys.argv[1])/2), fstr)
    bcr.refresh()    
    curses.curs_set(2)
    def val(c):
        scr.getch()
        # p = list(pcr.getyx())
        # logger.debug(str(c)+" "+chr(c))
        if curses.ascii.unctrl(c) == '^S':
            with open(sys.argv[1], 'w') as wl:
                wl.write(t.gather())
        if curses.ascii.unctrl(c) == '^Q':
            return curses.ascii.BEL
        if c == 10:
            pcr.move(pcr.getyx()[0]+1, 0)
            return curses.ascii.SI            
        if c == curses.KEY_BACKSPACE and pcr.getyx()[1] == 0:
            pcr.deleteln()
        if curses.ascii.unctrl(c) == '^h':
            for l in [l for l in curses.textpad.Textbox.__doc__.split('. ') if l.strip()]:
                pcr.addstr(i, 0, l)
                i += 1
        # pcr.move(*p)
        return c
    t.stripspaces = True
    t.edit(validate=val)