# Define the colors dictionary
colors = {'dy': "#5790fc", 'dynlo': "#f89c20", 'qcd': "#e42536", 'top': "#964a8b", 'ew': "#9c9ca1", 'ewknlo': "#7a21dd"}

# Function to print solid line with given color code and its hex
def print_solid_line_with_hex(color_name, color_code):
    # ANSI escape sequence to set background color


    color_escape = "\033[48;2;{};{};{}m".format(
        int(color_code[1:3], 16), int(color_code[3:5], 16), int(color_code[5:7], 16))
    # Solid line with colored background
    solid_line = " " * 20
    print(color_escape + solid_line + "\033[0m")


# Print solid line for each color code with its hex code
for color_name, color_code in colors.items():
    print_solid_line_with_hex(color_name, color_code)


