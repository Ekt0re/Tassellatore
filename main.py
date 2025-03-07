import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import csv


class ImageGridApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Suddivisione Immagine in Griglia")
        self.geometry("600x400")

        # Variabili di appoggio
        self.image_path = None
        self.img = None
        self.grid_result = []  # conterrà la griglia di lettere (M/T)

        # Frame superiore per i controlli
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Bottone per caricare l'immagine
        load_btn = tk.Button(control_frame, text="Carica Immagine", command=self.load_image)
        load_btn.grid(row=0, column=0, padx=5, pady=5)

        # Label e Entry per numero di celle orizzontali
        tk.Label(control_frame, text="Celle Orizzontali:").grid(row=0, column=1, padx=5, pady=5)
        self.cells_x_entry = tk.Entry(control_frame, width=5)
        self.cells_x_entry.grid(row=0, column=2, padx=5, pady=5)
        self.cells_x_entry.insert(0, "10")  # Valore di default

        # Label e Entry per numero di celle verticali
        tk.Label(control_frame, text="Celle Verticali:").grid(row=0, column=3, padx=5, pady=5)
        self.cells_y_entry = tk.Entry(control_frame, width=5)
        self.cells_y_entry.grid(row=0, column=4, padx=5, pady=5)
        self.cells_y_entry.insert(0, "10")  # Valore di default

        # Bottone per processare l'immagine
        process_btn = tk.Button(control_frame, text="Processa", command=self.process_image)
        process_btn.grid(row=0, column=5, padx=5, pady=5)

        # Bottone per salvare CSV
        save_btn = tk.Button(control_frame, text="Salva CSV", command=self.save_csv)
        save_btn.grid(row=0, column=6, padx=5, pady=5)

        # Text box per mostrare la griglia risultante
        self.result_text = tk.Text(self, wrap="none", width=80, height=15)
        self.result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_image(self):
        """Apre un file dialog per caricare un'immagine."""
        file_path = filedialog.askopenfilename(
            title="Seleziona un'immagine",
            filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Tutti i file", "*.*")]
        )
        if file_path:
            self.image_path = file_path
            try:
                # Carica l'immagine PIL
                self.img = Image.open(self.image_path).convert("RGB")
                messagebox.showinfo("Immagine caricata", f"Immagine caricata con successo:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile aprire l'immagine:\n{e}")
                self.image_path = None
                self.img = None

    def process_image(self):
        """Processa l'immagine caricata, suddividendola in celle e creando la griglia di M/T."""
        if not self.img:
            messagebox.showwarning("Attenzione", "Nessuna immagine caricata.")
            return

        try:
            num_cells_x = int(self.cells_x_entry.get())
            num_cells_y = int(self.cells_y_entry.get())
        except ValueError:
            messagebox.showwarning("Attenzione", "Inserisci valori numerici per le celle.")
            return

        if num_cells_x <= 0 or num_cells_y <= 0:
            messagebox.showwarning("Attenzione", "Il numero di celle deve essere maggiore di zero.")
            return

        width, height = self.img.size
        cell_width = width // num_cells_x
        cell_height = height // num_cells_y

        # Lista per la griglia di output
        self.grid_result = []

        # Scorriamo le celle
        for row in range(num_cells_y):
            row_data = []
            for col in range(num_cells_x):
                left = col * cell_width
                upper = row * cell_height
                right = left + cell_width
                bottom = upper + cell_height

                # Ritaglia la cella
                cell = self.img.crop((left, upper, right, bottom))
                pixels = cell.getdata()

                # Calcola la somma delle componenti
                r_sum, g_sum, b_sum = 0, 0, 0
                for (r, g, b) in pixels:
                    r_sum += r
                    g_sum += g
                    b_sum += b

                n = len(pixels)
                avg_r = r_sum / n
                avg_g = g_sum / n
                avg_b = b_sum / n

                # Criterio semplificato: se la componente B > R+10 e B > G+10 => 'M', altrimenti 'T'
                if avg_b > avg_r + 10 and avg_b > avg_g + 10:
                    cell_char = "M"
                else:
                    cell_char = "T"

                row_data.append(cell_char)
            self.grid_result.append(row_data)

        # Mostra la griglia nella Text box
        self.display_grid()

    def display_grid(self):
        """Visualizza la griglia di M/T nella Text box."""
        self.result_text.delete("1.0", tk.END)
        for row_data in self.grid_result:
            self.result_text.insert(tk.END, " ".join(row_data) + "\n")

    def save_csv(self):
        """Salva la griglia in un file CSV."""
        if not self.grid_result:
            messagebox.showwarning("Attenzione", "Nessuna griglia da salvare. Esegui prima il processing.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    for row_data in self.grid_result:
                        writer.writerow(row_data)
                messagebox.showinfo("CSV salvato", f"Griglia salvata con successo in:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile salvare il file CSV:\n{e}")


if __name__ == "__main__":
    app = ImageGridApp()
    app.mainloop()
