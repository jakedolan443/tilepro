import tkinter as tk
from tkinter import Scrollbar, Frame, Menu

class TileMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tile Map Editor")
        self.root.geometry("1920x1080")
        self.root.resizable(False, False)  # Make window non-resizable

        # New color scheme
        self.bg_color = "#F0F0F0"  # Light grey background for the left frame and menus
        self.text_color = "#333333"  # Dark grey text color
        self.hover_bg_color = "#D6EAF8"  # Light blue for hover highlight
        self.selected_bg_color = "#5DADE2"  # Medium blue for selection highlight
        self.menubar_color = "#BDC3C7"  # Light grey for menubar
        self.canvas_bg_color = "#000000"  # Black background for the canvas area

        self.root.configure(bg=self.bg_color)

        # Define colors for each material
        self.colors = {
            0: ("white", "White"),
            1: ("grey", "Grey"),
            2: ("red", "Red"),
            3: ("green", "Green"),
            4: ("saddlebrown", "Brown"),  # wood
            5: ("blue", "Blue"),
            6: ("yellow", "Yellow"),
            7: ("purple", "Purple"),
            8: ("orange", "Orange"),
            9: ("black", "Black")
        }

        # Create menubar
        self.create_menubar()

        # Set up the start screen
        self.create_start_screen()

    def create_menubar(self):
        menubar = Menu(self.root, bg=self.menubar_color, fg=self.text_color)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0, bg=self.menubar_color, fg=self.text_color)
        tools_menu = Menu(menubar, tearoff=0, bg=self.menubar_color, fg=self.text_color)
        settings_menu = Menu(menubar, tearoff=0, bg=self.menubar_color, fg=self.text_color)
        help_menu = Menu(menubar, tearoff=0, bg=self.menubar_color, fg=self.text_color)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Add dummy items to menus for demonstration purposes
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        tools_menu.add_command(label="Tool 1")
        tools_menu.add_command(label="Tool 2")

        settings_menu.add_command(label="Setting 1")
        settings_menu.add_command(label="Setting 2")

        help_menu.add_command(label="Help")
        help_menu.add_command(label="About")

    def create_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg=self.bg_color)
        self.start_frame.pack(fill=tk.BOTH, expand=True)

        self.start_button = tk.Button(self.start_frame, text="Click to start", command=self.initialize_app, bg=self.bg_color, fg=self.text_color, font=("Arial", 16))
        self.start_button.pack(pady=20)

        self.width_label = tk.Label(self.start_frame, text="Map Width:", bg=self.bg_color, fg=self.text_color)
        self.width_label.pack()
        self.width_entry = tk.Entry(self.start_frame)
        self.width_entry.insert(0, "48")
        self.width_entry.pack()

        self.height_label = tk.Label(self.start_frame, text="Map Height:", bg=self.bg_color, fg=self.text_color)
        self.height_label.pack()
        self.height_entry = tk.Entry(self.start_frame)
        self.height_entry.insert(0, "48")
        self.height_entry.pack()

    def initialize_app(self):
        self.start_frame.pack_forget()

        self.map_width = int(self.width_entry.get())
        self.map_height = int(self.height_entry.get())

        self.tile_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]

        # Set up the left frame for the materials list with padding
        self.left_frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Add a canvas for scrolling if needed
        self.scrollbar = Scrollbar(self.left_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.material_canvas = tk.Canvas(self.left_frame, yscrollcommand=self.scrollbar.set, bg=self.bg_color, bd=0, highlightthickness=0)
        self.material_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.material_canvas.yview)

        self.create_material_list()

        # Set up the right frame for the canvas
        self.right_frame = tk.Frame(self.root, bg=self.canvas_bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(self.right_frame, bg=self.canvas_bg_color)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=self.canvas_bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind events on the canvas and resizing
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)  # Handle dragging
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        self.root.bind("<Configure>", self.on_resize)

        # Variable to store the current hover position
        self.hover_x = -1
        self.hover_y = -1

        # Variables to track drag start position and direction
        self.drag_start_x = None
        self.drag_start_y = None

        # Variable to store the selected item
        self.selected_item = None

        # Timer to control redraw rate
        self.redraw_required = False
        self.redraw_timer = self.root.after(16, self.draw_tile_map)

    def create_material_list(self):
        y_position = 10
        self.material_items = []
        for material_id in range(10):
            color, name = self.colors[material_id]

            frame = tk.Frame(self.material_canvas, bg=self.bg_color)

            swatch = tk.Label(
                frame,
                bg=color,
                width=2,
                height=1,
                relief="solid",
                borderwidth=1
            )
            swatch.pack(side=tk.LEFT, padx=(0, 5))

            material_label = tk.Label(
                frame,
                text=f"{name} (ID: {material_id})",
                bg=self.bg_color,
                fg=self.text_color,
                padx=10,
                pady=5,
                anchor="w",
                relief="flat",
                borderwidth=1,
                width=40
            )
            material_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            frame.bind("<Enter>", lambda e, l=material_label: self.on_material_hover(l))
            frame.bind("<Leave>", lambda e, l=material_label: self.on_material_leave(l))

            material_label.bind("<Button-1>", self.on_material_click)

            self.material_items.append((frame, material_id))
            self.material_canvas.create_window((10, y_position), window=frame, anchor="nw")

            y_position += 35
        self.material_canvas.config(scrollregion=self.material_canvas.bbox("all"))

    def on_material_hover(self, label):
        if self.selected_item is None or self.selected_item != [mat_id for frm, mat_id in self.material_items if frm == label.master][0]:
            label.config(bg=self.hover_bg_color)

    def on_material_leave(self, label):
        if self.selected_item is not None:
            if self.selected_item == [mat_id for frm, mat_id in self.material_items if frm == label.master][0]:
                label.config(bg=self.selected_bg_color)
            else:
                label.config(bg=self.bg_color)
        else:
            label.config(bg=self.bg_color)

    def on_material_click(self, event):
        clicked_label = event.widget
        selected_frame = clicked_label.master
        clicked_id = [mat_id for frame, mat_id in self.material_items if frame == selected_frame][0]

        # Deselect all items
        for frame, _ in self.material_items:
            text_label = frame.winfo_children()[1]
            if text_label == clicked_label:
                text_label.config(bg=self.selected_bg_color)
            else:
                text_label.config(bg=self.bg_color)

        # Update selected item
        self.selected_item = clicked_id

    def draw_tile_map(self):
        if self.redraw_required:
            self.canvas.delete("all")

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate the tile size
            tile_size_x = canvas_width / self.map_width
            tile_size_y = canvas_height / self.map_height
            self.tile_size = min(tile_size_x, tile_size_y)

            # Center the tile map
            offset_x = (canvas_width - self.map_width * self.tile_size) // 2
            offset_y = (canvas_height - self.map_height * self.tile_size) // 2

            for y in range(self.map_height):
                for x in range(self.map_width):
                    color = self.colors[self.tile_map[y][x]][0]
                    self.canvas.create_rectangle(
                        offset_x + x * self.tile_size, offset_y + y * self.tile_size,
                        offset_x + (x + 1) * self.tile_size, offset_y + (y + 1) * self.tile_size,
                        fill=color, outline="grey"
                    )
            self.draw_hover_preview()
            self.redraw_required = False

        self.redraw_timer = self.root.after(16, self.draw_tile_map)

    def draw_hover_preview(self):
        if self.hover_x >= 0 and self.hover_y >= 0:
            selected_item = getattr(self, "selected_item", None)
            if selected_item is not None:
                color = self.colors[selected_item][0]
                offset_x = (self.canvas.winfo_width() - self.map_width * self.tile_size) // 2
                offset_y = (self.canvas.winfo_height() - self.map_height * self.tile_size) // 2
                self.canvas.create_rectangle(
                    offset_x + self.hover_x * self.tile_size, offset_y + self.hover_y * self.tile_size,
                    offset_x + (self.hover_x + 1) * self.tile_size, offset_y + (self.hover_y + 1) * self.tile_size,
                    fill=color, outline="black", stipple="gray75"
                )

    def on_canvas_click(self, event):
        selected_item = getattr(self, "selected_item", None)
        if selected_item is None:
            return

        x = int((event.x - (self.canvas.winfo_width() - self.map_width * self.tile_size) // 2) // self.tile_size)
        y = int((event.y - (self.canvas.winfo_height() - self.map_height * self.tile_size) // 2) // self.tile_size)

        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.tile_map[y][x] = selected_item
            self.redraw_required = True

            # Set the drag start position
            self.drag_start_x = x
            self.drag_start_y = y

    def on_canvas_drag(self, event):
        if self.drag_start_x is None or self.drag_start_y is None:
            return

        x = int((event.x - (self.canvas.winfo_width() - self.map_width * self.tile_size) // 2) // self.tile_size)
        y = int((event.y - (self.canvas.winfo_height() - self.map_height * self.tile_size) // 2) // self.tile_size)

        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            if x == self.drag_start_x:
                # Dragging vertically
                start_y = min(self.drag_start_y, y)
                end_y = max(self.drag_start_y, y)
                for j in range(start_y, end_y + 1):
                    self.tile_map[j][x] = self.selected_item
            elif y == self.drag_start_y:
                # Dragging horizontally
                start_x = min(self.drag_start_x, x)
                end_x = max(self.drag_start_x, x)
                for i in range(start_x, end_x + 1):
                    self.tile_map[y][i] = self.selected_item
            self.redraw_required = True

    def on_canvas_hover(self, event):
        x = int((event.x - (self.canvas.winfo_width() - self.map_width * self.tile_size) // 2) // self.tile_size)
        y = int((event.y - (self.canvas.winfo_height() - self.map_height * self.tile_size) // 2) // self.tile_size)

        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            if x != self.hover_x or y != self.hover_y:
                self.hover_x = x
                self.hover_y = y
                self.redraw_required = True
        else:
            if self.hover_x != -1 or self.hover_y != -1:
                self.hover_x = -1
                self.hover_y = -1
                self.redraw_required = True

    def on_resize(self, event):
        self.redraw_required = True

if __name__ == "__main__":
    root = tk.Tk()
    app = TileMapApp(root)
    root.mainloop()
