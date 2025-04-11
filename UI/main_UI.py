import os
import sys

# Add project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from menu import Menu
from result import Result


class Main(ctk.CTk):
	def __init__(self, *args, **kwargs):
		ctk.CTk.__init__(self, *args, **kwargs)

		self.title("Social network analysis")
		self.center_window(700, 600)

		# Configure the appearance
		ctk.set_appearance_mode("dark") # Options: "dark", "light"
		ctk.set_default_color_theme("dark-blue") # Options: "blue", "green", "dark-blue"

		# Create a container for frames
		container = ctk.CTkFrame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# Initialize variables
		self.social_network = None
		self.file_path = None
		self.strategy = None
		self.effort = None
		self.conflict = None

		# Dictionary to store frames
		self.frames = {}

		# Initialize frames
		for F in (Menu, Result):
			frame = F(container, self)
			self.frames[F.__name__] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		# Show initial frame
		self.show_frame("Menu")

	def center_window(self, width, height):
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		x = (screen_width // 2) - (width // 2)
		y = (screen_height // 2) - (height // 2)
		self.geometry(f"{width}x{height}+{x}+{y}")

	def show_frame(self, page_name):
		"""Show a frame for the given page name"""
		frame = self.frames[page_name]
		frame.tkraise()


if __name__ == "__main__":
	app = Main()
	app.mainloop()
