#std
import sys
import time
import random
#3rd party
import curses

#1st party
from cursor import Cursor
from color import Color, ColorLibrary

def cmain(stdscr: "curses._CursesWindow") -> int:
    bg_text = ""
    rain_chars = "@#!%^(E%^#"

    for _ in range(curses.LINES*curses.COLS):
        added_char = rain_chars[random.randint(0, len(rain_chars)-1)]
        bg_text += added_char
    
    drops:list[tuple[Cursor, int]] = []

    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    glow_color = Color.parse("#E6FFC9")
    filled_color = Color.parse("#87FA50")
    text_color = Color.parse("#00330D")
    bg_color = Color.parse("#000")
    color_manager = ColorLibrary()
    
    stdscr.bkgd(' ', color_manager.get_color_pair(text_color, bg_color))
    stdscr.nodelay(True)
    
    text_gen_amount = 8
    last_time = time.time()
    while True:
        try:
            char = stdscr.get_wch()
            if char == '\n':
                break
        except curses.error:
            pass

        for head, length in drops:
            y1 = head.y
            y2 = head.y-1
            y3 = head.y-length+2
            y4 = head.y-length

            p1 = head.x + y1*(curses.COLS)
            p2 = head.x + y2*(curses.COLS)
            p3 = head.x + y3*(curses.COLS)

            if 0 <= y1 < curses.LINES:
                char = bg_text[p1]
                stdscr.addch(y1, head.x, char, color_manager.get_color_pair(glow_color, bg_color))
            if 0 <= y2 < curses.LINES:
                char = bg_text[p2]
                stdscr.addch(y2, head.x, char, color_manager.get_color_pair(filled_color, bg_color))
            if 0 <= y3 < curses.LINES:
                char = bg_text[p3]
                stdscr.addch(y3, head.x, char, color_manager.get_color_pair(text_color, bg_color))
            if 0 <= y4 < curses.LINES:
                stdscr.addch(y4, head.x, ' ')
            
            if y4 >= curses.LINES:
                drops.remove((head, length))
                continue
            
            head.y += 1
        stdscr.refresh()
        while time.time()-last_time < 0.05:
            pass
        last_time = time.time()
        p = random.random()
        if p < 0.8:
            x_list = random.sample(range(0, curses.COLS-1), text_gen_amount)
            y_list = [random.randrange(5,10) for _ in range(text_gen_amount)]
            for x, y in zip(x_list, y_list):
                drops.append((Cursor(x, 0), y))
            

def main() -> int:
    return curses.wrapper(cmain)

if __name__ == "__main__":
    sys.exit(main())
