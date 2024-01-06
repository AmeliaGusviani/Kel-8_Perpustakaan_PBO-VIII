import pymysql
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def connection():
    conn=pymysql.connect(
        host='localhost', user='root', password='', db='perpustakaan'
    )
    return conn

class PerpustakaanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Perpustakaan")
        self.root.configure(bg="#D3D3D3")

        self.books = {
            "1": {"judul": "Python Programming", "pengarang": "John Doe", "rak": "A1","tersedia": True},
            "2": {"judul": "Data Science Basics", "pengarang": "Jane Smith", "rak": "B2","tersedia": True},
            "3": {"judul": "Web Development", "pengarang": "Bob Johnson", "rak": "C3","tersedia": True},
            "4": {"judul": "Python Crash Course", "pengarang": "Eric Matthes", "rak": "D4","tersedia": True},
            "5": {"judul": "Head First Design Patterns", "pengarang": "Bert Bates", "rak": "A2","tersedia": True},
            "6": {"judul": "Algorithms", "pengarang": "Robert Sedgewick", "rak": "B3","tersedia": True},
            "7": {"judul": "Eloquent Javascript", "pengarang": "Marijn Haverbeke", "rak": "C4","tersedia": True},
        }

        self.borrowed_books = []

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.buat_login_page()

    def buat_login_page(self):
        login_frame = ttk.Frame(self.root, padding=10)
        login_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        ttk.Label(login_frame, text="     PERPUSTAKAAN", font=("Roboto", 17, "bold")).grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")
        ttk.Label(login_frame, text="Username :", font=("Roboto", 10)).grid(row=1, column=0, sticky="E", padx=10, pady=5)
        ttk.Entry(login_frame, textvariable=self.username_var, font=("Roboto", 10)).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(login_frame, text="Password :", font=("Roboto", 10)).grid(row=2, column=0, sticky="E", padx=10, pady=5)
        ttk.Entry(login_frame, textvariable=self.password_var, show="*", font=("Roboto", 10)).grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(login_frame, text="Login", command=self.login, style="TButton").grid(row=3, column=0, columnspan=2, pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Roboto", 10))

    def buat_main_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Button(self.root, text="Pencarian", command=self.tampil_form_cari).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ttk.Button(self.root, text="Peminjaman", command=self.tampil_form_peminjaman).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ttk.Button(self.root, text="Pengembalian", command=self.tampil_form_pengembalian).grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ttk.Button(self.root, text="Histori", command=self.tampil_histori).grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

    def login(self):
        if self.username_var.get() == "user123" and self.password_var.get() == "12345":
            messagebox.showinfo("Login Berhasil", "Selamat datang!")
            self.buat_main_page()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def tampilkan_data_buku(self):
        conn = connection()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM buku"
            cursor.execute(query)
            result = cursor.fetchall()

            for i, row in enumerate(result, start=1):
                ttk.Label(self.root, text=f"{i}. Judul: {row[1]}, Pengarang: {row[2]}, Rak: {row[3]}", font=("Roboto", 10)).grid(row=i + 1, column=0, columnspan=3, pady=5)
                
        except pymysql.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def tampil_form_cari(self):
        SearchBukuForm(self.root, self)

    def tampil_form_peminjaman(self):
        PeminjamanBukuForm(self.root, self)

    def tampil_form_pengembalian(self):
        PengembalianBukuForm(self.root, self)

    def tampil_histori(self):
        HistoryForm(self.root, self)

class SearchBukuForm:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_search_form()

    def create_search_form(self):
        search_frame = ttk.Frame(self.root)
        search_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        ttk.Label(search_frame, text="Judul Buku:", font=("Roboto", 10)).grid(row=0, column=0, sticky="E", padx=5, pady=5)
        search_entry = ttk.Entry(search_frame, font=("Roboto", 10))
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(search_frame, text="Cari", command=lambda: self.display_book_info(search_frame, search_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def display_book_info(self, frame, book_title):
        found = False
        for key, value in self.app.books.items():
            if value["judul"].lower() == book_title.lower():
                found = True
                info_text = f"Judul: {value['judul']}\nPengarang: {value['pengarang']}\nRak: {value['rak']}"
                messagebox.showinfo("Informasi Buku", info_text)
                frame.destroy()
                break

        if not found:
            messagebox.showinfo("Informasi Buku", "Buku tidak ditemukan.")
        else:
            frame.destroy()

class PeminjamanBukuForm:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_borrow_form()

    def create_borrow_form(self):
        borrow_frame = ttk.Frame(self.root)
        borrow_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        ttk.Label(borrow_frame, text="Username:", font=("Roboto", 10)).grid(row=0, column=0, sticky="E", padx=5, pady=5)
        username_entry = ttk.Entry(borrow_frame, font=("Roboto", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(borrow_frame, text="Judul Buku:", font=("Roboto", 10)).grid(row=1, column=0, sticky="E", padx=5, pady=5)
        book_entry = ttk.Entry(borrow_frame, font=("Roboto", 10))
        book_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(borrow_frame, text="Tanggal Peminjaman:", font=("Roboto", 10)).grid(row=2, column=0, sticky="E", padx=5, pady=5)
        borrow_date_entry = ttk.Entry(borrow_frame, font=("Roboto", 10))
        borrow_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        borrow_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(borrow_frame, text="Pinjam", command=lambda: self.borrow_book(borrow_frame, username_entry.get(), book_entry.get(), borrow_date_entry.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def borrow_book(self, frame, username, book_title, borrow_date):
            if username and book_title and borrow_date:
                conn = connection()
                cursor = conn.cursor()

                try:
                    query = f"SELECT * FROM buku WHERE judul = '{book_title}' AND tersedia = 1"
                    cursor.execute(query)
                    result = cursor.fetchone()

                    if result:
                        book_id = result[0]
                        update_query = f"UPDATE buku SET tersedia = 0 WHERE id = {book_id}"
                        cursor.execute(update_query)

                        insert_query = f"INSERT INTO peminjaman (username, buku_id, tanggal_pinjam) VALUES ('{username}', {book_id}, '{borrow_date}')"
                        cursor.execute(insert_query)

                        history_query = f"INSERT INTO histori_peminjaman (buku_id, username, tanggal_pinjam) VALUES ({book_id}, '{username}', '{borrow_date}')"
                        cursor.execute(history_query)

                        conn.commit()
                        messagebox.showinfo("Peminjaman Berhasil", f"{book_title} berhasil dipinjam oleh {username}.")
                        frame.destroy()

                    else:
                        messagebox.showinfo("Peminjaman Gagal", f"{book_title} tidak tersedia atau tidak ditemukan.")

                except pymysql.Error as e:
                    print(f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

class PengembalianBukuForm:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_return_form()

    def create_return_form(self):
        return_frame = ttk.Frame(self.root)
        return_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        ttk.Label(return_frame, text="Username:", font=("Roboto", 10)).grid(row=0, column=0, sticky="E", padx=5, pady=5)
        username_entry = ttk.Entry(return_frame, font=("Roboto", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(return_frame, text="Judul Buku:", font=("Roboto", 10)).grid(row=1, column=0, sticky="E", padx=5, pady=5)
        book_entry = ttk.Entry(return_frame, font=("Roboto", 10))
        book_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(return_frame, text="Tanggal Pengembalian:", font=("Roboto", 10)).grid(row=2, column=0, sticky="E", padx=5, pady=5)
        return_date_entry = ttk.Entry(return_frame, font=("Roboto", 10))
        return_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        return_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(return_frame, text="Kembalikan", command=lambda: self.return_book(return_frame, username_entry.get(), book_entry.get(), return_date_entry.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def return_book(self, frame, username, book_title, return_date):
        if username and book_title and return_date:
            conn = connection()
            cursor = conn.cursor()

            try:
                query = f"SELECT * FROM peminjaman WHERE username = '{username}' AND buku_id IN (SELECT id FROM buku WHERE judul = '{book_title}') AND tanggal_kembali IS NULL"
                cursor.execute(query)
                result = cursor.fetchone()

                if result:
                    book_id = result[2]
                    update_query = f"UPDATE buku SET tersedia = 1 WHERE id = {book_id}"
                    cursor.execute(update_query)

                    update_query = f"UPDATE peminjaman SET tanggal_kembali = '{return_date}' WHERE username = '{username}' AND buku_id = {book_id}"
                    cursor.execute(update_query)

                    history_update_query = f"UPDATE histori_peminjaman SET tanggal_kembali = '{return_date}' WHERE buku_id = {book_id} AND username = '{username}'"
                    cursor.execute(history_update_query)

                    conn.commit()
                    messagebox.showinfo("Pengembalian Berhasil", f"{book_title} berhasil dikembalikan oleh {username}.")
                    frame.destroy()

                else:
                    messagebox.showinfo("Pengembalian Gagal", f"{book_title} tidak ditemukan atau tidak sedang dipinjam oleh {username}.")

            except pymysql.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


class HistoryForm:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_history_page()

    def create_history_page(self):
        history_frame = ttk.Frame(self.root)
        history_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        ttk.Label(history_frame, text="Histori", font=("Roboto", 14, "bold")).pack(pady=10)

        borrowed_books_frame = ttk.Frame(history_frame)
        borrowed_books_frame.pack(pady=10)
        self.show_borrowed_books(borrowed_books_frame)

        returned_books_frame = ttk.Frame(history_frame)
        returned_books_frame.pack(pady=10)
        self.show_returned_books(returned_books_frame)

    def show_borrowed_books(self, frame):
        query = "SELECT * FROM histori_peminjaman WHERE tanggal_kembali IS NULL"
        borrowed_books = self.fetch_history_data(query)
        ttk.Label(frame, text="Peminjaman", font=("Roboto", 12)).grid(row=0, column=0, pady=5)

        if not borrowed_books:
            ttk.Label(frame, text="Belum ada buku yang sedang dipinjam.", font=("Roboto", 10)).grid(row=1, column=0)
        else:
            for i, item in enumerate(borrowed_books, start=1):
                ttk.Label(frame, text=f"{i}. Judul: {item['book_title']}, Tanggal Peminjaman: {item['borrow_date']}", font=("Roboto", 10)).grid(row=i, column=0, pady=5)

    def show_returned_books(self, frame):
        query = "SELECT * FROM histori_peminjaman WHERE tanggal_kembali IS NOT NULL"
        returned_books = self.fetch_history_data(query)
        ttk.Label(frame, text="Pengembalian", font=("Roboto", 12)).grid(row=0, column=0, pady=5)

        if not returned_books:
            ttk.Label(frame, text="Belum ada buku yang dikembalikan.", font=("Roboto", 10)).grid(row=1, column=0)
        else:
            for i, item in enumerate(returned_books, start=1):
                ttk.Label(frame, text=f"{i}. Judul: {item['book_title']}, Tanggal Peminjaman: {item['borrow_date']}, Tanggal Pengembalian: {item['return_date']}", font=("Roboto", 10)).grid(row=i, column=0, pady=5)

    def fetch_history_data(self, query):
        conn = connection()
        cursor = conn.cursor()
        history_data = []

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            for row in result:
                book_id = row[1]
                book_query = f"SELECT judul FROM buku WHERE id = {book_id}"
                cursor.execute(book_query)
                book_result = cursor.fetchone()

                if book_result:
                    book_title = book_result[0]
                    history_data.append({
                        'book_title': book_title,
                        'borrow_date': row[3],
                        'return_date': row[4]
                    })

        except pymysql.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

        return history_data

if __name__ == "__main__":
    root = tk.Tk()
    app = PerpustakaanApp(root)
    root.mainloop()