import tkinter as tk
from tkinter import filedialog
from controller import DataController

class DataView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = DataController()
        self.title("BGV_Encryption_ Business_Revenue")
        self.geometry("700x600")
        
        # Option selection
        option_label = tk.Label(self, text="Select Option:")
        option_label.pack(anchor='w', padx=10, pady = (10,0))
        self.option_var = tk.StringVar()
        self.option_var.set("encrypt")  # Mặc định là encrypt
        option_menu = tk.OptionMenu(self, self.option_var, "encrypt", "decrypt", command=self.update_ui)
        option_menu.config(width=20)
        option_menu.pack(anchor='w', padx=10, pady=(0,10))

        # Encrypt frame
        self.encrypt_frame = tk.Frame(self)
        self.encrypt_frame.pack()
        self.encrypt_widgets = []
        self.create_encrypt_widgets()

        # Decrypt frame
        self.decrypt_frame = tk.Frame(self)
        # self.decrypt_frame.pack()
        self.decrypt_widgets = []
        self.create_decrypt_widgets()

    def create_encrypt_widgets(self):
        # Path selection
        file_label = tk.Label(self.encrypt_frame, text="Select File:")
        file_label.pack(anchor='w', padx=10, pady=(5, 0))
        file_path_frame = tk.Frame(self.encrypt_frame)  # Create a frame to hold the entry and button
        self.file_path_edit = tk.Entry(file_path_frame)
        self.file_path_edit.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Make the entry expandable
        file_button = tk.Button(file_path_frame, text="Browse", command=self.browse_file)
        file_button.pack(side=tk.LEFT)  # Place button to the right of the entry
        file_path_frame.pack(fill=tk.X,padx=10, pady=(0, 5))  # Allow the frame to f

        # Number inputs
        n_label = tk.Label(self.encrypt_frame, text=f"Enter N:")
        n_label.pack(anchor='w', padx=10, pady=(5, 0))
        self.n_number_edit = tk.Entry(self.encrypt_frame)
        self.n_number_edit.pack(anchor='w', padx=10, pady=(0, 5))
        # self.encrypt_widgets.append(n_number_edit)

        # coef_label = tk.Label(self.encrypt_frame, text=f"Enter coef modulus:")
        # coef_label.pack(anchor='w', padx=10, pady=(5, 0))
        # self.coef_edit = tk.Entry(self.encrypt_frame)
        # self.coef_edit.pack(anchor='w', padx=10, pady=(0, 5))
        # self.encrypt_widgets.append(coef_edit)

        # poly_label = tk.Label(self.encrypt_frame, text=f"Enter poly modulus:")
        # poly_label.pack(anchor='w', padx=10, pady=(5, 0))
        # self.poly_edit = tk.Entry(self.encrypt_frame)
        # self.poly_edit.pack(anchor='w', padx=10, pady=(0, 5))
        # self.encrypt_widgets.append(poly_edit)

        plain_label = tk.Label(self.encrypt_frame, text=f"Enter plaintext modulus:")
        plain_label.pack(anchor='w', padx=10, pady=(5, 0))
        self.plain_edit = tk.Entry(self.encrypt_frame)
        self.plain_edit.pack(anchor='w', padx=10, pady=(0, 5))

        base_label = tk.Label(self.encrypt_frame, text=f"Enter base number:")
        base_label.pack(anchor='w', padx=10, pady=(5, 0))
        self.base_edit = tk.Entry(self.encrypt_frame)
        self.base_edit.pack(anchor='w', padx=10, pady=(0, 5))

        # Preview file
        preview_label = tk.Label(self.encrypt_frame, text="Preview File:")
        preview_label.pack()
        self.preview_text = tk.Text(self.encrypt_frame, height=8, width=60)
        self.preview_text.pack()

        # Encrypt button
        encrypt_button = tk.Button(self.encrypt_frame, text="Encrypt", command=self.encryption_process)
        encrypt_button.pack()

    def create_decrypt_widgets(self):
        # Decrypt path selection
        decrypt_file_label = tk.Label(self.decrypt_frame, text="Select Decrypt File:")
        decrypt_file_label.pack(anchor='w', padx=10, pady=(5, 0))
        decrypt_file_path_frame = tk.Frame(self.decrypt_frame)
        self.decrypt_file_path_edit = tk.Entry(decrypt_file_path_frame)
        self.decrypt_file_path_edit.pack(side=tk.LEFT, fill=tk.X, expand=True)
        decrypt_file_button = tk.Button(decrypt_file_path_frame, text="Browse", command=self.browse_decrypt_file)
        decrypt_file_button.pack(side=tk.LEFT)
        decrypt_file_path_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        # SK file selection
        sk_file_label = tk.Label(self.decrypt_frame, text="Select SK File:")
        sk_file_label.pack(anchor='w', padx=10, pady=(5, 0))
        sk_file_path_frame = tk.Frame(self.decrypt_frame)
        self.sk_file_path_edit = tk.Entry(sk_file_path_frame)
        self.sk_file_path_edit.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sk_file_button = tk.Button(sk_file_path_frame, text="Browse", command=self.browse_sk_file)
        sk_file_button.pack(side=tk.LEFT)
        sk_file_path_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        # Plaintext modulus input
        plaintext_modulus_label = tk.Label(self.decrypt_frame, text="Enter Plaintext Modulus:")
        plaintext_modulus_label.pack(anchor='w', padx=10, pady=(5, 0))
        self.plaintext_modulus_edit = tk.Entry(self.decrypt_frame)
        self.plaintext_modulus_edit.pack(anchor='w', padx=10, pady=(0, 5))

        # Preview file
        preview_label = tk.Label(self.decrypt_frame, text="Preview File:")
        preview_label.pack()
        self.decrypt_preview_text = tk.Text(self.decrypt_frame, height=8, width=60)
        self.decrypt_preview_text.pack()

        # Decrypt button
        decrypt_button = tk.Button(self.decrypt_frame, text="Decrypt", command=self.decryption_process)
        decrypt_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_edit.delete(0, tk.END)
            self.file_path_edit.insert(0, file_path)
            # Update preview text
            with open(file_path, "r") as file:
                data = file.read()
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, data)

    def browse_decrypt_file(self):
        file_paths = filedialog.askopenfilenames(title="Select files", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if file_paths:
            self.decrypt_file_path_edit.delete(0, tk.END)
            self.decrypt_file_path_edit.insert(0, file_paths)
            # Update preview text
        for file_path in file_paths:
            try:
                with open(file_path, "r") as file:
                    data = file.read()
                    self.decrypt_preview_text.delete(1.0, tk.END)
                    self.decrypt_preview_text.insert(tk.END, f"--- {file_path} ---\n{data}\n\n")
            except Exception as e:
                self.decrypt_preview_text.insert(tk.END, f"Failed to read {file_path}: {str(e)}\n\n")

    def browse_sk_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.sk_file_path_edit.delete(0, tk.END)
            self.sk_file_path_edit.insert(0, file_path)
            try:
                with open(file_path, "r") as file:
                    data = file.read()
                    self.decrypt_preview_text.delete(1.0, tk.END)
                    self.decrypt_preview_text.insert(tk.END, data)
            except Exception as e:
                self.decrypt_preview_text.insert(tk.END, f"Failed to read {file_path}: {str(e)}\n\n")

    def encryption_process(self):
        select_option = self.option_var.get()
        file_path = self.file_path_edit.get()
        n_number = int(self.n_number_edit.get())
        plain_modulus = int(self.plain_edit.get())
        # plain_modulus = int(self.plaintext_modulus_edit.get())
        base = int(self.base_edit.get())

        self.controller.set_selected_option(select_option)
        self.controller.set_file_path(file_path)
        self.controller.set_value(n_number, plain_modulus , base)

        data = self.controller.get_data_encrypt()
        self.controller.process_encryption(data)

    def decryption_process(self):
        # select_option = self.option_var.get()
        file_decrypt_path = self.decrypt_file_path_edit.get()
        mid_term = len(file_decrypt_path)//2
        c0_path = file_decrypt_path[:mid_term].lstrip()
        c1_path = file_decrypt_path[mid_term:].lstrip()
        sk_path = self.sk_file_path_edit.get()
        plaintext_modulus = int(self.plaintext_modulus_edit.get())

        data = self.controller.set_decrypt_value(c0_path,c1_path,sk_path,plaintext_modulus)

        data = self.controller.get_data_decrypt()
        self.controller.process_decryption(data)


    def update_ui(self, *args):
        option = self.option_var.get()
        if option == "encrypt":
            self.encrypt_frame.pack(fill='both', expand=True)
            self.decrypt_frame.pack_forget()
        elif option == "decrypt":
            self.encrypt_frame.pack_forget()
            self.decrypt_frame.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = DataView()
    app.mainloop()