from mathengine.types.shape.basic import Point, Interval, Loop
from mathengine.types.shape.cube import Cube
from mathengine.tools.render.basic_grid import render



def render_shape(shape, name):
    model = shape.model
    render(model, name, "/data")
    return

def main():
    # We also used shapes_as_digital_images to generate some pictures.
    
    torus = Loop() * Loop()
    render_shape(torus, "torus")
    

    two = Point() + Point()
    three = Point() + Point() + Point()
    five = two + three
    six = two * three

    render_shape(two, "two")
    render_shape(three, "three")
    render_shape(five, "five")
    render_shape(six, "six")


    for i in range(5):
        cube = Cube(i)
        render_shape(cube, f"cube-{i}")

    return



if __name__ == '__main__':
    main()
