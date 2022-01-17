from mathengine.types.shape.cube import Cube
from mathengine.tools.render.basic_grid import render



def main():
    for i in range(6): # This renders 0 (the point) to 5 (the 5-cube).
        model = Cube(i).model
        render(model, f"{i}-cube", "/data")    
    return



if __name__ == '__main__':
    main()
