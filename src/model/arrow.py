from typing import Any



class ArrowType(object):
    equality = 0
    inclusion = 1
    restriction = -1


class Arrow(object):
    def __init__(self, start : int, end : int, data : Any):
        self.start = start
        self.end = end
        self.data = data
        return