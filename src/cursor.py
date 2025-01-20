from __future__ import annotations
from typing import Iterable

class Cursor:
    def __init__(self, x:int = 0, y:int = 0) -> None:
        self.x = x
        self.y = y

    def clamp(self, text:str):
        #if the cursor is to the left
        if self.x < 0:
            pass
        #if the cursor is to the right
        #if the cursor is above
        #if the cursor is below
    
    def up(self, text:str = None):
        self.y -= 1
        if text:
            self.clamp(text)

    def down(self, text:str = None):
        self.y += 1
        if text:
            self.clamp(text)

    def left(self, text:str = None):
        self.x -= 1
        if text:
            self.clamp(text)

    def right(self, text:str = None):
        self.x += 1
        if text:
            self.clamp(text)

    def move(self, dir: Iterable, text:str = None) -> None:
        if len(dir) != 2:
            return
        self += dir
        if text:
            self.clamp()

    def move_to(self, dir: Iterable, text:str = None) -> None:
        if len(dir) != 2:
            return
        self.x = dir[0]
        self.y = dir[1]
        
        if text:
            self.clamp()

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __add__(self, other) -> Cursor:
        if isinstance(other, Iterable) and len(other) == 2:
            self.x += other[0]
            self.y += other[1]
        else:
            raise "Invalid type was added to ```Cursor```"
        return self

    def __eq__(self, value):
        if isinstance(value, Iterable) and len(value) == 2:
            return self.x == value[0] and self.y == value[1]
        if isinstance(value, Cursor):
            return self.x == value.x and self.y == value.y
        raise "Invalid type was compared with ```Cursor```"