import os
import sys

# Add project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tkinter import filedialog, messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms.wrappers import modciFB, modciPD, modciV
from classes.social_network import SocialNetwork
from main import load_social_network_from_txt, write_output


class SocialNetworkApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Social Network Analysis")

		# Configure the appearance
		ctk.set_appearance_mode("dark")  # Options: "dark", "light"
		ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

		# Main frame
		self.main_frame = ctk.CTkFrame(root)
		self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

		# Button to load file
		self.btn_load = ctk.CTkButton(
			self.main_frame,
			text="Load TXT File",
			command=self.load_file
		)
		self.btn_load.pack(pady=10)

		# Dropdown to select algorithm
		self.algorithm_var = ctk.StringVar(value="Select Algorithm")
		self.dropdown_algorithm = ctk.CTkOptionMenu(
			self.main_frame,
			values=["Greedy", "Brute Force", "Dynamic Programming"],
			variable=self.algorithm_var
		)
		self.dropdown_algorithm.pack(pady=10)

		# Button to run algorithm
		self.btn_run = ctk.CTkButton(
			self.main_frame,
			text="Run Algorithm",
			command=self.run_algorithm
		)
		self.btn_run.pack(pady=10)

		# Area for graphs
		self.graph_frame = ctk.CTkFrame(self.main_frame)
		self.graph_frame.pack(fill="both", expand=True, pady=10)

		plt.style.use("dark_background") # Match with dark theme
		self.fig = plt.Figure(figsize=(5, 4), dpi=100)
		self.ax = self.fig.add_subplot(111)

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
		self.canvas_widget = self.canvas.get_tk_widget()
		self.canvas_widget.pack(fill="both", expand=True)

		# Labels for effort and conflict
		self.results_frame = ctk.CTkFrame(self.main_frame)
		self.results_frame.pack(fill="x", pady=10)

		self.lbl_effort = ctk.CTkLabel(self.results_frame, text="Effort: ")
		self.lbl_effort.pack(pady=5)
		self.lbl_conflict = ctk.CTkLabel(self.results_frame, text="Conflict: ")
		self.lbl_conflict.pack(pady=5)

		self.social_network = None
		self.file_path = None

	def load_file(self):
		self.file_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])
		if self.file_path:
			try:
				self.social_network = load_social_network_from_txt(self.file_path)
				if not isinstance(self.social_network, SocialNetwork):
					raise ValueError("Error: the file did not generate a valid social network")
				messagebox.showinfo("Success", "File loaded successfully.")
			except Exception as e:
				messagebox.showerror("Error", f"Could not load file: {e}")

	def run_algorithm(self):
		if not self.social_network:
			messagebox.showwarning("Warning", "Please load a TXT file first.")
			return

		algorithm = self.algorithm_var.get()
		if algorithm == "Select Algorithm":
			messagebox.showwarning("Warning", "Please select a valid algorithm.")
			return

		try:
			print(f"Running algorithm: {algorithm}")

			if algorithm == "Greedy":
				result = modciV(self.social_network)
			elif algorithm == "Brute Force":
				result = modciFB(self.social_network)
			elif algorithm == "Dynamic Programming":
				result = modciPD(self.social_network)

			if not isinstance(result, tuple) or len(result) != 3:
				raise ValueError(f"Error: invalid algorithm result ({result})")

			strategy, effort, conflict = result

			self.strategy = strategy
			self.effort = effort
			self.conflict = conflict

			if not isinstance(effort, (int, float)) or not isinstance(conflict, (int, float)):
				raise ValueError("Error: effort and conflict values must be numeric")

			self.show_result(strategy, effort, conflict)
		except Exception as e:
			print(f"Error: {e}")
			messagebox.showerror("Error", f"An error occurred while running the algorithm: {e}")

	def show_result(self, strategy, effort, conflict):
		self.ax.clear()
		labels = [f"Group {i + 1}" for i in range(len(strategy))]
		values = list(strategy)

		self.ax.bar(labels, values)
		self.ax.set_title("Algorithm results")
		self.canvas.draw()

		self.lbl_effort.configure(text=f"Effort: {effort}")
		self.lbl_conflict.configure(text=f"Conflict: {conflict}")

		# Save results to a file
		try:
			write_output("output.txt", self.social_network, self.strategy)
			messagebox.showinfo("Success", "Results saved in \"output.txt\"")
		except Exception as e:
			messagebox.showerror("Error", f"Could not save the file: {e}")


if __name__ == "__main__":
	root = ctk.CTk()
	app = SocialNetworkApp(root)
	root.mainloop()
