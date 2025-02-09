import subprocess
import tkinter as tk
import os
from tkinter import messagebox


def execute_commands_and_print_results(commands):
    result = subprocess.run(['C:\\Program Files\\Git\\bin\\bash.exe', '-c', commands], capture_output=True, text=True)

    if result.stdout:
        # Print the output
        print(result.stdout)
        return result.stdout
    if result.stderr:
        # Print the Error
        print(result.stderr)
        return result.stderr


# Create the main window
root = tk.Tk()
root.title("UI with 2 Panels")

# Create a frame for the left panel
left_panel = tk.Frame(root)
left_panel.pack(side=tk.LEFT, fill=tk.Y)

# Create a frame for the right panel
right_panel = tk.Frame(root)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
text_controls = []

# Create 5 text areas in the left panel with an execute button next to each
for i in range(5):
    text_area = tk.Text(left_panel, height=5, width=50)
    text_area.pack(fill=tk.X)


    def load_commands(i=i):
        try:
            file_name = f'file-{i}'
            if os.path.exists(file_name):
                with open(file_name, 'r') as file:
                    data = file.read()
                    return data
            return ""
        except Exception as e:
            status_label.config(text=f"Error loading file: {str(e)}")
            return ''


    text_area.insert(1.0, load_commands(), tk.END)
    button_frame = tk.Frame(left_panel)
    button_frame.pack()


    def print_output(text_area=text_area, i=i):
        commands = text_area.get("1.0", tk.END)
        text = execute_commands_and_print_results(commands)
        right_panel_text.delete(1.0, tk.END)
        right_panel_text.insert(1.0, f"Command: {i + 1}:\n{text}\n\n")


    def save_commands(text_area=text_area, i=i):
        commands = text_area.get("1.0", tk.END)
        if len(commands.strip()) < 1:
            print('empty commands')
            status_label.config(text=f"No commands to Save for Section:{i + 1}")
            return None
        filename = f"file-{i}"
        try:
            with open(filename, "w") as file:
                file.write(commands)
            status_label.config()
        except Exception as e:
            status_label.config(text=f"Error loading file: {str(e)}")


    button = tk.Button(button_frame, text=f"Execute-{i + 1}", command=print_output, width=25)
    button.pack(side=tk.LEFT)

    button = tk.Button(button_frame, text=f"Save-{i + 1}", command=save_commands, width=25)
    button.pack(side=tk.LEFT)

    status_label = tk.Label(button_frame, text="", padx=20, pady=10)
    status_label.pack()

    text_controls.append(text_area)

# Create a text area in the right panel to display the output
right_panel_text = tk.Text(right_panel)
right_panel_text.pack(fill=tk.BOTH, expand=True)


def on_closing():
    if messagebox.askokcancel("Exit Application", "Do you want to quit this Application?"):
        root.destroy()


entry = tk.Entry(root)
entry.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
# Start the main loop
root.mainloop()
