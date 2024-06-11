from enum import Enum

class Region(list, Enum):
	UVVIS = range(200, 800, 1)
	IR = range(700, 2000, 1)
	LARGE = range(100, 2000, 1)
	MID = range(50, 1000, 1)
	ALL = range(1, 2000, 1)
