#!/usr/bin/env python3
"""
Universe of Legends TCG - Image Optimizer & WebP Converter
Reduces high-resolution print card images (3-5 MB) to lightweight web assets (~60-150 KB)
while preserving sharp text and artwork quality.

Requirements:
  pip install Pillow
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Error: The 'Pillow' library is not installed.")
    print("Please install it by running:")
    print("    pip install Pillow")
    sys.exit(1)

def optimize_images(input_dir='Card_Images', output_dir='Card_Images_Optimized', max_width=600, quality=82):
    if not os.path.exists(input_dir):
        print(f"Error: Folder '{input_dir}' was not found in the current directory.")
        print(f"Make sure to run this script in the folder containing your '{input_dir}' directory.")
        return

    os.makedirs(output_dir, exist_ok=True)

    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]

    if not files:
        print(f"No image files found in '{input_dir}'.")
        return

    print(f"=== Starting Optimization for {len(files)} Card Images ===")
    print(f"Source Folder:  {input_dir}")
    print(f"Target Folder:  {output_dir}")
    print(f"Max Width:      {max_width}px (proportional scale)")
    print(f"Format:         WebP (Quality {quality}%)\n")

    total_orig_bytes = 0
    total_new_bytes = 0
    success_count = 0

    for i, filename in enumerate(files, 1):
        src_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        dst_filename = base_name + '.webp'
        dst_path = os.path.join(output_dir, dst_filename)

        orig_size = os.path.getsize(src_path)
        total_orig_bytes += orig_size

        try:
            with Image.open(src_path) as img:
                # Convert RGBA to RGB if needed, preserving alpha for transparency
                has_alpha = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)

                # Resize if larger than max_width
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # Save as WebP
                img.save(dst_path, 'WEBP', quality=quality, method=6, lossless=False)

            new_size = os.path.getsize(dst_path)
            total_new_bytes += new_size
            success_count += 1

            orig_mb = orig_size / (1024 * 1024)
            new_kb = new_size / 1024
            savings = (1 - (new_size / orig_size)) * 100 if orig_size > 0 else 0

            print(f"[{i}/{len(files)}] {filename} ({orig_mb:.2f} MB) -> {dst_filename} ({new_kb:.0f} KB) [-{savings:.0f}%]")

        except Exception as e:
            print(f"[{i}/{len(files)}] Error processing {filename}: {e}")

    orig_total_mb = total_orig_bytes / (1024 * 1024)
    new_total_mb = total_new_bytes / (1024 * 1024)
    total_savings = (1 - (total_new_bytes / total_orig_bytes)) * 100 if total_orig_bytes > 0 else 0

    print("\n=== Optimization Complete! ===")
    print(f"Cards Processed: {success_count} / {len(files)}")
    print(f"Total Size Before: {orig_total_mb:.1f} MB")
    print(f"Total Size After:  {new_total_mb:.1f} MB (Saved {total_savings:.1f}%)")
    print(f"\nYour optimized cards are in the '{output_dir}' folder.")

if __name__ == '__main__':
    in_dir = sys.argv[1] if len(sys.argv) > 1 else 'Card_Images'
    out_dir = sys.argv[2] if len(sys.argv) > 2 else 'Card_Images_Optimized'
    optimize_images(in_dir, out_dir)
