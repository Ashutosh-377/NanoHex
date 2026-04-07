from PIL import Image

nhx = 'cat.nhx'

file = open(nhx, "r")

content = file.read()
lines = content.splitlines()

# size decoder
sizes = []
size_dict = {}

for i in range(len(lines)):
    if lines[i] == "":
        break
    if lines[i].startswith("@"):
        continue
    else:
        sizes.append(lines[i])

for size in sizes:
    size_lst = size.split("=")
    size_dict[size_lst[0]] = int(size_lst[1])


# palette assigner
palette_index = lines.index("@palette")
palette = []
for i in range(palette_index, len(lines), 1):
    if lines[i] == "":
        break
    if lines[i].startswith("@"):
        continue
    palette.append(lines[i].lstrip("#"))


# data to canvas(nightmare ToT)

# size valiadtion
validate = True
error = ""

data_index = lines.index("@data")
str_bin_canvas = []
int_bin_canvas = []
for i in range(data_index + 1, len(lines) ,1):
    bin_row = lines[i].split(" ")
    str_bin_canvas.append(bin_row)
for i in str_bin_canvas:
    int_bin_row = []
    for j in i:
        int_bin_row.append(int(j))
    int_bin_canvas.append(int_bin_row)
if len(int_bin_canvas) != size_dict["h"] or len(int_bin_canvas[0]) != size_dict["w"]:
    validate = False
    error += "Error: Canvas size not as per mentioned dimension\n"

# palette validation
simple_int_bin = []
data_indices = []
for i in int_bin_canvas:
    for j in i:
        simple_int_bin.append(j)
for i in simple_int_bin:
    if i not in data_indices:
        data_indices.append(i)

if max(data_indices) >= len(palette):
    validate = False
    error += "Error: Canavas conatin color out of palette\n"


if validate == True:
    canvas = []
    data_index = lines.index("@data")
    for i in range(data_index + 1, len(lines), 1):
        row = lines[i].split(" ")
        canvas_row = []
        for j in row:
            canvas_row.append(palette[int(j)])
        canvas.append(canvas_row)
    
    rgb_canvas = []
    for i in canvas:
        rgb_row = []
        for j in i:
            rgb_row.append(tuple(int(j[k:k+2], 16) for k in range(0, 6, 2)))
        rgb_canvas.append(rgb_row)

    img = Image.new(mode="RGB", size=(size_dict['w'], size_dict['h']))
    pixel = img.load()

    for i in range(len(rgb_canvas)):
        for j in range(len(rgb_canvas[i])):
            pixel[j, i] = rgb_canvas[i][j]

    res = img.resize((size_dict['w'] * 10, size_dict['h'] * 10), Image.NEAREST)

    res.show()
else:
    print(error)

file.close()