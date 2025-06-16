
import os
import zipfile
import tempfile
import shutil

# === CONFIGURATION ===
input_folder = 'archives'  # Replace with your actual path
output_folder = 'out'   # Replace with your actual path
useTTFOverOTF = False  # Set to False to prefer OTF

# === SCRIPT START ===

def extract_fonts_from_zip(zip_path, output_folder):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        font_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith(('.ttf', '.otf')):
                    full_path = os.path.join(root, file)
                    font_files.append(full_path)

        # Classify by extension
        ttf_files = [f for f in font_files if f.lower().endswith('.ttf')]
        otf_files = [f for f in font_files if f.lower().endswith('.otf')]

        if useTTFOverOTF:
            selected_fonts = ttf_files or otf_files
        else:
            selected_fonts = otf_files or ttf_files

        for font_path in selected_fonts:
            try:
                shutil.copy(font_path, output_folder)
            except Exception as e:
                print(f"Failed to copy {font_path}: {e}")
        return len(selected_fonts)

def main():
    os.makedirs(output_folder, exist_ok=True)

    count = 0
    vcount = 0
    
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.zip'):
            zip_path = os.path.join(input_folder, file_name)
            print(f"Processing {zip_path}...")
            vcount += extract_fonts_from_zip(zip_path, output_folder)
            count += 1

    print("Font extraction complete.")
    print(f"Added {vcount} variants from {count} fonts")

if __name__ == "__main__":
    main()
