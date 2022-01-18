from .basic import Interval, Shape



class Cube(Shape):
    def __init__(self, dimension):
        cube = Interval() ** dimension
        cube_model = cube.model

        super().__init__(model=cube_model)
        return
