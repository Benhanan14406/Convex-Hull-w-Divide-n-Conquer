# Tugas Pemrograman 1: Geometri Komputasional (CSCE604045)
# Topik: Algoritma Divide & Conquer untuk Convex Hull
# Bahasa: Python 3
# Library yang digunakan: random, tkinter

import random
import tkinter as tk
from tkinter import ttk


def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


def calculate_polygon_area(polygon):
    n = len(polygon)
    area = 0.0
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        area += x1 * y2 - x2 * y1

    return abs(area) / 2.0


def base_case_hull(points):
    n = len(points)

    if n <= 2:
        return list(points)

    # Kasus n == 3
    cross_val = cross_product(points[0], points[1], points[2])
    if cross_val > 0:
        return [points[0], points[1], points[2]]
    elif cross_val < 0:
        return [points[0], points[2], points[1]]
    else:
        # Jika ketiga titik segaris, ambil dua titik terluar
        sorted_p = sorted(points)
        return [sorted_p[0], sorted_p[-1]]


def merge_hulls(left_hull, right_hull):
    n1 = len(left_hull)
    n2 = len(right_hull)

    # 1. Cari titik paling kanan di hull kiri
    left_start_idx = max(range(n1), key=lambda i: (left_hull[i][0], left_hull[i][1]))
    # 2. Cari titik paling kiri di hull kanan
    right_start_idx = min(range(n2), key=lambda i: (right_hull[i][0], right_hull[i][1]))

    # Mencari Upper Tangent 
    # Garis singgung atas: tidak boleh ada titik di atas garis A[curr_left_idx] -> B[curr_right_idx]
    curr_left_idx, curr_right_idx = left_start_idx, right_start_idx
    while True:
        changed = False

        # Berjalan berlawanan jarum jam (CCW) pada hull kiri (naik)
        for _ in range(n1):
            next_a = (curr_left_idx + 1) % n1
            if cross_product(left_hull[curr_left_idx], right_hull[curr_right_idx], left_hull[next_a]) > 0:
                curr_left_idx = next_a
                changed = True
            else:
                break

        # Berjalan searah jarum jam (CW) pada hull kanan (naik)
        for _ in range(n2):
            prev_b = (curr_right_idx - 1 + n2) % n2
            if cross_product(left_hull[curr_left_idx], right_hull[curr_right_idx], right_hull[prev_b]) > 0:
                curr_right_idx = prev_b
                changed = True
            else:
                break

        if not changed:
            break

    upper_a_idx, upper_b_idx = curr_left_idx, curr_right_idx

    # Mencari Lower Tangent
    # Garis singgung bawah: tidak boleh ada titik di bawah garis A[curr_left_idx] -> B[curr_right_idx]
    curr_left_idx, curr_right_idx = left_start_idx, right_start_idx
    while True:
        changed = False

        # Berjalan searah jarum jam (CW) pada hull kiri (turun)
        for _ in range(n1):
            prev_a = (curr_left_idx - 1 + n1) % n1
            if cross_product(left_hull[curr_left_idx], right_hull[curr_right_idx], left_hull[prev_a]) < 0:
                curr_left_idx = prev_a
                changed = True
            else:
                break

        # Berjalan berlawanan jarum jam (CCW) pada hull kanan (turun)
        for _ in range(n2):
            next_b = (curr_right_idx + 1) % n2
            if cross_product(left_hull[curr_left_idx], right_hull[curr_right_idx], right_hull[next_b]) < 0:
                curr_right_idx = next_b
                changed = True
            else:
                break

        if not changed:
            break

    lower_a_idx, lower_b_idx = curr_left_idx, curr_right_idx

    # Menggabungkan titik-titik hasil tangent (urutan CCW)
    merged = []

    # Telusuri hull kiri dari upper_a_idx ke lower_a_idx (arah CCW)
    curr = upper_a_idx
    merged.append(left_hull[curr])
    while curr != lower_a_idx:
        curr = (curr + 1) % n1
        merged.append(left_hull[curr])

    # Telusuri hull kanan dari lower_b_idx ke upper_b_idx (arah CCW)
    curr = lower_b_idx
    merged.append(right_hull[curr])
    while curr != upper_b_idx:
        curr = (curr + 1) % n2
        merged.append(right_hull[curr])

    return merged


def divide_and_conquer_hull(points):
    if len(points) <= 3:
        return base_case_hull(points)

    # Tahap Divide: Bagi titik menjadi dua bagian berdasarkan median absis (X)
    mid = len(points) // 2
    left_half = points[:mid]
    right_half = points[mid:]

    # Tahap Conquer: Selesaikan convex hull masing-masing bagian secara rekursif
    left_hull = divide_and_conquer_hull(left_half)
    right_hull = divide_and_conquer_hull(right_half)

    # Tahap Combine: Gabungkan kedua sub-hull
    return merge_hulls(left_hull, right_hull)


def compute_convex_hull(points):
    # Hapus duplikasi titik dan urutkan berdasarkan x (kemudian y jika x identik)
    unique_pts = sorted(set(points))
    return divide_and_conquer_hull(unique_pts)


# GUI MENGGUNAKAN TKINTER
class ConvexHullGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Tugas 1 Geometri Komputasional: Convex Hull Divide & Conquer')
        self.root.geometry('980x720')

        # Status data titik
        self.canvas_points = []  # Menyimpan titik dalam koordinat kanvas (piksel)
        self.origin_mode = tk.StringVar(value='center')  # 'center' atau 'top_left'

        self.canvas_width = 720
        self.canvas_height = 600

        self.setup_ui()
        self.draw_canvas_axes()

    def setup_ui(self):
        # Panel Kontrol (Kiri)
        control_frame = ttk.LabelFrame(self.root, text='Panel Kontrol', padding=(10, 10))
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Pilihan Pusat Koordinat
        ttk.Label(
            control_frame,
            text='Pusat Koordinat:',
            font=('Helvetica', 10, 'bold'),
        ).pack(anchor=tk.W, pady=(0, 5))

        ttk.Radiobutton(
            control_frame,
            text='Tengah Window (Cartesian)',
            variable=self.origin_mode,
            value='center',
            command=self.on_mode_change,
        ).pack(anchor=tk.W)

        ttk.Radiobutton(
            control_frame,
            text='Sudut Kiri Atas (Screen)',
            variable=self.origin_mode,
            value='top_left',
            command=self.on_mode_change,
        ).pack(anchor=tk.W, pady=(0, 15))

        # Tombol Aksi
        ttk.Button(
            control_frame, text='Hitung Convex Hull', command=self.run_convex_hull
        ).pack(fill=tk.X, pady=4)

        ttk.Button(
            control_frame,
            text='Generate 25 Titik Acak',
            command=self.generate_random_sites,
        ).pack(fill=tk.X, pady=4)

        ttk.Button(
            control_frame,
            text='Reset / Bersihkan Kanvas',
            command=self.clear_canvas,
        ).pack(fill=tk.X, pady=4)

        # Informasi & Statistik
        info_frame = ttk.LabelFrame(
            control_frame, text='Informasi Hasil', padding=(8, 8)
        )
        info_frame.pack(fill=tk.X, pady=15)

        self.lbl_points_count = ttk.Label(
            info_frame, text='Jumlah Titik: 0', font=('Helvetica', 10)
        )
        self.lbl_points_count.pack(anchor=tk.W, pady=2)

        self.lbl_hull_vertices = ttk.Label(
            info_frame, text='Titik Hull: 0', font=('Helvetica', 10)
        )
        self.lbl_hull_vertices.pack(anchor=tk.W, pady=2)

        self.lbl_area = ttk.Label(
            info_frame,
            text='Luas Hull: 0.00 unit²',
            font=('Helvetica', 10, 'bold'),
            foreground='#007acc',
        )
        self.lbl_area.pack(anchor=tk.W, pady=4)

        # Petunjuk Penggunaan
        help_lbl = ttk.Label(
            control_frame,
            text=(
                'Petunjuk:\n'
                '1. Klik kiri kanvas untuk menambah titik.\n'
                '2. Gunakan tombol acak untuk menguji\n'
                '   syarat minimal 25 sites.\n'
                '3. Klik "Hitung Convex Hull" untuk\n'
                '   menjalankan Divide & Conquer.'
            ),
            foreground='#555555',
            justify=tk.LEFT,
        )
        help_lbl.pack(anchor=tk.W, pady=20)

        # Kanvas Gambar (Kanan)
        canvas_container = ttk.Frame(self.root, padding=(5, 5))
        canvas_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.canvas = tk.Canvas(
            canvas_container,
            bg='#ffffff',
            width=self.canvas_width,
            height=self.canvas_height,
            relief=tk.SUNKEN,
            bd=2,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def canvas_to_user_coord(self, px, py):
        if self.origin_mode.get() == 'center':
            ox = self.canvas_width / 2.0
            oy = self.canvas_height / 2.0
            return (px - ox, oy - py)  # Sumbu Y kartesian mengarah ke atas
        else:
            return (px, py)  # Sudut kiri atas sebagai (0, 0)

    def user_to_canvas_coord(self, x, y):
        if self.origin_mode.get() == 'center':
            ox = self.canvas_width / 2.0
            oy = self.canvas_height / 2.0
            return (ox + x, oy - y)
        else:
            return (x, y)

    def draw_canvas_axes(self):
        self.canvas.delete('grid_lines')
        if self.origin_mode.get() == 'center':
            mid_x = self.canvas_width / 2.0
            mid_y = self.canvas_height / 2.0
            # Garis sumbu X dan Y
            self.canvas.create_line(
                0,
                mid_y,
                self.canvas_width,
                mid_y,
                fill='#e0e0e0',
                dash=(3, 3),
                tags='grid_lines',
            )
            self.canvas.create_line(
                mid_x,
                0,
                mid_x,
                self.canvas_height,
                fill='#e0e0e0',
                dash=(3, 3),
                tags='grid_lines',
            )
            self.canvas.create_text(
                mid_x + 15,
                mid_y + 10,
                text='(0,0)',
                fill='#888888',
                font=('Helvetica', 8),
                tags='grid_lines',
            )

    def on_mode_change(self):
        self.draw_canvas_axes()
        if self.canvas.find_withtag('hull_poly'):
            self.run_convex_hull()

    def on_canvas_click(self, event):
        px, py = event.x, event.y
        self.canvas_points.append((px, py))
        self.draw_point(px, py)
        self.lbl_points_count.config(text=f'Jumlah Titik: {len(self.canvas_points)}')

    def draw_point(self, px, py, color='#1f77b4'):
        r = 4
        self.canvas.create_oval(px - r, py - r, px + r, py + r, fill=color, outline='#000000', tags='point')

    def generate_random_sites(self):
        self.clear_canvas()
        num_points = random.randint(25, 35)
        margin = 50

        for _ in range(num_points):
            px = random.randint(margin, self.canvas_width - margin)
            py = random.randint(margin, self.canvas_height - margin)
            self.canvas_points.append((px, py))
            self.draw_point(px, py)

        self.lbl_points_count.config(text=f'Jumlah Titik: {len(self.canvas_points)}')

    def run_convex_hull(self):
        if len(self.canvas_points) < 3:
            self.lbl_hull_vertices.config(text='Titik Hull: < 3')
            self.lbl_area.config(text='Luas Hull: 0.00 unit²')
            return

        # 1. Konversi titik piksel ke sistem koordinat yang aktif
        logical_points = [self.canvas_to_user_coord(px, py) for (px, py) in self.canvas_points]

        # 2. Jalankan algoritma Divide & Conquer
        hull_logical = compute_convex_hull(logical_points)

        # 3. Hitung luas poligon convex hull
        area = calculate_polygon_area(hull_logical)

        # 4. Gambar convex hull pada kanvas
        self.canvas.delete('hull_poly')
        self.canvas.delete('hull_lines')

        # Kembalikan koordinat logika hull ke koordinat kanvas
        hull_canvas = [self.user_to_canvas_coord(x, y) for (x, y) in hull_logical]
        flat_coords = [coord for pt in hull_canvas for coord in pt]

        # Gambar bidang poligon transparan dan garis batas
        if len(hull_canvas) >= 3:
            self.canvas.create_polygon(
                flat_coords,
                fill='#ffcccc',
                outline='#d62728',
                width=2,
                tags='hull_poly',
            )

            # Gambar ulang semua titik agar titik interior tetap terlihat di atas area hull.
            self.canvas.delete('point')
            for px, py in self.canvas_points:
                self.draw_point(px, py)

            # Tandai titik verteks pembentuk hull dengan warna hijau
            for px, py in hull_canvas:
                r = 5
                self.canvas.create_oval(
                    px - r,
                    py - r,
                    px + r,
                    py + r,
                    fill='#2ca02c',
                    outline='#ffffff',
                    tags='hull_lines',
                )

        # Perbarui informasi GUI
        self.lbl_hull_vertices.config(text=f'Titik Hull: {len(hull_logical)}')
        self.lbl_area.config(text=f'Luas Hull: {area:,.2f} unit²')

    def clear_canvas(self):
        self.canvas_points.clear()
        self.canvas.delete('point')
        self.canvas.delete('hull_poly')
        self.canvas.delete('hull_lines')
        self.draw_canvas_axes()
        self.lbl_points_count.config(text='Jumlah Titik: 0')
        self.lbl_hull_vertices.config(text='Titik Hull: 0')
        self.lbl_area.config(text='Luas Hull: 0.00 unit²')


if __name__ == '__main__':
    root = tk.Tk()
    app = ConvexHullGUI(root)
    root.mainloop()