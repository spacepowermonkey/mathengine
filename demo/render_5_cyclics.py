from mathengine.types.algebra.group import make_n_cyclic
from mathengine.tools.render.basic_grid import render



def main():
    for i in range(2, 7): # This renders z2 to z6
        model = make_n_cyclic(i).model
        render(model, f"z{i}-group", "/data")    
    return



if __name__ == '__main__':
    main()
