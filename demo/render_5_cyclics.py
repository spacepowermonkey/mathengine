from mathengine.types.algebra.group import make_n_cyclic as make_n_group
from mathengine.tools.render.fancy_group import render as group_render

from mathengine.types.algebra.ring import make_n_cyclic as make_n_ring
from mathengine.tools.render.fancy_ring import render as ring_render



START = 5
STOP = START + 4
STRIDE = 1

def main(start, stop, stride):
    for i in range(start, stop, stride):
        # group = make_n_group(i)
        # group_model = group.model
        # group_render(group_model, f"z{i}-group", "/data", len(group.elements))

        ring = make_n_ring(i)
        ring_model = ring.model
        ring_render(ring_model, f"z{i}-ring", "/data", len(ring.elements))
    return



if __name__ == '__main__':
    main(START, STOP, STRIDE)
