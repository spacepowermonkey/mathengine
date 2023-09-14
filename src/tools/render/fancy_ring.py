import cairosvg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from dataclasses import dataclass
from matplotlib.gridspec import GridSpec



from ..map import map as mmap
from ...model import ArrowType



ARROW_COLORS = {
    ArrowType.NONE          : '#000000',
    ArrowType.equality      : '#785EF0',
    ArrowType.inclusion     : '#FE6100',
    ArrowType.restriction   : '#648FFF',
    ArrowType.equivalence   : '#DC267F',
}

def arrows_to_colors(model):
    rows = []
    cols = []
    cs = []

    for col, objs in model._arrows.items():
        for row, arrow in objs.items():
            rows.append(row)
            cols.append(col)
            cs.append(ARROW_COLORS[arrow.data])
    return (rows, cols, cs)


@dataclass
class RingRegion:
    xs : []
    ys : []
    cs : []

    def set(self, x, y, c):
        self.xs.append(x)
        self.ys.append(y)
        self.cs.append(c)
        return


@dataclass
class RingStructure:
    elements : RingRegion

    plus_pairs : RingRegion
    plus_op : RingRegion
    plus_levels : RingRegion

    mult_pairs : RingRegion
    mult_op : RingRegion
    mult_levels : RingRegion

    plus_to_mult : RingRegion
    mult_to_plus : RingRegion



def split_to_submatrices(rows, cols, cs, group_size):
    structure = RingStructure(
        RingRegion([],[],[]),

        RingRegion([],[],[]),
        RingRegion([],[],[]),
        RingRegion([],[],[]),

        RingRegion([],[],[]),
        RingRegion([],[],[]),
        RingRegion([],[],[]),

        RingRegion([],[],[]),
        RingRegion([],[],[])
    )

    size = len(rows)
    cut1 = group_size + 1
    cut2 = group_size ** 2 + group_size + 1

    for i in range(size):
        # Clearly mark rows vs columns
        x = cols[i]
        y = rows[i]
        c = cs[i]

        if x < cut1:
            if y < cut1:
                structure.elements.set(x, y, c)
            elif y < cut2:
                structure.plus_pairs.set(x, y, c)
            else:
                structure.mult_pairs.set(x, y, c)
        elif x < cut2:
            if y < cut1:
                structure.plus_op.set(x, y, c)
            elif y < cut2:
                structure.plus_levels.set(x, y, c)
            else:
                structure.plus_to_mult.set(x, y, c)
        else:
            if y < cut1:
                structure.mult_op.set(x, y, c)
            elif y < cut2:
                structure.mult_to_plus.set(x, y, c)
            else:
                structure.mult_levels.set(x, y, c)

    return structure



def configure_text_ax(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set(frame_on=False)
    return

def build_title_and_text(fig, grid, name):
    ax_title = fig.add_subplot(grid[0,:])
    ax_title.text(0.1, 0.5, f"{name}", fontsize='xx-large', va='center', ha='center')
    configure_text_ax(ax_title)

    ax_elements_in = fig.add_subplot(grid[1,0])
    ax_elements_in.text(0.5, 0.5, f"IN: elm", fontsize='large', va='center', ha='center')
    configure_text_ax(ax_elements_in)
    
    ax_elements_out = fig.add_subplot(grid[2,3])
    ax_elements_out.text(0.5, 0.5, f"OUT: elm", fontsize='large', va='center', ha='center')
    configure_text_ax(ax_elements_out)

    ax_plus_pairs_in = fig.add_subplot(grid[1,1])
    ax_plus_pairs_in.text(0.5, 0.5, f"IN: plus(,)", fontsize='large', va='center', ha='center')
    configure_text_ax(ax_plus_pairs_in)
    
    ax_plus_pairs_out = fig.add_subplot(grid[3,3])
    ax_plus_pairs_out.text(0.5, 0.5, f"OUT: plus(,)", fontsize='large', va='center', ha='center')
    configure_text_ax(ax_plus_pairs_out)

    ax_mult_pairs_in = fig.add_subplot(grid[1,2])
    ax_mult_pairs_in.text(0.5, 0.5, f"IN: mult(,)", fontsize='large', va='center', ha='center')
    configure_text_ax(ax_mult_pairs_in)
    
    ax_mult_pairs_out = fig.add_subplot(grid[4,3])
    ax_mult_pairs_out.text(0.5, 0.5, f"OUT: mult(,)", fontsize='large', va='center', ha='center')
    configure_text_ax(ax_mult_pairs_out)
    return


def configure_struct_ax(ax, xlim, ylim):
    ax.set_facecolor('#222222')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    return

def build_ring_structure(fig, grid, structure, size, bounds):
    layout = {
        0: [ ("elm -> elm", structure.elements, bounds[0][0]), ("plus(,) -> elm", structure.plus_op, bounds[0][1]), ("mult(,) -> elm", structure.mult_op, bounds[0][2])],
        1: [ ("elm -> plus(,)", structure.plus_pairs, bounds[1][0]), ("plus(,) -> plus(,)", structure.plus_levels, bounds[1][1]), ("mult(,) -> plus(,)", structure.mult_to_plus, bounds[1][2])],
        2: [ ("elm -> mult(,)", structure.mult_pairs, bounds[2][0]), ("plus(,) -> mult(,)", structure.plus_to_mult, bounds[2][1]), ("mult(,) -> mult(,)", structure.mult_levels, bounds[2][2])],
    }

    for row, cols in layout.items():
        for col, data in enumerate(cols):
            name, vals, lims = data

            xidx = row + 2
            yidx = col

            ax = fig.add_subplot(grid[xidx, yidx])
            ax.set_xlabel(name)
            ax.scatter(vals.xs, vals.ys, color=vals.cs, s=(100/size))
            configure_struct_ax(ax, lims['xlim'], lims['ylim'])
    return


def render(model, name, path, group_size):
    rows, cols, cs = arrows_to_colors(model)
    structure = split_to_submatrices(rows, cols, cs, group_size)


    weights = [group_size + 1, group_size ** 2, group_size ** 2]
    steps = [0, sum(weights[:1]), sum(weights[:2]), sum(weights[:3])]
    ratios = [(steps[i+1]-steps[i])/sum(weights) for i in range(len(steps) - 1)]

    bounds = [
        [{
            'ylim':(steps[i]-1, steps[i+1]+1),
            'xlim':(steps[j]-1, steps[j+1]+1)
        } for j in range(3)]
    for i in range(3)]

    print(bounds)

    fig_width = 20
    fig_height = 20
    fig_scale = 0.95
    widths = [fig_scale * r for r in ratios] + [0.05]
    heights = [0.03, 0.02] + [fig_scale * r for r in ratios]


    fig = plt.figure(figsize=(fig_width, fig_height))
    grid = GridSpec(5, 4, figure=fig,
        wspace=0.08, hspace=0.08, left=0.02, bottom=0.02, right=0.98, top=0.98,
        width_ratios=widths, height_ratios=heights
    )

    build_title_and_text(fig, grid, name)
    build_ring_structure(fig, grid, structure, model.size, bounds)

    png_path = f'{path}/{name}.png'
    fig.savefig(png_path)
    return
