import svgwrite
def draw_chart(asc_index, bucket, size=720):
    dwg = svgwrite.Drawing(size=(size,size))
    pad = 20
    dwg.add(dwg.rect(insert=(pad,pad), size=(size-2*pad,size-2*pad), fill='white', stroke='black'))
    font_size = 14
    y = pad+20
    for i in range(12):
        labels = ','.join(bucket.get(i,[]))
        dwg.add(dwg.text(f"{i+1}: {labels}", insert=(pad+10,y), font_size=font_size))
        y += 22
    return dwg.tostring()
