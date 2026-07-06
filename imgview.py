import customtkinter as ctk
from PIL import Image, ImageTk, UnidentifiedImageError
import os
from tkinter import filedialog, messagebox

try:
    import pillow_heif
except ImportError:
    print("Pillow-Heif not found. HEIF/HEIC support might be limited.")
    print("Install it using: pip install Pillow-Heif")

class ImageViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ImageViewer++")
        self.geometry("1000x700")
        self.minsize(600, 500)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.image_paths = []
        self.current_image_index = -1
        self.current_folder = None
        self.single_file_mode = False

        self.supported_extensions = (
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif",
            ".webp", ".ico", ".heic", ".heif", ".avif", ".jp2", ".jpx",
            ".psd", ".pcx", ".tga", ".exif", ".wmf", ".emf", ".dib",
            ".pbm", ".pgm", ".ppm", ".pnm", ".sgi", ".im", ".cur", ".xbm", ".xpm"
        )
        self.file_types = [("All Image Files", " ".join(["*" + ext for ext in self.supported_extensions]))]
        for ext in self.supported_extensions:
            self.file_types.append((f"{ext.upper().replace('.', '')} files", f"*{ext}"))
        self.file_types.append(("All files", "*.*"))


        self.control_frame = ctk.CTkFrame(self, corner_radius=10)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.open_folder_button = ctk.CTkButton(self.control_frame, text="Open Folder", command=self.open_folder)
        self.open_folder_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.open_file_button = ctk.CTkButton(self.control_frame, text="Open File", command=self.open_single_file)
        self.open_file_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.prev_button = ctk.CTkButton(self.control_frame, text="Previous", command=self.show_previous_image, state="disabled")
        self.prev_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.next_button = ctk.CTkButton(self.control_frame, text="Next", command=self.show_next_image, state="disabled")
        self.next_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.image_display_frame = ctk.CTkFrame(self, corner_radius=10)
        self.image_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.image_display_frame.grid_columnconfigure(0, weight=1)
        self.image_display_frame.grid_rowconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.image_display_frame, text="Open a file or folder to view images.")
        self.image_label.grid(row=0, column=0, sticky="nsew")

        self.status_bar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.status_bar_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.status_bar_frame.grid_columnconfigure(0, weight=1)

        self.file_path_label = ctk.CTkLabel(self.status_bar_frame, text="No file or folder selected", wraplength=800)
        self.file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.bind("<Configure>", self.on_resize)

    def reset_viewer_state(self):
        self.image_paths = []
        self.current_image_index = -1
        self.current_folder = None
        self.single_file_mode = False
        self.image_label.configure(image=None)
        self.image_label.configure(text="Open a file or folder to view images.")
        self.file_path_label.configure(text="No file or folder selected")
        self.prev_button.configure(state="disabled")
        self.next_button.configure(state="disabled")

    def open_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.reset_viewer_state()
            self.current_folder = selected_folder
            self.single_file_mode = False

            for filename in os.listdir(self.current_folder):
                file_path = os.path.join(self.current_folder, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(self.supported_extensions):
                    self.image_paths.append(file_path)

            self.image_paths.sort()

            if self.image_paths:
                self.current_image_index = 0
                self.load_and_display_image()
                self.prev_button.configure(state="normal")
                self.next_button.configure(state="normal")
            else:
                self.image_label.configure(text="No supported images found in this folder.")
                self.file_path_label.configure(text=f"Folder: {self.current_folder}")
                messagebox.showinfo("No Images", "No supported image files found in the selected folder.")
        else:
            if not self.image_paths:
                self.reset_viewer_state()


    def open_single_file(self):
        selected_file = filedialog.askopenfilename(filetypes=self.file_types)
        if selected_file:
            if not selected_file.lower().endswith(self.supported_extensions):
                messagebox.showerror("Unsupported File Type",
                                     f"The selected file '{os.path.basename(selected_file)}' is not a supported image format.")
                self.reset_viewer_state()
                return

            self.reset_viewer_state()
            self.image_paths = [selected_file]
            self.current_image_index = 0
            self.single_file_mode = True

            self.load_and_display_image()
            self.prev_button.configure(state="disabled")
            self.next_button.configure(state="disabled")
        else:
            if not self.image_paths:
                self.reset_viewer_state()

    def load_and_display_image(self):
        if not self.image_paths:
            self.image_label.configure(image=None)
            self.image_label.configure(text="No images to display.")
            self.file_path_label.configure(text="No file or folder selected")
            return

        image_path = self.image_paths[self.current_image_index]
        self.file_path_label.configure(text=f"Current file: {image_path}")

        try:
            pil_image = Image.open(image_path)
            self.display_image(pil_image)
        except UnidentifiedImageError:
            self.image_label.configure(image=None)
            self.image_label.configure(text=f"Could not open image: {os.path.basename(image_path)}\n(Unsupported format or corrupted file)")
            messagebox.showerror("Image Error", f"Could not open image: {os.path.basename(image_path)}\nIt might be an unsupported format or a corrupted file.")
            if not self.single_file_mode and len(self.image_paths) > 1:
                self.show_next_image()
            else:
                self.file_path_label.configure(text="Error loading image.")
                self.reset_viewer_state()
        except FileNotFoundError:
            self.image_label.configure(image=None)
            self.image_label.configure(text=f"File not found: {os.path.basename(image_path)}")
            messagebox.showerror("File Error", f"File not found: {os.path.basename(image_path)}. It might have been moved or deleted.")
            if not self.single_file_mode:
                self.image_paths.pop(self.current_image_index)
                if self.image_paths:
                    if self.current_image_index >= len(self.image_paths):
                        self.current_image_index = 0
                    self.load_and_display_image()
                else:
                    self.image_label.configure(text="No more images in this folder.")
                    self.reset_viewer_state()
            else:
                self.reset_viewer_state()
        except Exception as e:
            self.image_label.configure(image=None)
            self.image_label.configure(text=f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.reset_viewer_state()


    def display_image(self, pil_image):
        frame_width = self.image_display_frame.winfo_width()
        frame_height = self.image_display_frame.winfo_height()

        padding = 20
        max_width = max(1, frame_width - padding)
        max_height = max(1, frame_height - padding)

        img_width, img_height = pil_image.size

        if img_width > max_width or img_height > max_height:
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = pil_image

        ctk_image = ctk.CTkImage(light_image=resized_image,
                                 dark_image=resized_image,
                                 size=(resized_image.width, resized_image.height))

        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image

    def on_resize(self, event):
        if self.image_paths and self.current_image_index != -1 and event.widget == self:
            image_path = self.image_paths[self.current_image_index]
            try:
                pil_image = Image.open(image_path)
                self.display_image(pil_image)
            except (UnidentifiedImageError, FileNotFoundError, Exception) as e:
                print(f"Error during resize re-display: {e}")
                self.image_label.configure(image=None, text="Error re-displaying image.")
                self.reset_viewer_state()

    def show_next_image(self):
        if self.image_paths and not self.single_file_mode:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.load_and_display_image()

    def show_previous_image(self):
        if self.image_paths and not self.single_file_mode:
            self.current_image_index = (self.current_image_index - 1 + len(self.image_paths)) % len(self.image_paths)
            self.load_and_display_image()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ImageViewerApp()
    app.mainloop()
