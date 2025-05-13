import numpy as np
from PIL import Image
import math
import os

class LSBSteganography:
    def __init__(self):
        self.zigzag_indices = None
    
    def _generate_zigzag_indices(self, width, height):
        """Generate zigzag scan pattern indices"""
        indices = []
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block_indices = []
                for k in range(8):
                    if k % 2 == 0:
                        # Left to right
                        block_indices.extend([(i + k, j + x) for x in range(8)])
                    else:
                        # Right to left
                        block_indices.extend([(i + k, j + x) for x in range(7, -1, -1)])
                indices.extend(block_indices)
        self.zigzag_indices = indices
    
    def _text_to_bits(self, text):
        """Convert text to binary string"""
        if isinstance(text, str):
            return ''.join(format(ord(i), '08b') for i in text)
        elif isinstance(text, bytes):
            return ''.join(format(i, '08b') for i in text)
        else:
            raise TypeError("Text must be string or bytes")
    
    def _bits_to_text(self, bits):
        """Convert binary string to text"""
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            chars.append(chr(int(byte, 2)))
        return ''.join(chars)
    
    def _calculate_psnr(self, original_img, stego_img):
        """Calculate PSNR between original and stego image"""
        mse = np.mean((original_img - stego_img) ** 2)
        if mse == 0:
            return float('inf')
        max_pixel = 255.0
        psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
        return psnr
    
    def _generate_key(self, img_array, message_bits):
        """Generate dynamic symmetric key as described in the paper"""
        key = []
        message_index = 0
        
        for i in range(len(self.zigzag_indices)):
            if message_index >= len(message_bits):
                break
                
            x, y = self.zigzag_indices[i]
            pixel = img_array[x, y]
            
            # Get LSB and next bit
            lsb = pixel & 1
            next_bit = (pixel >> 1) & 1
            
            msg_bit = int(message_bits[message_index])
            
            # Key generation rules from the paper
            if msg_bit == lsb:
                key_bit = 0
            elif msg_bit == next_bit:
                key_bit = 1
            else:
                key_bit = 0
                
            key.append(str(key_bit))
            message_index += 1
            
        return ''.join(key)
    
    def encode(self, image_path, message, output_path):
        """Encode message into image using LSB with dynamic key"""
        # Open image and convert to numpy array
        img = Image.open(image_path)
        # Convert to grayscale if it's a color image
        if img.mode != 'L':
            img = img.convert('L')
        img_array = np.array(img)
        
        # Generate zigzag pattern
        height, width = img_array.shape[:2]
        self._generate_zigzag_indices(width, height)
        
        # Convert message to binary
        message_bits = self._text_to_bits(message)
        message_len = len(message_bits)
        
        # Check if message fits in image
        max_bits = len(self.zigzag_indices)
        if message_len > max_bits:
            raise ValueError(f"Message too large for image. Max bits: {max_bits}, Message bits: {message_len}")
        
        # Generate dynamic key
        key = self._generate_key(img_array, message_bits)
        
        # Encode message using LSB
        stego_img = img_array.copy()
        message_index = 0
        
        for i in range(len(self.zigzag_indices)):
            if message_index >= message_len:
                break
                
            x, y = self.zigzag_indices[i]
            pixel = stego_img[x, y]
            
            # Modify LSB
            msg_bit = int(message_bits[message_index])
            stego_img[x, y] = (pixel & 0xFE) | msg_bit
            
            message_index += 1
        
        # Save stego image
        stego_image = Image.fromarray(stego_img)
        stego_image.save(output_path)
        
        # Calculate PSNR
        psnr = self._calculate_psnr(img_array, stego_img)
        print(f"PSNR: {psnr:.2f} dB")
        
        # Save key to file
        key_path = os.path.splitext(output_path)[0] + "_key.txt"
        with open(key_path, 'w') as f:
            f.write(key)
        
        return key
    
    def decode(self, stego_path, key_path):
        """Decode message from stego image using key"""
        # Open stego image
        stego_img = Image.open(stego_path)
        # Convert to grayscale if it's a color image
        if stego_img.mode != 'L':
            stego_img = stego_img.convert('L')
        stego_array = np.array(stego_img)
        
        # Generate zigzag pattern (must be same as encoding)
        width, height = stego_img.size
        self._generate_zigzag_indices(width, height)
        
        # Read key
        with open(key_path, 'r') as f:
            key = f.read().strip()
        
        # Decode message
        message_bits = []
        key_index = 0
        
        for i in range(len(self.zigzag_indices)):
            if key_index >= len(key):
                break
                
            x, y = self.zigzag_indices[i]
            pixel = stego_array[x, y]
            
            # Get LSB and next bit
            lsb = pixel & 1
            next_bit = (pixel >> 1) & 1
            
            key_bit = int(key[key_index])
            
            # Reconstruct message bit based on key
            if key_bit == 0:
                msg_bit = lsb
            else:
                msg_bit = next_bit
                
            message_bits.append(str(msg_bit))
            key_index += 1
        
        # Convert binary to text
        message = self._bits_to_text(''.join(message_bits))
        return message

# Example usage
if __name__ == "__main__":
    stego = LSBSteganography()
    
    # Encoding
    image_path = "flower.png"
    message = "This is a secret message!"
    output_path = "stego_image.png"
    
    print("Encoding message...")
    key = stego.encode(image_path, message, output_path)
    print(f"Generated key: {key[:50]}...")  # Print first 50 chars of key
    
    # Decoding
    print("\nDecoding message...")
    decoded_message = stego.decode(output_path, os.path.splitext(output_path)[0] + "_key.txt")
    print(f"Decoded message: {decoded_message}")