import numpy as np

# number of terms to generate
n_max = 75

# margins around image, in pixels
svg_x_margin = 5
svg_y_margin = 5

# scale of image, in pixels per unit value
svg_scale = 10

# width of lines, in pixels
line_weight = 2

# data type for integer values
type_sel = np.int32

# generate values according to definition
recam = np.empty(n_max, dtype=type_sel)
recam[0] = 0

for n in range(1, n_max):
    new_val = recam[n-1] - n
    if((new_val > 0) and not (new_val in recam[:n-1])):
        recam[n] = new_val
    else:
        recam[n] = recam[n-1] + n

# finding values to align and scale image
max_delta = np.ceil(np.max(np.abs(recam[:-1]-recam[1:]))/2)
max_val = np.max(recam[:])

svg_centerline = ((svg_scale*max_delta)+svg_y_margin).astype(type_sel)

svg_max_y = 2*svg_centerline
svg_max_x = (svg_scale*max_val+2*svg_x_margin).astype(type_sel)

# Writing out SVG image: single-line preface, then semicircles, then single-line termination
print("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"{0}\" height=\"{1}\">\n".format(svg_max_x, svg_max_y))

# semicircles generated using SVG path arc function
path_string = "<path d=\"M {0} {1} A {2} {2} 0 0 {3} {4} {1}\" stroke=\"black\" stroke-width=\"{5}\" fill=\"none\" />"

for i in range(1,n_max):
    start_x = svg_scale*recam[i-1]+svg_x_margin
    end_x = svg_scale*recam[i]+svg_x_margin
    radius = np.abs((start_x-end_x)/2).astype(type_sel)
    if(start_x < end_x):
        sweep_flag = (i+1)%2
    else:
        sweep_flag = (i)%2
    print(path_string.format(start_x, svg_centerline, radius,sweep_flag, end_x, line_weight))
    
print("\n</svg>")
