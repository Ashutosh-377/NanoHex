from PIL import Image

img_file = 'cat.png'
nhx = 'cat.nhx'
height = 32
width = 32
max_color = 16

image = Image.open(img_file)
res = image.resize((width, height), Image.NEAREST)
indexed_img = res.convert(mode="P", palette=Image.ADAPTIVE, colors=max_color)
unord_palette = indexed_img.getpalette()


ord_palette = []

for i in range(0, max_color * 3, 3):
    color = tuple(unord_palette[i:i+3])
    ord_palette.append(color)

ord_hex_palette = []
for i in ord_palette:
    hex_color = '#{:02X}{:02X}{:02X}'.format(i[0], i[1], i[2])
    ord_hex_palette.append(hex_color)

unord_data = indexed_img.get_flattened_data()

ord_data = []
for i in range(0, len(unord_data), width):
    row = tuple(unord_data[i:i+width])
    ord_data.append(row)


nhx_file = open(nhx, "w")

nhx_file.write("@size\n")
nhx_file.write(f"h={height}\n")
nhx_file.write(f"w={width}\n")
nhx_file.write("\n")
nhx_file.write("@palette\n")
for i in ord_hex_palette:
    nhx_file.write(f"{i}\n")
nhx_file.write("\n")
nhx_file.write("@data\n")
for i in ord_data:
    line = " ".join(str(x) for x in i)
    nhx_file.write(f"{line}\n")