from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog, Label, Button, Entry, StringVar, OptionMenu
from PIL import Image, ImageTk

class ImageScalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Tool - Scale / Flatten / Rotate Frames")

        self.mode = StringVar(value="scale")

        # Chọn chế độ
        tk.Label(root, text="Chọn chức năng:").pack()
        OptionMenu(root, self.mode, "scale", "flatten", "rotate_frames_90").pack()

        # Nhập kích thước
        self.width_entry = Entry(root)
        self.height_entry = Entry(root)
        self.frame_w_entry = Entry(root)
        self.frame_h_entry = Entry(root)

        Label(root, text="Chiều rộng (px):").pack()
        self.width_entry.pack()
        Label(root, text="Chiều cao (px):").pack()
        self.height_entry.pack()

        Label(root, text="Frame Width (flatten/rotate):").pack()
        self.frame_w_entry.pack()
        Label(root, text="Frame Height (flatten/rotate):").pack()
        self.frame_h_entry.pack()

        self.label = Label(root, text="📂 Kéo thả ảnh PNG vào đây", width=40, height=10, bg="#f0f0f0", relief="solid")
        self.label.pack(pady=10)
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)
        self.save_button = Button(root, text="💾 Lưu ảnh kết quả", command=self.save_image, state="disabled")
        self.save_button.pack(pady=10)
        self.img_preview = Label(root)
        self.img_preview.pack()



        self.scaled_image = None

    def drop(self, event):
        path = event.data.strip('{}')
        mode = self.mode.get()
        if mode == "scale":
            self.process_scale(path)
        elif mode == "flatten":
            self.process_flatten(path)
        elif mode == "rotate_frames_90":
            self.process_rotate_frames(path)

    def process_scale(self, path):
        img = Image.open(path)
        try:
            target_width = int(self.width_entry.get())
            target_height = int(self.height_entry.get())
        except:
            self.show_error("Kích thước không hợp lệ!")
            return

        self.scaled_image = img.resize((target_width, target_height), Image.NEAREST)
        preview = self.scaled_image.resize((target_width // 2, target_height // 2))
        self.show_preview(preview)

    def process_flatten(self, path):
        try:
            fw = int(self.frame_w_entry.get())
            fh = int(self.frame_h_entry.get())
        except:
            self.show_error("Kích thước frame không hợp lệ!")
            return

        img = Image.open(path)
        cols = img.width // fw
        rows = img.height // fh
        total_frames = cols * rows

        result_img = Image.new("RGBA", (fw * total_frames, fh))
        frame_index = 0

        for y in range(rows):
            for x in range(cols):
                box = (x * fw, y * fh, (x + 1) * fw, (y + 1) * fh)
                frame = img.crop(box)
                result_img.paste(frame, (frame_index * fw, 0))
                frame_index += 1

        self.scaled_image = result_img
        self.resize_and_show_preview(result_img)

    def process_rotate_frames(self, path):
        try:
            fw = int(self.frame_w_entry.get())
            fh = int(self.frame_h_entry.get())
        except:
            self.show_error("Kích thước frame không hợp lệ!")
            return

        img = Image.open(path)
        columns = img.width // fw
        rows = img.height // fh
        total_frames = columns * rows

        # Vì xoay nên width/height đổi chỗ
        rotated_w, rotated_h = fh, fw
        result_img = Image.new("RGBA", (rotated_w * total_frames, rotated_h))
        frame_index = 0

        for y in range(rows):
            for x in range(columns):
                box = (x * fw, y * fh, (x + 1) * fw, (y + 1) * fh)
                frame = img.crop(box)
                rotated = frame.rotate(-90, expand=True)
                result_img.paste(rotated, (frame_index * rotated_w, 0))
                frame_index += 1

        self.scaled_image = result_img
        self.resize_and_show_preview(result_img)

    def resize_and_show_preview(self, img):
        preview_width = min(400, img.width)
        preview_ratio = preview_width / img.width
        preview_height = max(1, int(img.height * preview_ratio))
        preview = img.resize((preview_width, preview_height))
        self.show_preview(preview)

    def show_preview(self, img):
        photo = ImageTk.PhotoImage(img)
        self.img_preview.configure(image=photo)
        self.img_preview.image = photo
        self.save_button.config(state="normal")

    def save_image(self):
        if self.scaled_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Images", "*.png")])
            if save_path:
                self.scaled_image.save(save_path)

    def show_error(self, msg):
        error = tk.Toplevel(self.root)
        error.title("Lỗi")
        Label(error, text=msg, fg="red").pack(padx=20, pady=10)
        Button(error, text="OK", command=error.destroy).pack(pady=5)

# Chạy ứng dụng
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageScalerApp(root)
    root.mainloop()
