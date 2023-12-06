from datetime import datetime

# Read data from the file
with open('extra_text.txt', 'r') as file:
    lines = file.readlines()

date_prefix_to_add = ''
output_lines = []

# Process the lines
for line in lines:
    elements = line.strip().split(' - ')

    # Check if the line is empty
    if line.strip():
        try:
            # Check if the first element is a date
            datetime.strptime(elements[0], '%m/%d/%Y %I:%M %p')
            date_prefix_to_add = elements[0]
            output_lines.append(line)
        except ValueError:
            # Append the line with date prefix if it exists, otherwise as is
            if date_prefix_to_add:
                output_lines.append(f"{date_prefix_to_add} - {line.strip()}")
            else:
                output_lines.append(line)

# Write modified data back to the file
with open('modified_extra_text.txt', 'w') as file:
    file.write('\n'.join(output_lines))

    # Open the file in read mode
with open('modified_extra_text.txt', 'r') as file:
    lines = file.readlines()  # Read all lines into a list

# Replace '-' with ',' for the first 5 occurrences in each line
modified_lines = []
for line in lines:
    modified_line = line.replace('-', ',', 8)  # Replace only the first 5 occurrences
    modified_lines.append(modified_line)

# Write the modified lines back to the file
with open('modified_extra_text.txt', 'w') as file:
    file.writelines(modified_lines)

