import os

# Specify the directory path (you can change this or take user input)
directory = input("Enter the directory path: ")

# Check if the directory exists
if os.path.exists(directory):
    print(f"\nContents of directory '{directory}':\n")
    
    # List all files and directories
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print(f"[DIR]  {item}")
        else:
            print(f"      {item}")
else:
    print("The specified directory does not exist.")
