import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Global sinyal tanımı
t = np.linspace(-20, 20, 1000)
signal = np.zeros_like(t)

def plot_signal():
    plt.plot(t, signal, label='Signal')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlabel('Time (t)')
    plt.ylabel('Amplitude')
    plt.title('Continuous Signal')
    plt.legend()
    plt.show()

def add_segment():
    try:
        tip = type_var.get().strip().upper()
        Bast = float(entry_start_time.get())
        Sont = float(entry_end_time.get())
        Basnok = float(entry_start_amp.get())
        Sonnok = float(entry_end_amp.get())

        scale_text = entry_scale.get().strip()
        apply_scale = False
        if scale_text != "":
            try:
                scale = float(scale_text)
                apply_scale = True
            except ValueError:
                messagebox.showerror("Error", "Scale must be a valid number.")
                return

        # Zaman kaydırma ve ölçekleme
        time_shift_text = entry_time_shift.get().strip()
        time_scale_text = entry_time_scale.get().strip()
        time_shift = 0
        time_scale = 1

        if time_shift_text != "":
            try:
                time_shift = -float(time_shift_text)
            except ValueError:
                messagebox.showerror("Error", "Time Shift must be a valid number.")
                return

        if time_scale_text != "":
            if time_scale_text.lower() == "sym":
                time_scale = -1  # Zaman eksenine göre simetri
            else:
                try:
                    time_scale = float(time_scale_text)
                    if time_scale == 0:
                        messagebox.showerror("Error", "Time Scale cannot be zero.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Time Scale must be a valid number or 'sym'.")
                    return

        if Sont == Bast:
            messagebox.showerror("Error", "Start and end times cannot be the same.")
            return

        # Yeni zaman aralığına göre maske oluştur
        transformed_t = (t - time_shift) / time_scale
        mask = (transformed_t >= Bast) & (transformed_t <= Sont)

        if tip == "Y":
            slope = (Sonnok - Basnok) / (Sont - Bast)
            temp_signal = Basnok + slope * (transformed_t[mask] - Bast)
        elif tip == "S":
            temp_signal = np.full_like(transformed_t[mask], Basnok)
        else:
            messagebox.showerror("Error", "Type must be Y (linear) or S (step).")
            return

        if apply_scale:
            temp_signal *= scale

        signal[mask] = temp_signal

        messagebox.showinfo("Success", "Segment added successfully.")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# Tkinter GUI
root = tk.Tk()
root.title("Signal Builder")

# Segment tipi
tk.Label(root, text="Type (Y/S):").grid(row=0, column=0)
type_var = tk.StringVar()
tk.Entry(root, textvariable=type_var).grid(row=0, column=1)

# Başlangıç zamanı
tk.Label(root, text="Start time (t1):").grid(row=1, column=0)
entry_start_time = tk.Entry(root)
entry_start_time.grid(row=1, column=1)

# Bitiş zamanı
tk.Label(root, text="End time (t2):").grid(row=2, column=0)
entry_end_time = tk.Entry(root)
entry_end_time.grid(row=2, column=1)

# Başlangıç genliği
tk.Label(root, text="Start amplitude:").grid(row=3, column=0)
entry_start_amp = tk.Entry(root)
entry_start_amp.grid(row=3, column=1)

# Bitiş genliği
tk.Label(root, text="End amplitude:").grid(row=4, column=0)
entry_end_amp = tk.Entry(root)
entry_end_amp.grid(row=4, column=1)

# Genlik Ölçekleme (opsiyonel)
tk.Label(root, text="Amplitude Scale (optional):").grid(row=5, column=0)
entry_scale = tk.Entry(root)
entry_scale.grid(row=5, column=1)

# Zaman kaydırma (opsiyonel)
tk.Label(root, text="Time Shift (optional):").grid(row=6, column=0)
entry_time_shift = tk.Entry(root)
entry_time_shift.grid(row=6, column=1)

# Zaman ölçekleme (opsiyonel)
tk.Label(root, text="Time Scale (optional, use 'sym' for reflection):").grid(row=7, column=0)
entry_time_scale = tk.Entry(root)
entry_time_scale.grid(row=7, column=1)

# Segment ekle butonu
tk.Button(root, text="Add Segment", command=add_segment).grid(row=8, column=0, columnspan=2)

# Çizim butonu
tk.Button(root, text="Plot Signal", command=plot_signal).grid(row=9, column=0, columnspan=2)

# Bilgi etiketi
tk.Label(root, text="If you want to use the optional variables, please include them in every data input process.").grid(row=10, column=0, columnspan=2)

# Arayüz boyutu
root.geometry("700x400")

# GUI döngüsü
root.mainloop()
