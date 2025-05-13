# LSB Steganography Tool

A GUI application for hiding and extracting messages in images using LSB (Least Significant Bit) steganography.

## Features

- Hide messages in images using LSB steganography
- Extract hidden messages using a key file
- User-friendly GUI interface
- Support for various image formats (PNG, JPG, JPEG, BMP, GIF)
- Image preview functionality
- Dynamic key generation for enhanced security

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python steganography_gui.py
```

2. To hide a message:
   - Click on the "Encode Message" tab
   - Select a cover image
   - Enter your secret message
   - Choose an output path
   - Click "Encode Message"
   - Save the generated key file securely

3. To extract a message:
   - Click on the "Decode Message" tab
   - Select the stego image
   - Select the key file
   - Click "Decode Message"
   - View the extracted message

## Requirements

- Python 3.x
- numpy
- Pillow (PIL)
- tkinter (usually comes with Python)

## Security Note

Always keep your key files secure. Without the key file, the hidden message cannot be extracted from the stego image.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 