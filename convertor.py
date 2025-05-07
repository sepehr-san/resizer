import os
from PIL import Image

TARGET_SIZE = (1024, 576)


def convert_to_png(image_path):
    # Clean up the input path
    image_path = image_path.strip().strip('"')

    # Debug info
    print(f"Input path: {image_path}")
    print("Exists:", os.path.isfile(image_path))

    # Check existence
    if not os.path.isfile(image_path):
        print("❌ File not found.")
        return

    # Validate extension
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        print("❌ Unsupported file type. Please use JPG or PNG.")
        return

    try:
        with Image.open(image_path) as img:
            orig_w, orig_h = img.size
            target_w, target_h = TARGET_SIZE

            # Calculate scale to cover the target area (scale up until it fits)
            scale = max(target_w / orig_w, target_h / orig_h)
            new_size = (int(orig_w * scale), int(orig_h * scale))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

            # Center-crop to exact target size
            left = (new_size[0] - target_w) / 2
            top = (new_size[1] - target_h) / 2
            right = left + target_w
            bottom = top + target_h
            img_cropped = img_resized.crop((left, top, right, bottom))

            # Prepare output filename and save as PNG (lossless)
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(os.getcwd(), f"{base_name}.webp")
            img_cropped.save(output_path, format="WEBP", quality=100)

        print(f"✅ Converted and saved as: {output_path}")

    except Exception as e:
        print(f"❌ Error during conversion: {e}")


if __name__ == "__main__":
    print(f"👉 Drag and drop a JPG or PNG file here and press Enter:")
    input_path = input()
    convert_to_png(input_path)
