def replace_tabs_with_spaces(file_path, spaces=4):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            # Replace tabs with the correct number of spaces
            new_line = ""
            for char in line:
                if char == '\t':
                    # Calculate the number of spaces needed to reach the next tab stop
                    new_line += ' ' * (spaces - len(new_line) % spaces)
                else:
                    new_line += char
            new_lines.append(new_line)

        with open(file_path, 'w') as file:
            file.writelines(new_lines)
            
        print(f"Successfully converted tabs to spaces in {file_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.py' with the path to your Python file

replace_tabs_with_spaces('include/Canvas.py', spaces=4)

