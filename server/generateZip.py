import os
import random

def generate_dummy_file(file_path, size_in_bytes):
    """Create a dummy file with the specified size."""
    with open(file_path, 'wb') as f:
        f.write(os.urandom(size_in_bytes))

def create_zip_files(file_sizes):
    """Generate ZIP files with specified sizes."""
    output_dir = "files"
    os.makedirs(output_dir, exist_ok=True)

    for i, file_size in enumerate(file_sizes):
        zip_filename = os.path.join(output_dir, f"File{i + 1}.zip")
        dummy_file = os.path.join(output_dir, f"dummy_{i + 1}.bin")

        # Calculate dummy file size to meet ZIP size requirement (small overhead for ZIP metadata)
        dummy_file_size = file_size - 1024  # Reserving 1 KB for ZIP overhead

        if dummy_file_size <= 0:
            raise ValueError(f"File size for file {i + 1} must be greater than 1 KB to account for ZIP overhead.")

        # Create a dummy file of the calculated size
        generate_dummy_file(dummy_file, dummy_file_size)

        # Create a ZIP file using system command
        os.system(f"zip -j {zip_filename} {dummy_file}")

        # Remove the dummy file after adding it to the ZIP
        os.remove(dummy_file)

        print(f"Generated {zip_filename} with size {file_size} bytes.")

if __name__ == "__main__":
    try:
        # User input for the sizes of ZIP files
        sizes_input = input("Enter the sizes of ZIP files (in bytes), separated by commas: ")
        file_sizes = [int(size.strip()) for size in sizes_input.split(",")]

        if any(size <= 0 for size in file_sizes):
            raise ValueError("All file sizes must be positive integers.")

        create_zip_files(file_sizes)
        print("All ZIP files generated successfully.")

    except Exception as e:
        print(f"Error: {e}")

#5242880,10485760,20971520