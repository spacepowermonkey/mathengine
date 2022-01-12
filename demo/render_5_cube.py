from mathengine.types.shape.cube import Cube
from mathengine.tools.render.basic_grid import render



def main():
    render(Cube(5).model, "5-cube", "/data")
    return



if __name__ == '__main__':
    main()
