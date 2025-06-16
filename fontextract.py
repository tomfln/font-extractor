import os
import zipfile
import tempfile
import shutil
import argparse

# === FILE TYPE DEFINITIONS ===
web_extensions = ('.woff', '.woff2', '.eot', '.svg')
license_extensions = ('.txt',)

def safe_copy(src_path, dest_folder, check_existing=True):
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, os.path.basename(src_path))
    
    if check_existing and os.path.exists(dest_path):
        return False  # File already exists, didn't copy
    
    try:
        shutil.copy(src_path, dest_path)
        return True  # Successfully copied
    except Exception as e:
        print(f"Failed to copy {src_path} -> {dest_path}: {e}")
        return False

def extract_fonts_from_zip(zip_path, font_folder, prefer_ttf, include_web):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        font_files = []
        license_files = []
        web_files = []

        for root, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                lower = file.lower()
                if lower.endswith(('.ttf', '.otf')):
                    font_files.append(full_path)
                elif include_web and lower.endswith(web_extensions):
                    web_files.append(full_path)
                elif lower.endswith(license_extensions):
                    license_files.append(full_path)

        ttf_files = [f for f in font_files if f.lower().endswith('.ttf')]
        otf_files = [f for f in font_files if f.lower().endswith('.otf')]

        selected_fonts = ttf_files if prefer_ttf else otf_files
        if not selected_fonts:
            selected_fonts = otf_files if prefer_ttf else ttf_files

        if not selected_fonts and not (include_web and web_files):
            return 0, 0, False  # No font files found, skip this archive

        # Count copied vs already existing files
        copied_fonts = 0
        existing_fonts = 0
        
        for font_path in selected_fonts:
            if safe_copy(font_path, font_folder):
                copied_fonts += 1
            else:
                existing_fonts += 1

        for txt_path in license_files:
            safe_copy(txt_path, font_folder, check_existing=False)  # Always copy licenses

        copied_web = 0
        existing_web = 0
        if include_web:
            for web_path in web_files:
                web_folder = os.path.join(font_folder, 'web')
                if safe_copy(web_path, web_folder):
                    copied_web += 1
                else:
                    existing_web += 1

        total_copied = copied_fonts + copied_web
        total_existing = existing_fonts + existing_web
        family_has_new_files = total_copied > 0
        
        return total_copied, total_existing, family_has_new_files

def main():
    parser = argparse.ArgumentParser(
        description="Extract fonts from ZIP archives into structured folders."
    )
    parser.add_argument("input", help="Input folder containing .zip font archives")
    parser.add_argument("-o", "--output", default="out", help="Output folder (default: out)")
    parser.add_argument("--prefer-ttf", action="store_true", help="Prefer TTF files over OTF (default: prefer OTF)")
    parser.add_argument("--no-web", action="store_true", help="Do not extract web fonts (.woff, .woff2, etc.)")

    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(f"Error: Input folder '{args.input}' does not exist.")
        return    os.makedirs(args.output, exist_ok=True)

    font_family_count = 0
    font_file_count = 0
    existing_family_count = 0
    existing_file_count = 0

    for file_name in os.listdir(args.input):
        if file_name.lower().endswith('.zip'):
            zip_path = os.path.join(args.input, file_name)
            font_name = os.path.splitext(file_name)[0]
            font_folder = os.path.join(args.output, font_name)

            print(f"Processing {zip_path}...")
            copied, existing, has_new_files = extract_fonts_from_zip(
                zip_path,
                font_folder,
                args.prefer_ttf,
                not args.no_web
            )

            if copied > 0 or existing > 0:
                if has_new_files:
                    font_family_count += 1
                    font_file_count += copied
                    if existing > 0:
                        print(f"  -> Copied {copied} new files, {existing} already existed")
                    else:
                        print(f"  -> Copied {copied} files")
                else:
                    existing_family_count += 1
                    existing_file_count += existing
                    print(f"  -> All {existing} files already existed")

    print("\nFont extraction complete.")
    print(f"Extracted {font_file_count} font files from {font_family_count} font families.")
    if existing_file_count > 0:
        print(f"Found {existing_file_count} font files from {existing_family_count} font families already installed.")

if __name__ == "__main__":
    main()