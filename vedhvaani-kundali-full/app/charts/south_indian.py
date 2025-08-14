import svgwrite
def draw_chart(asc_index, bucket, size=720):
    dwg = svgwrite.Drawing(size=(size,size))
    pad = 20
    cell = (size-2*pad)/4.0
    for i in range(5):
        dwg.add(dwg.line(start=(pad+i*cell,pad), end=(pad+i*cell,size-pad), stroke='black'))
        dwg.add(dwg.line(start=(pad,pad+i*cell), end=(size-pad,pad+i*cell), stroke='black'))
    font_size = 14
    for i in range(12):
        row = i//4; col = i%4
        labels = ','.join(bucket.get(i,[]))
        x = pad + col*cell + 8
        y = pad + row*cell + 20
        dwg.add(dwg.text(f"{i+1}: {labels}", insert=(x,y), font_size=font_size))
    return dwg.tostring()
