from typing import NamedTuple

import curses

class Color(NamedTuple):
    r: int
    g: int
    b: int

    @classmethod
    def parse(cls, s:str) -> None:
        if s.startswith('#') and len(s) >= 7:
            return cls(r=int(s[1:3], 16), g=int(s[3:5], 16), b=int(s[5:7], 16))
        elif s.startswith('#'):
            return cls.parse(f'#{s[1] * 2}{s[2] * 2}{s[3] * 2}')

def color_to_curse(color:Color) -> tuple:
    multiplier = 1000/255
    return int(color.r*multiplier), int(color.g*multiplier), int(color.b*multiplier)
    
class ColorLibrary:
    """Holds all the colors that is currently being used in the program.\n
    Is able to retrive the a give color pair index by taking in the ```Color``` object"""
    _colors: dict[Color, int] = {}
    _color_pairs: dict[tuple[int, int], int] = {}

    def get_color_number(self, color:Color| None = None) -> int:
        if color == None:
            return -1
        #Find the color that is registered
        try:
            return self._colors[color]
        except:
            pass
        #if it is not registered register it and return the index
        return self.init_color(color)

    def get_color_pair_number(self, fg: Color|None = None, bg: Color|None = None) -> int:
        """Finds the pair number that has the color of that was passed in the arguments"""
        
        #Find the color pair that is registers
        try:
            fg_i = self._colors[fg]
            bg_i = self._colors[bg]
            return self._color_pairs[(fg_i, bg_i)]
        except:
            pass
        #if it is not registred register it and return the index
        return self.init_color_pair(fg, bg)

    def get_color_pair(self, fg: Color|None = None, bg: Color|None = None) -> int:
        """Finds the pair number that has the color of that was passed in the arguments.\n
          However also calls ```curses.color_pair``` so you don't have to"""
        
        return curses.color_pair(self.get_color_pair_number(fg, bg))
        
    def init_color(self, color: Color) -> int:
        if curses.can_change_color():
            n = min(self._colors.values(), default = curses.COLORS) -1
            self._colors[color] = n
            curses.init_color(n, *color_to_curse(color))
            return n
        return -1

    def init_color_pair(self, fg: Color|None, bg: Color|None = None) -> int:
        fg_index = self.get_color_number(fg)
        bg_index = self.get_color_number(bg)
        n = len(self._color_pairs)+1
        curses.init_pair(n, fg_index, bg_index)
        self._color_pairs[(fg_index, bg_index)] = n
        return n

    def __str__(self) -> str:
        string = 'Colors Registered: \n'
        for color, index in self._colors.items():
            string += f"<{index}> {color}\n"
        string += '-'*100+'\n Colors Pairs Registered: \n'
        for color_pair, index in self._color_pairs.items():
            string += f"<{index}> [fg: {color_pair[0]}, bg:{color_pair[1]}]\n"
        string.removesuffix('\n')
        return string