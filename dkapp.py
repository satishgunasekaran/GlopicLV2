import time
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from night_images import illuminate
from PIL import Image, ImageTk

illum = illuminate()

class ImageEnhancementTool(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Image Enhancement Tool")

        # Create the heading label
        self.heading_label = tk.Label(self.master, text="Image Enhancement Tool", font=("Helvetica", 24))
        self.heading_label.pack(pady=20)

        # Create a frame for the buttons and labels
        frame = tk.Frame(self.master)
        frame.pack(padx=20, pady=20)

        # Create an empty label for column 0
        empty_label_left = tk.Label(frame)
        empty_label_left.grid(row=0, column=0, padx=20, pady=20)

        # Create the input button
        self.input_button = tk.Button(frame, text="Upload Image", command=self.upload_image, bg="#4CAF50", fg="white", font=("Helvetica", 12), width=20)
        self.input_button.grid(row=0, column=1, padx=20, pady=20)

        # Create an empty label for column 2
        empty_label_right = tk.Label(frame)
        empty_label_right.grid(row=0, column=2, padx=20, pady=20)

        # Create the two image labels and titles
        self.original_image_label = tk.Label(frame)
        self.original_image_label.grid(row=1, column=0, padx=20, pady=20, columnspan=1)
        self.original_image_title = tk.Label(frame, text="")
        self.original_image_title.grid(row=2, column=0)

        self.enhanced_image_label = tk.Label(frame)
        self.enhanced_image_label.grid(row=1, column=2, padx=20, pady=20, columnspan=1)
        self.enhanced_image_title = tk.Label(frame, text="")
        self.enhanced_image_title.grid(row=2, column=2)
        
        
        # Create the download button for the enhanced image
        self.download_button = tk.Button(frame, text="Download", command=self.download_enhanced_image, bg="#4CAF50", fg="white", font=("Helvetica", 12), width=25)
        self.download_button.grid(row=3, column=2, padx=20, pady=20)
        self.download_button.config(state=tk.DISABLED)
        self.download_button.grid_remove()
        # hide the download button


    
    def download_enhanced_image(self):
        # Get the enhanced image and save it to a file
        enhanced_image = self.enhanced_image_label.image
        if enhanced_image:
            filename = filedialog.asksaveasfilename(defaultextension=".png")
            pil_image = ImageTk.getimage(enhanced_image)  # Convert PhotoImage to PIL Image
            pil_image.save(filename)

                                
    def upload_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename()

        # Load the image and display it in the original image label
        original_image = Image.open(file_path)
        original_image = original_image.resize((300, 300), Image.ANTIALIAS)
        original_image_tk = ImageTk.PhotoImage(original_image)
        self.original_image_label.config(image=original_image_tk)
        self.original_image_label.image = original_image_tk
        self.original_image_title.config(text=" Original Image")

        # Call a function to update the enhanced image after a delay of 5 seconds
        self.input_button.config(state=tk.DISABLED)
        self.master.title("Image Enhancement Tool - Processing")
        self.heading_label = tk.Label(self.master, text="Image Enhancement Tool - Processing", font=("Helvetica", 24))
        self.download_button.grid_remove()
        
        self.master.after(1000, lambda: self.update_enhanced_image(original_image))

    def update_enhanced_image(self, original_image):
        # Perform image enhancement and display the enhanced image in the enhanced image label
        # Replace the following code with your own image enhancement code
        enhanced_image = illum.starter(original_image)
        enhanced_image_tk = ImageTk.PhotoImage(enhanced_image)
        self.enhanced_image_label.config(image=enhanced_image_tk)
        self.enhanced_image_label.image = enhanced_image_tk
        self.enhanced_image_title.config(text=" Enhanced Image")
        self.download_button.grid(row=3, column=2, padx=20, pady=20)
        self.download_button.config(state=tk.NORMAL)
        
        self.input_button.config(state=tk.NORMAL)
        self.master.title("Image Enhancement Tool")

        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    app = ImageEnhancementTool(master=root)
    app.mainloop()
