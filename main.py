#!/usr/bin/env python3
"""
Kannada OCR Script using Tesseract and Pillow
This script reads Kannada text from images and displays the output.
"""

import pytesseract
from PIL import Image, ImageEnhance
import os
import sys
import argparse


def check_tesseract_installation():
    """Check if Tesseract is properly installed and Kannada language is available."""
    try:
        # Check if tesseract is available
        available_languages = pytesseract.get_languages()
        
        print("✅ Tesseract is installed successfully!")
        print(f"Available languages: {', '.join(available_languages)}")
        
        if 'kan' in available_languages:
            print("✅ Kannada language pack is available!")
            return True
        else:
            print("❌ Kannada language pack is not installed.")
            print("Please install Kannada language pack for Tesseract.")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Tesseract installation: {str(e)}")
        print("Please make sure Tesseract is installed and in your PATH.")
        return False


def preprocess_image(image, enhance_contrast=True, convert_grayscale=True):
    """
    Preprocess image for better OCR results.
    
    Args:
        image (PIL.Image): Input image
        enhance_contrast (bool): Whether to enhance contrast
        convert_grayscale (bool): Whether to convert to grayscale
    
    Returns:
        PIL.Image: Preprocessed image
    """
    processed_image = image.copy()
    
    if convert_grayscale:
        processed_image = processed_image.convert('L')
        print("📝 Converted image to grayscale")
    
    if enhance_contrast:
        enhancer = ImageEnhance.Contrast(processed_image)
        processed_image = enhancer.enhance(2.0)
        print("📝 Enhanced image contrast")
    
    return processed_image


def extract_kannada_text(image_path, preprocess=True, show_image_info=True):
    """
    Extract Kannada text from an image file.
    
    Args:
        image_path (str): Path to the image file
        preprocess (bool): Whether to apply image preprocessing
        show_image_info (bool): Whether to display image information
    
    Returns:
        str: Extracted text from the image
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return f"❌ Error: Image file '{image_path}' not found."
        
        # Open the image
        print(f"📂 Opening image: {image_path}")
        image = Image.open(image_path)
        
        # Display image information
        if show_image_info:
            print(f"📊 Image Information:")
            print(f"   Size: {image.size}")
            print(f"   Mode: {image.mode}")
            print(f"   Format: {image.format}")
        
        # Preprocess image if requested
        if preprocess:
            print("🔧 Preprocessing image...")
            image = preprocess_image(image)
        
        # OCR configuration for better results
        custom_config = r'--oem 3 --psm 6'
        
        print("🔍 Extracting text using OCR...")
        
        # Extract text using both Kannada and English for better mixed content support
        extracted_text = pytesseract.image_to_string(
            image, 
            lang='kan',
            config=custom_config
        )
        
        return extracted_text
        
    except Exception as e:
        return f"❌ Error processing image: {str(e)}"


def save_text_to_file(text, image_path, output_dir=None):
    """
    Save extracted text to a .txt file.

    Args:
        text (str): Extracted text to save
        image_path (str): Path to the original image
        output_dir (str): Directory to save the text file (optional)

    Returns:
        str: Path to the saved text file
    """
    # Generate output filename based on image name
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_filename = f"{image_name}_extracted_text.txt"

    # Determine output directory
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
    else:
        # Save in the same directory as the image
        image_dir = os.path.dirname(image_path) or '.'
        output_path = os.path.join(image_dir, output_filename)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header with metadata
            f.write(f"Extracted Text from: {os.path.basename(image_path)}\n")
            f.write(f"Processing Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Character Count: {len(text)}\n")
            f.write(f"Word Count: {len(text.split())}\n")
            f.write(f"Line Count: {len(text.splitlines())}\n")
            f.write("=" * 50 + "\n\n")

            # Write the extracted text
            f.write(text)

        return output_path
    except Exception as e:
        print(f"❌ Error saving text file: {str(e)}")
        return None


def display_results(text, image_path, save_output=False, output_dir=None):
    """
    Display the OCR results in a formatted way and optionally save to file.

    Args:
        text (str): Extracted text
        image_path (str): Path to the processed image
        save_output (bool): Whether to save text to file
        output_dir (str): Directory to save the text file
    """
    print("\n" + "="*60)
    print(f"📋 OCR RESULTS FOR: {os.path.basename(image_path)}")
    print("="*60)

    if text.strip():
        print("📝 Extracted Text:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        print(f"📊 Character count: {len(text)}")
        print(f"📊 Word count: {len(text.split())}")
        print(f"📊 Line count: {len(text.splitlines())}")

        # Save to file if requested
        if save_output:
            output_path = save_text_to_file(text, image_path, output_dir)
            if output_path:
                print(f"💾 Text saved to: {output_path}")

    else:
        print("⚠️  No text was extracted from the image.")
        print("💡 Tips to improve results:")
        print("   - Ensure the image has good contrast")
        print("   - Make sure the text is clearly visible")
        print("   - Try with a higher resolution image")
        print("   - Check if the text is properly oriented")


def process_multiple_images(folder_path, save_output=False, output_dir=None):
    """
    Process all images in a folder.

    Args:
        folder_path (str): Path to folder containing images
        save_output (bool): Whether to save text to files
        output_dir (str): Directory to save the text files
    """
    supported_formats = ('.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif')

    if not os.path.exists(folder_path):
        print(f"❌ Folder '{folder_path}' not found.")
        return

    image_files = [f for f in os.listdir(folder_path)
                   if f.lower().endswith(supported_formats)]

    if not image_files:
        print(f"❌ No image files found in '{folder_path}'")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return

    print(f"📁 Found {len(image_files)} image file(s) in '{folder_path}'")

    for i, image_file in enumerate(image_files, 1):
        print(f"\n🔄 Processing image {i}/{len(image_files)}: {image_file}")
        image_path = os.path.join(folder_path, image_file)

        extracted_text = extract_kannada_text(image_path, preprocess=True, show_image_info=False)
        display_results(extracted_text, image_path, save_output, output_dir)


def main():
    """Main function to handle command line arguments and execute OCR."""
    parser = argparse.ArgumentParser(
        description="Extract Kannada text from images using OCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py image.jpg                           # Process single image
  python main.py image.jpg --save                    # Process and save text to file
  python main.py --folder ./images --save            # Process folder and save all texts
  python main.py image.png --save --output ./texts   # Save to specific directory
  python main.py image.png --no-preprocess           # Process without preprocessing
  python main.py --check                             # Check Tesseract installation
        """
    )

    parser.add_argument('path', nargs='?', help='Path to image file or folder')
    parser.add_argument('--folder', action='store_true',
                       help='Process all images in the specified folder')
    parser.add_argument('--no-preprocess', action='store_true',
                       help='Skip image preprocessing')
    parser.add_argument('--save', action='store_true',
                       help='Save extracted text to .txt files')
    parser.add_argument('--output', type=str, metavar='DIR',
                       help='Directory to save text files (default: same as image location)')
    parser.add_argument('--check', action='store_true',
                       help='Check Tesseract installation and language support')

    args = parser.parse_args()
    
    print("🚀 Kannada OCR Script")
    print("=" * 30)
    
    # Check installation if requested
    if args.check:
        check_tesseract_installation()
        return
    
    # Check if path is provided
    if not args.path:
        print("❌ Please provide an image path or folder path.")
        print("Use --help for usage information.")
        return
    
    # Check Tesseract installation
    if not check_tesseract_installation():
        return
    
    print()  # Add spacing
    
    # Validate output directory if specified
    if args.output and not args.save:
        print("⚠️  --output can only be used with --save option")
        return

    # Process folder or single image
    if args.folder:
        process_multiple_images(args.path, save_output=args.save, output_dir=args.output)
    else:
        # Process single image
        preprocess = not args.no_preprocess
        extracted_text = extract_kannada_text(args.path, preprocess=preprocess)
        display_results(extracted_text, args.path, save_output=args.save, output_dir=args.output)

    print("\n✅ Processing completed!")


if __name__ == "__main__":
    main()
