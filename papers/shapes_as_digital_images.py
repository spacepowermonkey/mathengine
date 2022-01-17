from mathengine.types.shape.basic import Point, Interval, Loop
from mathengine.tools.render.basic_grid import render



def render_shape(shape, name):
    model = shape.model
    render(model, name, "/data")
    return

def main():
    render_shape(Point(), "point")
    render_shape(Interval(), "interval")
    render_shape(Loop(), "loop")
    
    square = Interval() * Interval()
    render_shape(square, "square")
    
    cylinder = Interval() * Loop()
    render_shape(cylinder, "cylinder")

    glue = cylinder - square
    render_shape(glue, "glue")
    return



if __name__ == '__main__':
    main()
