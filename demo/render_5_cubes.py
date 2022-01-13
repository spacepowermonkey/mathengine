from mathengine.types.shape.cube import Cube
from mathengine.tools.render.basic_grid import render



def main():
    for i in range(5):
        model = Cube(i).model
        render(model, f"{i}-cube", "/data")    
    return



if __name__ == '__main__':
    main()
