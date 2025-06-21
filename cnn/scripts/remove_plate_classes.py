import os

# remove comment and add path to images and labels with .txt files
folder_path = "/Users/kresovic/Documents/Uni/Master/2.Semester/Bild/Model_test/data/labels"


for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        full_path = os.path.join(folder_path, filename)

        with open(full_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Filter out lines starting with a number > 0
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and stripped.split()[0].lstrip("-").isdigit():
                if int(stripped.split()[0]) <= 0:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Overwrite file with cleaned content
        with open(full_path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)
