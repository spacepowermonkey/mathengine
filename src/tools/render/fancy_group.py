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


def split_to_submatrices(rows, cols, cs, cut_val):
    elements = {'xs':[], 'ys': [], 'cs': []}
    pairs = {'xs':[], 'ys': [], 'cs': []}
    op = {'xs':[], 'ys': [], 'cs': []}
    levels = {'xs':[], 'ys': [], 'cs': []}

    size = len(rows)

    for i in range(size):
        # Clearly mark rows vs columns
        x = cols[i]
        y = rows[i]
        c = cs[i]

        if x < cut_val:
            if y < cut_val:
                elements['xs'].append(x)
                elements['ys'].append(y)
                elements['cs'].append(c)
            else:
                pairs['xs'].append(x)
                pairs['ys'].append(y)
                pairs['cs'].append(c)
        else:
            if y < cut_val:
                op['xs'].append(x)
                op['ys'].append(y)
                op['cs'].append(c)
            else:
                levels['xs'].append(x)
                levels['ys'].append(y)
                levels['cs'].append(c)

    return elements, pairs, op, levels


def render(model, name, path, group_size):
    cut_val = group_size + 1
    full_val = 1 + group_size + group_size ** 2 # star + elements + pairs
    cut_ratio = cut_val / full_val

    bound_low = [-1, cut_val + 1]
    bound_high = [cut_val - 1, full_val + 1]

    rows, cols, cs = arrows_to_colors(model)
    elements, pairs, op, levels = split_to_submatrices(rows, cols, cs, cut_val)


    fig_width = 20
    fig_height = 20
    widths = [0.92*cut_ratio, 0.92*(1 - cut_ratio), 0.08]
    heights = [0.05, 0.03, 0.92*cut_ratio, 0.92*(1 - cut_ratio)]

    fig = plt.figure(figsize=(fig_width, fig_height))
    grid = GridSpec(4, 3, figure=fig,
        wspace=0.08, hspace=0.08, left=0.02, bottom=0.02, right=0.98, top=0.98,
        width_ratios=widths, height_ratios=heights
    )

    ax_title = fig.add_subplot(grid[0,:])
    ax_title.text(0.5, 0.5, f"{name}", fontsize='xx-large', va='center', ha='center')
    ax_title.set_xticks([])
    ax_title.set_yticks([])
    ax_title.set(frame_on=False)

    ax_elements_in = fig.add_subplot(grid[1,0])
    ax_elements_in.text(0.5, 0.5, f"IN: elm", fontsize='large', va='center', ha='center')
    ax_elements_in.set_xticks([])
    ax_elements_in.set_yticks([])
    ax_elements_in.set(frame_on=False)
    
    ax_elements_out = fig.add_subplot(grid[2,2])
    ax_elements_out.text(0.5, 0.5, f"OUT: elm", fontsize='large', va='center', ha='center')
    ax_elements_out.set_xticks([])
    ax_elements_out.set_yticks([])
    ax_elements_out.set(frame_on=False)
    
    ax_pairs_in = fig.add_subplot(grid[1,1])
    ax_pairs_in.text(0.5, 0.5, f"IN: pair", fontsize='large', va='center', ha='center')
    ax_pairs_in.set_xticks([])
    ax_pairs_in.set_yticks([])
    ax_pairs_in.set(frame_on=False)
    
    ax_pairs_out = fig.add_subplot(grid[3,2])
    ax_pairs_out.text(0.5, 0.5, f"OUT: pair", fontsize='large', va='center', ha='center')
    ax_pairs_out.set_xticks([])
    ax_pairs_out.set_yticks([])
    ax_pairs_out.set(frame_on=False)


    ax_elements = fig.add_subplot(grid[2,0])
    ax_pairs = fig.add_subplot(grid[3,0])
    ax_op = fig.add_subplot(grid[2,1])
    ax_levels = fig.add_subplot(grid[3,1])


    ax_elements.set_xlabel("elm -> elm")
    ax_elements.scatter(elements['xs'], elements['ys'], color=elements['cs'], s=(100/model.size))

    ax_elements.set_facecolor('#222222')
    ax_elements.set_xlim(bound_low)
    ax_elements.set_ylim(bound_low)
    ax_elements.invert_yaxis()
    ax_elements.set_xticks([])
    ax_elements.set_yticks([])


    ax_pairs.set_xlabel("elm -> pair")
    ax_pairs.scatter(pairs['xs'], pairs['ys'], color=pairs['cs'], s=(100/model.size))

    ax_pairs.set_facecolor('#222222')
    ax_pairs.set_xlim(bound_low)
    ax_pairs.set_ylim(bound_high)
    ax_pairs.invert_yaxis()
    ax_pairs.set_xticks([])
    ax_pairs.set_yticks([])


    ax_op.set_xlabel("pair -> elm")
    ax_op.scatter(op['xs'], op['ys'], color=op['cs'], s=(100/model.size))

    ax_op.set_facecolor('#222222')
    ax_op.set_xlim(bound_high)
    ax_op.set_ylim(bound_low)
    ax_op.invert_yaxis()
    ax_op.set_xticks([])
    ax_op.set_yticks([])


    ax_levels.set_xlabel("pair -> pair")
    ax_levels.scatter(levels['xs'], levels['ys'], color=levels['cs'], s=(100/model.size))

    ax_levels.set_facecolor('#222222')
    ax_levels.set_xlim(bound_high)
    ax_levels.set_ylim(bound_high)
    ax_levels.invert_yaxis()
    ax_levels.set_xticks([])
    ax_levels.set_yticks([])


    png_path = f'{path}/{name}.png'
    fig.savefig(png_path)
    return
