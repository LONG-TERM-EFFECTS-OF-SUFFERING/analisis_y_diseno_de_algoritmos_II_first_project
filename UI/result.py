from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from main import write_output


class Result(ctk.CTkFrame):
	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)
		self.controller = controller

		# Main frame
		main_frame = ctk.CTkFrame(self)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)

		# Title
		title_label = ctk.CTkLabel(main_frame, text="algorithm results", font=("Helvetica", 18))
		title_label.pack(pady=10)

		# Button to go back to home page
		back_button = ctk.CTkButton(
			main_frame,
			text="back to home",
			command=lambda: controller.show_frame("Menu")
		)
		back_button.pack(pady=10)

		# Area for graphs
		self.graph_frame = ctk.CTkFrame(main_frame)
		self.graph_frame.pack(fill="both", expand=True, pady=10)

		plt.style.use("dark_background") # Match with dark theme
		self.fig = plt.Figure(figsize=(6, 4), dpi=100)
		self.ax = self.fig.add_subplot(111)

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
		self.canvas_widget = self.canvas.get_tk_widget()
		self.canvas_widget.pack(fill="both", expand=True)

		# Labels for effort and conflict
		self.results_frame = ctk.CTkFrame(main_frame)
		self.results_frame.pack(fill="x", pady=10)

		self.lbl_effort = ctk.CTkLabel(self.results_frame, text="effort: ")
		self.lbl_effort.pack(pady=5)
		self.lbl_original_conflict = ctk.CTkLabel(self.results_frame, text="original conflict: ")
		self.lbl_original_conflict.pack(pady=5)
		self.lbl_moderated_conflict = ctk.CTkLabel(self.results_frame, text="moderated conflict: ")
		self.lbl_moderated_conflict.pack(pady=5)

		# Button to save results
		self.btn_save = ctk.CTkButton(
			main_frame,
			text="save results",
			command=self.save_results
		)
		self.btn_save.pack(pady=10)

	def show_result(self, strategy, effort, conflict):
		self.ax.clear()

		# Get the original social network
		original_network = self.controller.social_network

		# This is the same for both networks
		o_1 = [group.o_1 for group in original_network.groups]
		o_2 = [group.o_2 for group in original_network.groups]

		# Extract data for plotting
		# Original network data
		sizes_orig = [group.n * 20 for group in original_network.groups] # Scale for visibility

		# Moderated network data
		sizes_mod = [e * 20 for e in strategy] # Scale for visibility

		# Create scatter plots
		scatter_orig = self.ax.scatter(o_1, o_2, s=sizes_orig, alpha=0.5, color="blue", label="original")
		scatter_mod = self.ax.scatter(o_1, o_2, s=sizes_mod, alpha=0.5, color="red", label="moderated")

		# Add reference lines at x=0 and y=0
		self.ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
		self.ax.axvline(x=0, color="gray", linestyle="--", alpha=0.3)

		# Set labels and title
		self.ax.set_xlabel("opinion 1")
		self.ax.set_ylabel("opinion 2")
		self.ax.set_title("opinion distribution in social network")
		self.ax.legend()

		# Set axis limits to show the full range of possible opinions
		self.ax.set_xlim(-110, 110)
		self.ax.set_ylim(-110, 110)

		self.canvas.draw()

		# Update labels
		self.lbl_effort.configure(text=f"effort: {effort}")
		self.lbl_original_conflict.configure(text="original conflict: " + str(self.controller.original_conflict))
		self.lbl_moderated_conflict.configure(text=f"new conflict: {conflict}")

	def save_results(self):
		if not self.controller.social_network or not hasattr(self.controller, "strategy"):
			messagebox.showwarning("Warning", "No results to save.")
			return

		try:
			write_output("output.txt", self.controller.social_network, self.controller.strategy)
			messagebox.showinfo("Success", "Results saved in \"output.txt\"")
		except Exception as e:
			messagebox.showerror("Error", f"Could not save the file: {e}")
