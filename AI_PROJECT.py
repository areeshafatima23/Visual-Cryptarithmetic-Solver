import customtkinter as ctk
from tkinter import messagebox
from itertools import permutations
from tkinter.font import Font
from PIL import Image, ImageTk

# Function to process a single cryptarithm equation
def process_equation(equations):
    """
    Process the equations to identify unique letters and prepare them for solving.
    Args:
        equations (list): List of equations as strings.
    Returns:
        tuple: Set of unique letters and a list of processed equations.
    """
    unique_letters = set()
    processed_equations = []

    for equation in equations:
        equation = equation.replace(" ", "")  # Remove spaces
        parts = equation.split("=")  # Split equation into left and right sides

        if len(parts) != 2:
            raise ValueError(f"Invalid equation format: {equation}")

        left_side = parts[0].split("+")  # Split left side into words
        right_side = parts[1]  # Extract right side

        if not right_side or not all(left_side):
            raise ValueError(f"Invalid equation format: {equation}")

        words = left_side + [right_side]  # Combine all words
        letters = set("".join(words))  # Extract unique letters

        unique_letters.update(letters)
        processed_equations.append((letters, words))

    return unique_letters, processed_equations

# Function to validate the number of unique letters
def validate_equation(letters, max_digits=10):
    """
    Ensure the number of unique letters does not exceed the available digits.
    Args:
        letters (set): Set of unique letters.
        max_digits (int): Maximum number of available digits (default 10).
    """
    if len(letters) > max_digits:
        raise ValueError(f"Too many unique letters ({len(letters)}) for available digits (max: {max_digits}).")

# Function to solve the cryptarithm
def solve_cryptarithm(unique_letters, words):
    """
    Solve the cryptarithm by finding a valid mapping of letters to digits.
    Args:
        unique_letters (set): Set of unique letters.
        words (list): List of words in the equation.
    Returns:
        dict or None: Mapping of letters to digits if solution exists, otherwise None.
    """
    letters = list(unique_letters)
    n = len(letters)

    if n > 10:  # More letters than digits available
        return None

    # Try all permutations of digits for the unique letters
    for perm in permutations(range(10), n):
        letter_to_digit = dict(zip(letters, perm))

        # Skip mappings where leading digits are zero
        if any(letter_to_digit[word[0]] == 0 for word in words):
            continue

        # Check if the current mapping is a valid solution
        if is_valid_solution(letter_to_digit, words):
            return letter_to_digit

    return None

# Helper function to validate a solution
def is_valid_solution(letter_to_digit, words):
    """
    Check if a given letter-to-digit mapping is a valid solution.
    Args:
        letter_to_digit (dict): Mapping of letters to digits.
        words (list): List of words in the equation.
    Returns:
        bool: True if the solution is valid, otherwise False.
    """
    left_side = words[:-1]  # All words except the last
    right_side = words[-1]  # The last word (result)

    left_sum = sum(convert_to_number(word, letter_to_digit) for word in left_side)
    right_number = convert_to_number(right_side, letter_to_digit)

    return left_sum == right_number

# Helper function to convert a word to a number
def convert_to_number(word, letter_to_digit):
    """
    Convert a word to a number based on a letter-to-digit mapping.
    Args:
        word (str): The word to convert.
        letter_to_digit (dict): Mapping of letters to digits.
    Returns:
        int: The corresponding number.
    """
    return int("".join(str(letter_to_digit[letter]) for letter in word))

# GUI class for the Cryptarithm Solver
class CryptarithmSolverGUI:
    def __init__(self, root):
        """
        Initialize the GUI application.
        Args:
            root (ctk.CTk): Root window for the application.
        """
        self.root = root
        self.root.title("Visual Cryptarithm Solver")
        self.root.geometry("800x600")

        # Set theme for customtkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.equations = []  # List to store added equations
        self.show_welcome_screen()  # Show the welcome screen

    def show_welcome_screen(self):
        """
        Display the welcome screen with a background image and a start button.
        """
        welcome_frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color="#4A6D67")
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Try loading a background image
        try:
            img = Image.open("C:/Users/Dell/Downloads/iCryptInt-Screenshot-b.jpg")
            bg_image = ImageTk.PhotoImage(img)
            background_label = ctk.CTkLabel(welcome_frame, image=bg_image)
            background_label.place(relwidth=1, relheight=1)
            background_label.image = bg_image
        except Exception as e:
            print("Error loading background image:", e)

        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to Cryptarithm Solver!",
            text_color="white",
            font=("Arial", 30, "bold"),
        )
        welcome_label.pack(pady=100)

        start_button = ctk.CTkButton(
            welcome_frame,
            text="Start",
            command=lambda: self.show_main_screen(welcome_frame),
            font=("Arial", 20, "bold"),
            fg_color="#008080",
            hover_color="#006666",
            text_color="white",
            corner_radius=20,
            width=200,
            height=60,
            border_width=4
        )
        start_button.pack(pady=20, anchor="center")

    def show_main_screen(self, frame_to_destroy):
        """
        Transition to the main screen and destroy the welcome frame.
        Args:
            frame_to_destroy (ctk.CTkFrame): The frame to be destroyed.
        """
        frame_to_destroy.destroy()
        self.create_main_interface()

    def create_main_interface(self):
        """
        Create the main interface for adding and solving cryptarithm equations.
        """
        # Header section
        header_frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color="#326D7F")
        header_frame.pack(fill="x", padx=20, pady=10)

        header_label = ctk.CTkLabel(
            header_frame,
            text="Cryptarithm Solver",
            text_color="white",
            font=("Times New Roman", 26, "bold"),
        )
        header_label.pack(pady=10)

        # Content section
        content_frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color="#BED1E3")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(content_frame, text="Enter Cryptarithm Equation:", font=("Times New Roman", 20, "bold"), text_color="#5A94C1").pack(pady=15)

        # Input field for entering equations
        self.input_field = ctk.CTkEntry(content_frame, width=400, font=("Times New Roman", 14), border_color="white", border_width=2, fg_color="#77A6C0", text_color="#404040")
        self.input_field.pack(pady=10)

        # Buttons for adding and solving equations
        button_frame = ctk.CTkFrame(content_frame, fg_color="#BED1E3")
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Add Equation", command=self.add_equation, font=("Times New Roman", 16), fg_color="#5A94C1", text_color="white", hover_color="#006666", corner_radius=10).grid(row=0, column=0, padx=15)
        ctk.CTkButton(button_frame, text="Solve", command=self.solve, font=("Times New Roman", 16), fg_color="#5A94C1", hover_color="#006666", text_color="white", corner_radius=10).grid(row=0, column=1, padx=15)

        # Display added equations
        ctk.CTkLabel(content_frame, text="Added Equations:", font=("Times New Roman", 18, "bold"), text_color="#5A94C1").pack(pady=15)
        self.equations_list = ctk.CTkTextbox(content_frame, width=400, height=200, font=("Times New Roman", 14), border_color="white", border_width=2, fg_color="#77A6C0", text_color="#404040", corner_radius=10)
        self.equations_list.pack()

    def add_equation(self):
        """
        Add a new equation to the list after validating it.
        """
        equation = self.input_field.get().strip()
        if not equation:
            self.display_error("Invalid Input", "The equation cannot be empty.")
            return

        try:
            _, _ = process_equation([equation])  # Validate the equation format
            self.equations.append(equation)
            self.equations_list.insert("end", equation + "\n")
            self.input_field.delete(0, "end")
        except ValueError as e:
            self.display_error("Invalid Equation", str(e))

    def solve(self):
        """
        Solve the added equations and display the result.
        """
        if not self.equations:
            self.display_error("Error", "No equations added!")
            return

        try:
            # Process and validate equations
            unique_letters, processed_equations = process_equation(self.equations)
            validate_equation(unique_letters)

            # Prepare message for processed equations
            result = f"Unique Letters: {unique_letters}\n\nProcessed Equations:\n"
            for i, (letters, words) in enumerate(processed_equations):
                result += f"Equation {i+1}: {words}\n"

            # Display processed equations and proceed to solving
            self.display_processed_equations_and_continue("Processed Equations", result, unique_letters, processed_equations)

        except ValueError as e:
            self.display_error("Error", str(e))

    def display_processed_equations_and_continue(self, title, message, unique_letters, processed_equations):
        """
        Display processed equations and proceed to finding a solution.
        """
        def on_ok():
            output_window.destroy()  # Close the current window
            words = [word for _, words in processed_equations for word in words]
            solution = solve_cryptarithm(unique_letters, words)

            if solution:
                solution_str = "\n".join([f"{letter} -> {digit}" for letter, digit in solution.items()])
                self.display_output("Solution Found", f"Mapping:\n{solution_str}")
            else:
                self.display_output("No Solution", "The given cryptarithm has no solution.")

        output_window = ctk.CTkToplevel(self.root)
        output_window.title(title)
        output_window.geometry("600x400")

        header_frame = ctk.CTkFrame(output_window, corner_radius=20, fg_color="#326D7F")
        header_frame.pack(fill="x", padx=20, pady=10)

        header_label = ctk.CTkLabel(
            header_frame,
            text=title,
            text_color="white",
            font=("Times New Roman", 24, "bold"),
        )
        header_label.pack(pady=10)

        frame = ctk.CTkFrame(output_window, fg_color="#BED1E3", corner_radius=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=message, font=("Times New Roman", 14), text_color="#404040", wraplength=540).pack(pady=20)
        ctk.CTkButton(frame, text="OK", command=on_ok, font=("Times New Roman", 12), fg_color="#5A94C1", text_color="white", corner_radius=10).pack(pady=10)

    def display_output(self, title, message):
        """
        Display output or solution in a new window.
        """
        output_window = ctk.CTkToplevel(self.root)
        output_window.title(title)
        output_window.geometry("600x400")

        header_frame = ctk.CTkFrame(output_window, corner_radius=20, fg_color="#326D7F")
        header_frame.pack(fill="x", padx=20, pady=10)

        header_label = ctk.CTkLabel(
            header_frame,
            text=title,
            text_color="white",
            font=("Times New Roman", 24, "bold"),
        )
        header_label.pack(pady=10)

        frame = ctk.CTkFrame(output_window, fg_color="#BED1E3", corner_radius=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=message, font=("Times New Roman", 14), text_color="#404040", wraplength=540).pack(pady=20)
        ctk.CTkButton(frame, text="Close", command=output_window.destroy, font=("Times New Roman", 12), fg_color="#5A94C1", text_color="white", corner_radius=10).pack(pady=10)

    def display_error(self, title, message):
        """
        Display an error message in a new window.
        """
        error_window = ctk.CTkToplevel(self.root)
        error_window.title(title)
        error_window.geometry("400x200")

        header_frame = ctk.CTkFrame(error_window, corner_radius=20, fg_color="#326D7F")
        header_frame.pack(fill="x", padx=20, pady=10)

        header_label = ctk.CTkLabel(
            header_frame,
            text=title,
            text_color="white",
            font=("Times New Roman", 24, "bold"),
        )
        header_label.pack(pady=10)

        frame = ctk.CTkFrame(error_window, fg_color="#BED1E3", corner_radius=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=message, font=("Times New Roman", 14), text_color="#404040", wraplength=380).pack(pady=20)
        ctk.CTkButton(frame, text="OK", command=error_window.destroy, font=("Times New Roman", 12), fg_color="#5A94C1", text_color="white", corner_radius=10).pack(pady=10)

# Main execution
if __name__ == "__main__":
    root = ctk.CTk()  # Create the root window
    app = CryptarithmSolverGUI(root)  # Instantiate the GUI class
    root.mainloop()  # Run the main event loop
