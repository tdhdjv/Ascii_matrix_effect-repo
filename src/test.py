import curses
import sys
import time

def cmain(stdscr:"curses._CursesWindow") -> int:
    t1 = time.time_ns()
    for _ in range(1000):
        stdscr.addch(0, 0, 'a')

    print(time.time_ns()-t1)     
    stdscr.get_wch()   
    return 0

def main() -> int:
    return curses.wrapper(cmain)

if __name__ == "__main__":
    sys.exit(main())