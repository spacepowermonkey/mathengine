from typing import Any



class ArrowType(object):
    NONE        = 0
    equality    = 1
    inclusion   = 2
    restriction = 3


class Arrow(object):
    def __init__(self, start : int, end : int, data : Any):
        self.start = start
        self.end = end
        self.data = data
        return