import os

def move_files(source_dir, target_dir):
    if not os.path.exists(target_dir):
        print("Directory did not exist, so created it")
        os.makedirs(target_dir)

    count = 0
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)

        if os.path.isfile(source_path):
            os.rename(source_path, target_path)
        
        count += 1
    
    print("Total Files Moved: ", count)

if __name__ == "__main__":

    # Move labels
    move_files("Data Augmentation/ New_Labels", "train/labels")

    # Move Images
    move_files("Data Augmentation/Rotated_Images", "train/images")