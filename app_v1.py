import tkinter as tk
from tkinter import filedialog, ttk
import csv

def open_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.config(state="normal")
        entry_widget.insert(0, file_path)
        entry_widget.config(state="readonly")
        update_preview(file_path)

def update_file_button_label(*args):

    # file_button
    # Làm mới vùng preview khi thay đổi lựa chọn
    # file_button.config(text=f"Choose {'Encryption' if option_var.get() == 'Encryption' else 'Decryption'} File")
    # path_entry.config(state="normal")
    # path_entry.delete(0, tk.END)
    # path_entry.config(state="readonly")

    # # if 'path_sk_entry' in globals() and isinstance(path_sk_entry, tk.Entry):
    # #     path_sk_entry.config(state="normal")
    # #     path_sk_entry.delete(0, tk.END)
    # #     path_sk_entry.config(state="readonly")
    
    # preview_text.delete('1.0', tk.END)

    # for widget in parameter_frame.winfo_children():
    #     widget.destroy()
    
    # Tạo các trường nhập mới dựa trên lựa chọn
    if option_var.get() == 'Encryption':
        create_encryption_parameters()
    else:
        create_decryption_parameters()

def create_encryption_parameters():
    tk.Label(parameter_frame, text="Enter n - the exponent of 2:").grid(row=0, column=0, sticky='w')
    tk.Entry(parameter_frame, borderwidth=1, relief="solid").grid(row=0, column=1, sticky='ew',padx=(0,500),pady=(10,10))
    
    tk.Label(parameter_frame, text="Enter bit of coef_modulus:").grid(row=1, column=0, sticky='w',pady=(0,10))
    tk.Entry(parameter_frame, borderwidth=1, relief="solid").grid(row=1, column=1, sticky='ew',padx=(0,500))
    
    tk.Label(parameter_frame, text="Enter plaintext_modulus:").grid(row=2, column=0, sticky='w',pady=(0,10))
    tk.Entry(parameter_frame, borderwidth=1, relief="solid").grid(row=2, column=1, sticky='ew',padx=(0,500))

    encrypt_button = tk.Button(parameter_frame,text="Encryption_Messages", borderwidth=1, relief="solid",height=3)
    encrypt_button.grid(row=3, column=0,sticky="ew")

def create_decryption_parameters():
    global path_sk_entry
    parameter_frame.grid_columnconfigure(0, weight=1)
    path_sk_entry = tk.Entry(parameter_frame, state="readonly",relief="solid", borderwidth=1)
    path_sk_entry.grid(row=0, column=0,columnspan=2, sticky='we', padx=(0,150), pady=5)

    file_sk_button = tk.Button(parameter_frame, text="Choose Secret Key File", command=lambda: open_file(path_sk_entry),relief="solid", borderwidth=1)
    file_sk_button.grid(row=0, column=1, padx=(10,0), pady=5,sticky='e')
    
    tk.Label(parameter_frame, text="Enter plaintext_modulus:").grid(row=1, column=0, sticky='w',pady=(0,10))
    tk.Entry(parameter_frame, borderwidth=1, relief="solid").grid(row=1, column=1, sticky='ew',padx=(0,500))

    encrypt_button = tk.Button(parameter_frame,text="Encryption_Messages", borderwidth=1, relief="solid",height=3)
    encrypt_button.grid(row=2, column=0,sticky="ew")

def update_preview(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Bỏ qua dòng đầu tiên (tiêu đề)
        # Lấy 5 dòng tiếp theo từ file CSV
        rows = [next(csvreader) for _ in range(5)]
        preview_text.delete('1.0', tk.END)  # Xóa nội dung cũ trước khi cập nhật
        # Cập nhật vùng preview với 5 dòng tiếp theo
        preview_text.insert(tk.END,"Preview csv file:"+"\n")
        for row in rows:
            preview_text.insert(tk.END, ', '.join(row) + '\n')


root = tk.Tk()

update_file_button_label()

parameter_frame = tk.Frame(root,relief='solid',borderwidth=1)
parameter_frame.grid(row=3, column=0,columnspan=2, sticky='ew', padx=10, pady=5)

# Tạo cửa sổ chính
root.title("File Selection Interface")
root.geometry("950x700")
root.resizable(False, False)

# Tạo biến Tkinter để lưu giá trị được chọn từ bảng kéo xuống
option_var = tk.StringVar(root)
option_var.set("Decryption")  # Đặt giá trị mặc định
option_var.trace("w", update_file_button_label)

# Tạo bảng kéo xuống
option_menu = ttk.Combobox(root, textvariable=option_var, values=["Encryption", "Decryption"], state="readonly")
option_menu.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

# Tạo entry để hiển thị đường dẫn file và đặt nó thành không thể chỉnh sửa
path_entry = tk.Entry(root, width=50, state="readonly",relief="solid", borderwidth=1)
path_entry.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

# Tạo nút để mở hộp thoại chọn file
file_button = tk.Button(root, text="Choose Encryption File", command=lambda:open_file(path_entry),relief="solid", borderwidth=1)
file_button.grid(row=1, column=1, padx=10, pady=5)

preview_text = tk.Text(root, height=10, width=70, borderwidth=1, relief="solid")
preview_text.grid(row=4, column=0, sticky='ew', padx=10, pady=5)

root.grid_columnconfigure(0, weight=1)

# Chạy giao diện
root.mainloop()
