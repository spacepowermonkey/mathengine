from mathengine.types.shape.cube import Cube
from mathengine.types.shape.basic import Interval
from mathengine.tools.render.basic_grid import render



def main():
    model = Cube(5).model
    print(f"5-cube: {model.size} {model.complexity}")
    render(model, "5-cube", "/data")


    model = Interval().model
    print(f"5-cube: {model.size} {model.complexity}")
    render(model, "interval", "/data")
    
    return



if __name__ == '__main__':
    main()
