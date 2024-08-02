colors = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]

# Function to print solid line with given color code and its hex
def print_solid_line_with_hex(color_code):
    # ANSI escape sequence to set background color
    color_escape = "\033[48;2;{};{};{}m".format(
        int(color_code[1:3], 16), int(color_code[3:5], 16), int(color_code[5:7], 16))
    # Solid line with colored background
    solid_line = " " * 20
    print(color_escape + solid_line + "\033[0m")

# Print solid line for each color code with its hex code
for color_code in colors:
    print_solid_line_with_hex(color_code)

