import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

from algorithms.wrappers import modciFB, modciPD, modciV
from classes.social_network import (SocialNetwork, calculate_effort,
                                    calculate_internal_conflict)
from main import load_social_network_from_txt


class Menu(ctk.CTkFrame):
	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)
		self.controller = controller

		# Main frame
		main_frame = ctk.CTkFrame(self)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)

		# Title
		title_label = ctk.CTkLabel(main_frame, text="Social network analysis", font=("Helvetica", 18))
		title_label.pack(pady=20)

		# Button to load file
		self.btn_load = ctk.CTkButton(
			main_frame,
			text="Load TXT File",
			command=self.load_file
		)
		self.btn_load.pack(pady=10)

		# Display loaded file path
		self.lbl_file_path = ctk.CTkLabel(main_frame, text="No file loaded")
		self.lbl_file_path.pack(pady=5)

		# Dropdown to select algorithm
		self.algorithm_var = ctk.StringVar(value="select algorithm")
		self.dropdown_algorithm = ctk.CTkOptionMenu(
			main_frame,
			values=["Greedy", "Brute force", "Dynamic programming"],
			variable=self.algorithm_var
		)
		self.dropdown_algorithm.pack(pady=10)

		# Button to run algorithm
		self.btn_run = ctk.CTkButton(
			main_frame,
			text="Run algorithm",
			command=self.run_algorithm
		)
		self.btn_run.pack(pady=20)

	def load_file(self):
		file_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])
		if file_path:
			try:
				social_network = load_social_network_from_txt(file_path)
				if not isinstance(social_network, SocialNetwork):
					raise ValueError("Error: the file did not generate a valid social network")
				self.controller.social_network = social_network
				self.controller.file_path = file_path
				self.lbl_file_path.configure(text=f"Loaded: {os.path.basename(file_path)}")
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

			# Navigate to results page
			self.controller.show_frame("Result")
			# Update results
			results_page = self.controller.frames["Result"]
			results_page.show_result(strategy, effort, conflict)

		except Exception as e:
			print(f"Error: {e}")
			messagebox.showerror("Error", f"An error occurred while running the algorithm: {e}")
