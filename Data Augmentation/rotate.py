from PIL import Image
import os


def create_labels(input_file, output_file, img_size):
    """
    Adjust bounding box labels for rotated images.

    Parameters:
        input_file (str): Path to the input YOLO label file.
        output_file (str): Path to save the updated YOLO label file.
        img_size (int): Size of the square image.
    """
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            data = line.strip().split()
            if len(data) != 5:
                print(f"Skipping invalid line: {line.strip()}")
                continue

            # Read label data
            label = data[0]
            x_center = round(float(data[1]) * img_size)
            y_center = round(float(data[2]) * img_size)
            width = round(float(data[3]) * img_size)
            height = round(float(data[4]) * img_size)

            # Calculate new values after rotation
            new_x = y_center / img_size
            new_y = (img_size - x_center) / img_size
            new_width = height / img_size
            new_height = width / img_size

            # Write updated labels to the output file
            outfile.write(
                f"{label} {new_x:.6f} {new_y:.6f} {new_width:.6f} {new_height:.6f}\n"
            )


# Directory for images
directory = "valid/images"

# Initialize counters
num_files = 0
num_rotated = 0

# Ensure output directory exists
os.makedirs("./Data Augmentation/Rotated_Images", exist_ok=True)
os.makedirs("./Data Augmentation/New_Labels", exist_ok=True)

# Process each image in the directory
for filename in os.scandir(directory):
    if filename.is_file() and filename.name.lower().endswith(".jpg"):
        num_files += 1

        # Load image
        img = Image.open(filename)

        # Extract base filename without extension
        short_name = os.path.basename(img.filename)
        actual_name = os.path.splitext(short_name)[0]

        # Create 3 rotations
        for i in range(1, 4):
            # Rotate image
            rotated_img = img.rotate(90)

            # Save rotated image
            rotated_img_path = f"./Data Augmentation/Rotated_Images/r{i}__{short_name}"
            rotated_img.save(rotated_img_path)

            # Increment rotated file counter
            num_rotated += 1

            # Update for next rotation
            img = rotated_img

        # Create new label files for each rotation
        for i in range(1, 4):
            if i == 1:
                input_file = f"valid/labels/{actual_name}.txt"
            else:
                input_file = f"Data Augmentation/New_Labels/r{i - 1}__{actual_name}.txt"

            output_file = f"Data Augmentation/New_Labels/r{i}__{actual_name}.txt"

            # Adjust labels for the rotation
            create_labels(input_file, output_file, 640)

# Print results
print("Total Image Files: ", num_files)
print("Total Rotated Images: ", num_rotated)
