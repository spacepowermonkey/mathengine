import cairosvg

from dataclasses import dataclass
from typing import Tuple



from ..map import map as mmap



@dataclass
class Const:
    text_indent : int = 2

    row_height : int = 20
    row_key_width : int = 20
    row_data_width : int = 80
    row_width : int = row_key_width + row_data_width

    column_height : int = 20
    column_width : int = 20

    array_height : int = row_height
    array_width : int = column_width

    row_offset : Tuple[int,int] = (0, column_height)
    column_offset : Tuple[int,int] = (row_width, 0)
    array_offset : Tuple[int,int] = (row_width, column_height)



def obj_render_row(obj):
    row_y = obj.idx * Const.row_height + Const.text_indent
    return f'<text x="{Const.text_indent}" y="{row_y}">{obj.idx}</text><text x="{Const.text_indent+Const.row_key_width}" y="{row_y}">{obj.data}</text>'

def obj_render_column(obj):
    col_x = obj.idx * Const.column_width + Const.text_indent
    return f'<text x="{col_x}" y="{Const.text_indent}">{obj.idx}</text>'

def obj_render(obj):
    print("RENDERING!")
    return f'<g transform="translate({Const.row_offset[0], Const.row_offset[1]})">{obj_render_row(obj)}</g>' + \
            f'<g transform="translate({Const.row_offset[0], Const.row_offset[1]})">{obj_render_column(obj)}</g>'


def arr_render(arr):
    svg = ""
    return svg



def render(model, name, path):
    column_total_width = model.size * Const.column_width
    row_total_height = model.size * Const.row_height
    svg_width = Const.row_width + column_total_width
    svg_height = row_total_height + Const.column_height

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
