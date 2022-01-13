import cairosvg

from dataclasses import dataclass



from ..map import map as mmap
from ...model import ArrowType



@dataclass
class Const:
    data_width = 200
    point_radius = 4
    point_width = 2 * (point_radius + 1)


    header_height = 100
    header_width = 100



def obj_render(obj):
    svg = ""
    return svg


ARROW_COLORS = {
    ArrowType.NONE          : '#000000',
    ArrowType.equality      : '#785EF0',
    ArrowType.inclusion     : '#DC267F',
    ArrowType.restriction   : '#648FFF',
}
def arr_color(arr):
    return ARROW_COLORS[arr.data]

def arr_render(arr):
    cx = Const.header_width + Const.point_width * (arr.start + 0.5)
    cy = Const.header_height + Const.point_width * (arr.end + 0.5)
    svg = f'<circle cx="{cx}" cy="{cy}" r="{Const.point_radius}" stroke="None" fill="{arr_color(arr)}"/>'
    return svg



def render(model, name, path, render_data=False):
    array_width = model.size * Const.point_width

    svg_width = array_width + (Const.data_width if render_data else 0) + Const.header_width
    svg_height = array_width + Const.header_height

    svg = f'<svg width="{svg_width}" height="{svg_height}" viewbox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">'

    obj_svg, arr_svg = mmap( 
        model, obj_render, "", arr_render, ""
    )
    svg += obj_svg + arr_svg
    svg += '</svg>'

    svg_path = f'{path}/{name}.svg'
    png_path = f'{path}/{name}.png'

    with open(svg_path, 'w') as handle:
        handle.write(svg)

    cairosvg.svg2png(
        bytestring=open(svg_path, 'rb').read(), write_to=png_path
    )
    return
