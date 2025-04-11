import os
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from algorithms.wrappers import modciFB, modciPD, modciV
from classes.social_network import SocialNetwork, calculate_internal_conflict
from main import load_social_network_from_txt


class Menu(ctk.CTkFrame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		ctk.set_appearance_mode("light") # "light" or "dark"
		ctk.set_default_color_theme("blue")

		# Absolute path of the image
		bg_path = os.path.join(os.path.dirname(__file__), "wallpapers", "page1.png")

		if os.path.exists(bg_path):
			img = Image.open(bg_path)
			img = img.resize((700, 600))
			self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(700, 600))
			self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
			self.bg_label.place(relx=0.5, rely=0.5,anchor="center")
		else:
			print(f" Image {bg_path} not found")

		# Main container on top of the background
		main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
		main_frame.place(relx=0.5, rely=0.5, anchor="center")

		# Title
		title_label = ctk.CTkLabel(
			main_frame,
			text="🌐 Social Network Analysis",
			font=("Segoe UI", 22, "bold")
		)
		title_label.pack(pady=(20, 20)) # 20 30

		# File upload button
		self.btn_load = ctk.CTkButton(
			main_frame,
			text=" Load TXT File",
			command=self.load_file,
			width=200,
			height=40,
			corner_radius=10
		)
		self.btn_load.pack(pady=20)

		# Path of the uploaded file
		self.lbl_file_path = ctk.CTkLabel(
			main_frame,
			text="No file loaded",
			text_color="gray",
			font=("Segoe UI", 12)
		)
		self.lbl_file_path.pack(pady=5) #5

		# Algorithm selection
		self.algorithm_var = ctk.StringVar(value="Select algorithm")
		self.dropdown_algorithm = ctk.CTkOptionMenu(
			main_frame,
			values=["Greedy", "Brute force", "Dynamic programming"],
			variable=self.algorithm_var,
			width=200,
			height=35,
			corner_radius=10
		)
		self.dropdown_algorithm.pack(pady=15) # 15

		# Button to run algorithm
		self.btn_run = ctk.CTkButton(
			main_frame,
			text="⚙️ Run Algorithm",
			command=self.run_algorithm,
			width=200,
			height=40,
			corner_radius=10,
			fg_color="#3B82F6",
			hover_color="#2563EB"
		)
		self.btn_run.pack(pady=25) # 25

	def load_file(self):
		file_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])
		if file_path:
			try:
				social_network = load_social_network_from_txt(file_path)
				if not isinstance(social_network, SocialNetwork):
					raise ValueError("Error: the file did not generate a valid social network")
				self.controller.social_network = social_network
				self.controller.file_path = file_path
				self.lbl_file_path.configure(text=f"✅ Loaded: {os.path.basename(file_path)}")
				messagebox.showinfo("Success", "File loaded successfully.")
			except Exception as e:
				messagebox.showerror("Error", f"Could not load file: {e}")

	def run_algorithm(self):
		if not self.controller.social_network:
			messagebox.showwarning("Warning", "Please load a TXT file first.")
			return

		algorithm = self.algorithm_var.get()
		if algorithm == "Select algorithm":
			messagebox.showwarning("Warning", "Please select a valid algorithm.")
			return

		try:
			print(f"Running algorithm: {algorithm}")

			if algorithm == "Greedy":
				result = modciV(self.controller.social_network)
			elif algorithm == "Brute force":
				result = modciFB(self.controller.social_network)
			elif algorithm == "Dynamic programming":
				result = modciPD(self.controller.social_network)

			if not isinstance(result, tuple) or len(result) != 3:
				raise ValueError(f"Error: invalid algorithm result ({result})")

			strategy, effort, conflict = result

			self.controller.strategy = strategy
			self.controller.effort = effort
			self.controller.conflict = conflict
			self.controller.original_conflict = calculate_internal_conflict(self.controller.social_network)

			# Switch to results page
			self.controller.show_frame("Result")
			results_page = self.controller.frames["Result"]
			results_page.show_result(strategy, effort, conflict)

		except Exception as e:
			print(f"Error: {e}")
			messagebox.showerror("Error", f"An error occurred while running the algorithm: {e}")