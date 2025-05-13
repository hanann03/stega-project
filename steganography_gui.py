import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

# Silence the Tk deprecation warning on macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

from LSBSteganography import LSBSteganography

class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LSB Steganography Tool")
        self.root.geometry("900x700")
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a90e2"
        self.root.configure(bg=self.bg_color)
        
        # Initialize steganography object
        self.stego = LSBSteganography()
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create notebook for tabs
        style = ttk.Style()
        style.configure("TNotebook", background=self.bg_color)
        style.configure("TNotebook.Tab", padding=[10, 5], font=('Helvetica', 10))
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create encode and decode tabs
        self.encode_frame = ttk.Frame(self.notebook, padding="20")
        self.decode_frame = ttk.Frame(self.notebook, padding="20")
        
        self.notebook.add(self.encode_frame, text="Encode Message")
        self.notebook.add(self.decode_frame, text="Decode Message")
        
        self.setup_encode_tab()
        self.setup_decode_tab()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def setup_encode_tab(self):
        # Title
        title_label = ttk.Label(self.encode_frame, text="Hide a Message in an Image", font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Image selection
        ttk.Label(self.encode_frame, text="Select Cover Image:", font=('Helvetica', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.encode_image_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.encode_image_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(self.encode_frame, text="Browse", command=self.browse_encode_image).grid(row=1, column=2)
        
        # Message input
        ttk.Label(self.encode_frame, text="Enter Message:", font=('Helvetica', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.message_text = tk.Text(self.encode_frame, height=5, width=50, font=('Helvetica', 10))
        self.message_text.grid(row=2, column=1, columnspan=2, pady=5)
        
        # Output path
        ttk.Label(self.encode_frame, text="Output Path:", font=('Helvetica', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.encode_output_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.encode_output_path, width=50).grid(row=3, column=1, padx=5)
        ttk.Button(self.encode_frame, text="Browse", command=self.browse_encode_output).grid(row=3, column=2)
        
        # Encode button
        encode_button = ttk.Button(self.encode_frame, text="Encode Message", command=self.encode_message)
        encode_button.grid(row=4, column=1, pady=20)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self.encode_frame, text="Image Preview", padding="10")
        self.preview_frame.grid(row=5, column=0, columnspan=3, pady=10)
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.grid(row=0, column=0)

    def setup_decode_tab(self):
        # Title
        title_label = ttk.Label(self.decode_frame, text="Extract Hidden Message", font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Stego image selection
        ttk.Label(self.decode_frame, text="Select Stego Image:", font=('Helvetica', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.decode_image_path = tk.StringVar()
        ttk.Entry(self.decode_frame, textvariable=self.decode_image_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(self.decode_frame, text="Browse", command=self.browse_decode_image).grid(row=1, column=2)
        
        # Key file selection
        ttk.Label(self.decode_frame, text="Select Key File:", font=('Helvetica', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.key_path = tk.StringVar()
        ttk.Entry(self.decode_frame, textvariable=self.key_path, width=50).grid(row=2, column=1, padx=5)
        ttk.Button(self.decode_frame, text="Browse", command=self.browse_key_file).grid(row=2, column=2)
        
        # Decode button
        decode_button = ttk.Button(self.decode_frame, text="Decode Message", command=self.decode_message)
        decode_button.grid(row=3, column=1, pady=20)
        
        # Decoded message display
        ttk.Label(self.decode_frame, text="Decoded Message:", font=('Helvetica', 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.decoded_text = tk.Text(self.decode_frame, height=5, width=50, font=('Helvetica', 10))
        self.decoded_text.grid(row=4, column=1, columnspan=2, pady=5)
        
        # Preview frame
        self.decode_preview_frame = ttk.LabelFrame(self.decode_frame, text="Image Preview", padding="10")
        self.decode_preview_frame.grid(row=5, column=0, columnspan=3, pady=10)
        self.decode_preview_label = ttk.Label(self.decode_preview_frame)
        self.decode_preview_label.grid(row=0, column=0)

    def browse_encode_image(self):
        filename = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filename:
            self.encode_image_path.set(filename)
            self.show_preview(filename, self.preview_label)

    def browse_encode_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Stego Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if filename:
            self.encode_output_path.set(filename)

    def browse_decode_image(self):
        filename = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("Image files", "*.png")]
        )
        if filename:
            self.decode_image_path.set(filename)
            self.show_preview(filename, self.decode_preview_label)

    def browse_key_file(self):
        filename = filedialog.askopenfilename(
            title="Select Key File",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            self.key_path.set(filename)

    def show_preview(self, image_path, label, max_size=(300, 300)):
        try:
            image = Image.open(image_path)
            image.thumbnail(max_size)
            photo = ImageTk.PhotoImage(image)
            label.configure(image=photo)
            label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image preview: {str(e)}")

    def encode_message(self):
        try:
            image_path = self.encode_image_path.get()
            message = self.message_text.get("1.0", tk.END).strip()
            output_path = self.encode_output_path.get()
            
            if not all([image_path, message, output_path]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            key = self.stego.encode(image_path, message, output_path)
            messagebox.showinfo("Success", 
                              f"Message encoded successfully!\n\n"
                              f"Stego image saved to:\n{output_path}\n\n"
                              f"Key saved to:\n{output_path[:-4]}_key.txt")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")

    def decode_message(self):
        try:
            stego_path = self.decode_image_path.get()
            key_path = self.key_path.get()
            
            if not all([stego_path, key_path]):
                messagebox.showerror("Error", "Please select both stego image and key file")
                return
            
            decoded_message = self.stego.decode(stego_path, key_path)
            self.decoded_text.delete("1.0", tk.END)
            self.decoded_text.insert("1.0", decoded_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop() 