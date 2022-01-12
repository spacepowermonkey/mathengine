from mathengine.types.shape.cube import Cube
from mathengine.tools.render.basic_grid import render



def main():
    model = Cube(5).model

    print(model.size)
    print(model.complexity)

    render(model, "5-cube", "/data")
    
    return



if __name__ == '__main__':
    main()
