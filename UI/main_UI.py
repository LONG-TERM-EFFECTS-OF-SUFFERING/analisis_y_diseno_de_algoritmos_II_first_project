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
		self.geometry("700x600")

		# Configure the appearance
		ctk.set_appearance_mode("dark")  # Options: "dark", "light"
		ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

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

	def show_frame(self, page_name):
		"""Show a frame for the given page name"""
		frame = self.frames[page_name]
		frame.tkraise()


if __name__ == "__main__":
	app = Main()
	app.mainloop()
