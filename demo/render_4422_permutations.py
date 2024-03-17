from mathengine.types.algebra.group import make_n_cyclic as make_n_group
from mathengine.tools.render.fancy_group import render as group_render



CONFIGS = [
    (4, 4, 2, 2),
    (4, 2, 4, 2),
    (4, 2, 2, 4),
    (2, 4, 4, 2),
    (2, 4, 2, 4),
    (2, 2, 4, 4)
]



def prod(groups):
    result = groups[0]
    tail = groups[1:]
    while(len(tail) > 0):
        result = result * tail[0]
        tail = tail[1:]
    return result

def main(configs, reverse=False):
    for config in configs:
        groups = [make_n_group(i) for i in config]
        if reverse:
            groups = list(reversed(groups))
        group = prod(groups)
        group_model = group.model

        group_labels = [f"z{i}" for i in config]
        group_render(group_model, f"{'-'.join(group_labels)}-group", "/data", len(group.elements))

    return



if __name__ == '__main__':
    main(CONFIGS)
