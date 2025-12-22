from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

class ImageScalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scaler - Kéo ảnh PNG vào")

        self.label = Label(root, text="📂 Kéo thả ảnh PNG vào đây", width=40, height=10, bg="#f0f0f0", relief="solid")
        self.label.pack(pady=10)
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)

        self.img_preview = Label(root)
        self.img_preview.pack()

        self.save_button = Button(root, text="💾 Lưu ảnh đã scale", command=self.save_image, state="disabled")
        self.save_button.pack(pady=10)

        self.scaled_image = None

    def drop(self, event):
        path = event.data.strip('{}')
        self.process_image(path)

    def process_image(self, path):
        img = Image.open(path)
        target_height = 100
        scale_ratio = target_height / img.height
        target_width = int(img.width * scale_ratio)
        self.scaled_image = img.resize((target_width, target_height), Image.NEAREST)

        preview = self.scaled_image.resize((target_width//2, target_height//2))
        photo = ImageTk.PhotoImage(preview)
        self.img_preview.configure(image=photo)
        self.img_preview.image = photo

        self.save_button.config(state="normal")

    def save_image(self):
        if self.scaled_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Images", "*.png")])
            if save_path:
                self.scaled_image.save(save_path)

# Chạy ứng dụng
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageScalerApp(root)
    root.mainloop()
