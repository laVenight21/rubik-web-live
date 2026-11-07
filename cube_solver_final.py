import cv2
import kociemba
import numpy as np
import math
from math import sin, cos, pi

IMG_WIDTH = 640
IMG_HEIGHT = 360
IMG_CENTER = (IMG_WIDTH//2, IMG_HEIGHT//2)
COLORS = ["white", "yellow", "blue", "red", "green", "orange"]

# Nama warna dalam bahasa Indonesia. Hanya dipakai untuk teks yang tampil di layar.
# Nama warna di dalam kode tetap memakai bahasa Inggris karena dipakai sebagai kunci (key).
COLOR_NAMES_ID = {"white": "putih", "yellow": "kuning", "blue": "biru",
                  "red": "merah", "green": "hijau", "orange": "oranye"}

# Batas (limit) untuk keenam warna kubus. Perhatikan bahwa nilainya dalam format HSV.
low_b = np.array([105, 100, 100])
high_b = np.array([135, 255, 255])
low_r = np.array([160, 75, 75])
high_r = np.array([180, 255, 255])
low_g = np.array([55, 80, 80])
high_g = np.array([85, 255, 255])
low_o = np.array([5, 75, 75])
high_o = np.array([15, 255, 255])
low_y = np.array([20, 100, 100])
high_y = np.array([40, 255, 255])
low_w = np.array([0, 0, 150])
high_w = np.array([180, 60, 255])

# Class Cube merepresentasikan Rubik's Cube itu sendiri. Kubus punya enam sisi yang disimpan
# dalam atribut bernama state, yaitu kondisi (acakan) kubus saat ini.
# Sisi kubus biasanya disebut berdasarkan warna bidak tengahnya (misalnya sisi biru) atau
# berdasarkan posisinya relatif terhadap pengguna (misalnya sisi depan). Dalam program ini
# posisi sisi dianggap seperti berikut: putih = atas (up); biru = depan (front);
# oranye = kanan (right); hijau = belakang (back); merah = kiri (left); kuning = bawah (down).
# Ini menjelaskan pemakaian huruf U, F, R, B, L dan D di dalam program. Logika notasi putaran:
# U berarti memutar sisi atas searah jarum jam dan U' (U-prime) berarti memutarnya berlawanan
# arah jarum jam. Huruf x dan y di antara putaran berarti memutar seluruh kubus pada sumbu x
# atau sumbu y. Solusi sebenarnya diambil dari fungsi 'solve' milik library Kociemba.

class Cube:
    def __init__(self):
        empty_face = np.empty([3, 3], '<U6')
        
        self.state = {"white": empty_face, "orange": empty_face, "blue": empty_face,
                      "yellow": empty_face, "red": empty_face, "green": empty_face}
    
    def save_face(self, color, face):
        self.state[color] = face

    def get_face(self, color):
        return self.state[color]
    
    def print_state(self):
        print("Kondisi kubus:")
        for color in self.state:
            print()
            print(f"sisi {color}:")
            print()
            count = 0
            for i in range(3):
                print("    | ", end="")
                for j in range(3):
                    print(self.state[color][i][j], end=" | ")
                    if j == 2:
                        print()

    def color_to_letter(self, color):
        if color == "blue":
            return "F"
        if color == "green":
            return "B"
        if color == "white":
            return "U"
        if color == "yellow":
            return "D"
        if color == "red":
            return "L"
        if color == "orange":
            return "R"

    def get_solution(self):

        state_str = ''
        for color in self.state:
            face = self.state[color]
            for i in range(3):
                for j in range(3):
                    state_str += self.color_to_letter(face[i][j])


        solution = kociemba.solve(state_str)

        return solution

    
    def call_turn(self, turn):
        prime = False
        if len(turn) > 2:
            print("Perintah tidak dikenal")
            return
        if len(turn) == 2:
            if turn[1] == "'":
                turn = turn[0]
                prime = True
            elif turn[1] == "2":
                turn = turn[0] + turn[0]
            else:
                print("Perintah tidak dikenal")
                return

        for letter in turn:
            
            if letter == "R":
                self.right_turn(prime)
            elif letter == "L":
                self.left_turn(prime)
            elif letter == "U":
                self.up_turn(prime)
            elif letter == "D":
                self.down_turn(prime)
            elif letter == "F":
                self.front_turn(prime)
            elif letter == "B":
                self.back_turn(prime)
            else:
                print("Perintah tidak dikenal")
                return
        return
    
    def right_turn(self, prime):
        old_blue = self.state["blue"].copy()
        old_white = self.state["white"].copy()
        old_green = self.state["green"].copy()
        old_yellow = self.state["yellow"].copy()
        
        new_blue = old_blue.copy()
        new_white = old_white.copy()
        new_green = old_green.copy()
        new_yellow = old_yellow.copy()

        for i in range(3):
            i_reversed = abs(i - 2)

            if prime:
                new_yellow[i][2] = old_blue[i][2]
                new_blue[i][2] = old_white[i][2]
                new_white[i][2] = old_green[i_reversed][0]
                new_green[i][0] = old_yellow[i_reversed][2]
            else:
                new_blue[i][2] = old_yellow[i][2]
                new_white[i][2] = old_blue[i][2]
                new_green[i][0] = old_white[i_reversed][2]
                new_yellow[i][2] = old_green[i_reversed][0]
      
        old_orange = self.state["orange"].copy()
        new_orange = initialize_face()
        for i in range(3):
            i_reversed = abs(i - 2)
            for j in range(3):
                j_reversed = abs(j - 2)
                if prime:
                    new_orange[i][j] = old_orange[j][i_reversed]
                else:
                    new_orange[i][j] = old_orange[j_reversed][i]

        self.save_face("blue", new_blue)
        self.save_face("white", new_white)
        self.save_face("green", new_green)
        self.save_face("yellow", new_yellow)
        self.save_face("orange", new_orange)

    def left_turn(self, prime):
        old_blue = self.state["blue"].copy()
        old_white = self.state["white"].copy()
        old_green = self.state["green"].copy()
        old_yellow = self.state["yellow"].copy()
        
        new_blue = old_blue.copy()
        new_white = old_white.copy()
        new_green = old_green.copy()
        new_yellow = old_yellow.copy()

        for i in range(3):
            i_reversed = abs(i - 2)

            if prime:
                new_blue[i][0] = old_yellow[i][0]
                new_white[i][0] = old_blue[i][0]
                new_green[i][2] = old_white[i_reversed][0]
                new_yellow[i][0] = old_green[i_reversed][2]
            else:
                new_yellow[i][0] = old_blue[i][0]
                new_blue[i][0] = old_white[i][0]
                new_white[i][0] = old_green[i_reversed][2]
                new_green[i][2] = old_yellow[i_reversed][0]
      
        old_red = self.state["red"].copy()
        new_red = initialize_face()
        for i in range(3):
            i_reversed = abs(i - 2)
            for j in range(3):
                j_reversed = abs(j - 2)
                if prime:
                    new_red[i][j] = old_red[j][i_reversed]
                else:
                    new_red[i][j] = old_red[j_reversed][i]

        self.save_face("blue", new_blue)
        self.save_face("white", new_white)
        self.save_face("green", new_green)
        self.save_face("yellow", new_yellow)
        self.save_face("red", new_red)

    def up_turn(self, prime):
        old_blue = self.state["blue"].copy()
        old_red = self.state["red"].copy()
        old_green = self.state["green"].copy()
        old_orange = self.state["orange"].copy()
        
        new_blue = old_blue.copy()
        new_red = old_red.copy()
        new_green = old_green.copy()
        new_orange = old_orange.copy()

        for j in range(3):

            if prime:
                new_orange[0][j] = old_blue[0][j]
                new_blue[0][j] = old_red[0][j]
                new_red[0][j] = old_green[0][j]
                new_green[0][j] = old_orange[0][j]
            else:
                new_blue[0][j] = old_orange[0][j]
                new_red[0][j] = old_blue[0][j]
                new_green[0][j] = old_red[0][j]
                new_orange[0][j] = old_green[0][j]
      
        old_white = self.state["white"].copy()
        new_white = initialize_face()
        for i in range(3):
            i_reversed = abs(i - 2)
            for j in range(3):
                j_reversed = abs(j - 2)
                if prime:
                    new_white[i][j] = old_white[j][i_reversed]
                else:
                    new_white[i][j] = old_white[j_reversed][i]

        self.save_face("blue", new_blue)
        self.save_face("red", new_red)
        self.save_face("green", new_green)
        self.save_face("orange", new_orange)
        self.save_face("white", new_white)

    def down_turn(self, prime):
        old_blue = self.state["blue"].copy()
        old_red = self.state["red"].copy()
        old_green = self.state["green"].copy()
        old_orange = self.state["orange"].copy()
        
        new_blue = old_blue.copy()
        new_red = old_red.copy()
        new_green = old_green.copy()
        new_orange = old_orange.copy()

        for j in range(3):

            if prime:
                new_blue[2][j] = old_orange[2][j]
                new_red[2][j] = old_blue[2][j]
                new_green[2][j] = old_red[2][j]
                new_orange[2][j] = old_green[2][j]
            else:
                new_orange[2][j] = old_blue[2][j]
                new_blue[2][j] = old_red[2][j]
                new_red[2][j] = old_green[2][j]
                new_green[2][j] = old_orange[2][j]
                
        old_yellow = self.state["yellow"].copy()
        new_yellow = initialize_face()
        for i in range(3):
            i_reversed = abs(i - 2)
            for j in range(3):
                j_reversed = abs(j - 2)
                if prime:
                    new_yellow[i][j] = old_yellow[j][i_reversed]
                else:
                    new_yellow[i][j] = old_yellow[j_reversed][i]

        self.save_face("blue", new_blue)
        self.save_face("red", new_red)
        self.save_face("green", new_green)
        self.save_face("orange", new_orange)
        self.save_face("yellow", new_yellow)

    def front_turn(self, prime):
        old_red = self.state["red"].copy()
        old_white = self.state["white"].copy()
        old_orange = self.state["orange"].copy()
        old_yellow = self.state["yellow"].copy()
        
        new_red = old_red.copy()
        new_white = old_white.copy()
        new_orange = old_orange.copy()
        new_yellow = old_yellow.copy()

        for i in range(3):
            i_reversed = abs(i - 2)

            if prime:
                new_yellow[0][i] = old_red[i][2]
                new_red[i][2] = old_white[2][i_reversed]
                new_white[2][i] = old_orange[i][0]
                new_orange[i][0] = old_yellow[0][i_reversed]
            else:
                new_red[i][2] = old_yellow[0][i]
                new_white[2][i] = old_red[i_reversed][2]
                new_orange[i][0] = old_white[2][i]
                new_yellow[0][i] = old_orange[i_reversed][0]
      
        old_blue = self.state["blue"].copy()
        new_blue = initialize_face()
        for i in range(3):
            i_reversed = abs(i - 2)
            for j in range(3):
                j_reversed = abs(j - 2)
                if prime:
                    new_blue[i][j] = old_blue[j][i_reversed]
                else:
                    new_blue[i][j] = old_blue[j_reversed][i]

        self.save_face("red", new_red)
        self.save_face("white", new_white)
        self.save_face("orange", new_orange)
        self.save_face("yellow", new_yellow)
        self.save_face("blue", new_blue)

    def back_turn(self, prime):
        old_red = self.state["red"].copy()
        old_white = self.state["white"].copy()
        old_orange = self.state["orange"].copy()
        old_yellow = self.state["yellow"].copy()
        
        new_red = old_red.copy()
        new_white = old_white.copy()
        new_orange = old_orange.copy()
        new_yellow = old_yellow.copy()

        for i in range(3):
            i_reversed = abs(i - 2)

            if prime:
                new_red[i][0] = old_yellow[2][i]
                new_white[0][i] = old_red[i_reversed][0]
                new_orange[i][2] = old_white[0][i]
                new_yellow[2][i] = old_orange[i_reversed][2]
            else:
                new_yellow[2][i] = old_red[i][0]
                new_red[i][0] = old_white[0][i_reversed]
                new_white[0][i] = old_orange[i][2]
                new_orange[i][2] = old_yellow[2][i_reversed]
      
        old_green = self.state["green"].copy()
        new_green = initialize_face()
        for i in range(3):
            i_reversed = abs(i - 2)
            for j in range(3):
                j_reversed = abs(j - 2)
                if prime:
                    new_green[i][j] = old_green[j][i_reversed]
                else:
                    new_green[i][j] = old_green[j_reversed][i]

        self.save_face("red", new_red)
        self.save_face("white", new_white)
        self.save_face("orange", new_orange)
        self.save_face("yellow", new_yellow)
        self.save_face("green", new_green)

        return
    
    def copy(self, cube_to_copy):
        for color in self.state:
            self.state[color] = cube_to_copy.get_face(color).copy()
        return


cube = Cube()

# Mengembalikan nilai boolean apakah contour_a berada di dalam contour_b.
def contour_in_contour(contour_a, contour_b):
    for point_as_array in contour_a:
        point = (float(point_as_array[0][0]), float(point_as_array[0][1]))
        if cv2.pointPolygonTest(contour_b, point, False) < 0:
            return False
    return True
    
def distance(point_a, point_b):
    x_a, y_a = point_a
    x_b, y_b = point_b
    dist = math.sqrt((x_a - x_b)**2 + (y_a - y_b)**2)
    return dist

# Fungsi ini dipakai untuk memeriksa apakah setiap bidak pada sebuah sisi sudah terdeteksi
# setelah proses inisialisasi.
def detection_completed(face):
    for i in range(3):
        for j in range(3):
            if face[i][j] == "init":
                return False
    return True

def initialize_face():
    face = np.empty([3, 3], '<U6')
    for i in range(3):
        for j in range(3):
            face[i][j] = "init"
    return face


# Fungsi ini dipakai untuk memeriksa apakah sebuah contour punya parent, yaitu contour
# pembungkus dengan warna yang sama di dalam sisi tersebut. Ini berguna pada situasi rumit
# ketika bidak tengah misalnya biru dan semua bidak lain pada sisi itu misalnya merah.
# Pada situasi itu program mudah tertipu dan menyimpulkan bahwa bidak tengah juga merah,
# karena bidak tengah berada di dalam contour merah (bagian dalam) yang ukurannya kira-kira
# sebesar bidak tengah. Situasi unik ini bisa dikenali dengan memeriksa siapa parent dari
# lingkaran merah bagian dalam tersebut. Kalau parent-nya berukuran sebesar sisi kubus,
# disimpulkan bahwa bidak tengah punya warna yang berbeda (dalam contoh ini biru).
def parents_inside_face(contour_array, hierarchy_array, index, contour_face):
    hierarchy_i = hierarchy_array[0][index]
    index_of_parent = hierarchy_i[3]
    # Kalau sama sekali tidak ada parent, indeksnya -1
    if index_of_parent == -1:
        return False
    
    contour_parent = contour_array[index_of_parent]
    if contour_in_contour(contour_parent, contour_face):
        return True
    
    return False

                
# Fungsi ini membuat dan mengembalikan mask untuk keenam warna kubus. Mask ini dipakai
# untuk mengenali warna bidak.
def get_masks(img):
    mask_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_blue = cv2.inRange(mask_img, low_b, high_b)
    mask_green = cv2.inRange(mask_img, low_g, high_g)
    mask_orange = cv2.inRange(mask_img, low_o, high_o)
    mask_yellow = cv2.inRange(mask_img, low_y, high_y)
    mask_white = cv2.inRange(mask_img, low_w, high_w)

    # Batas warna (variabel global di atas) bisa berbeda tergantung pencahayaan
    # lingkungan. Kadang nilai hue terbaik melewati nol (atau melewati 180 derajat, yang
    # sama saja). Dalam kasus itu mask merah harus dibuat dari dua mask terpisah: satu dari
    # batas "bawah" sampai 180 derajat, dan satu dari nol (180) derajat sampai batas "atas".
    if high_r[0] > 180:
        low_r_1 = low_r
        low_r_2 = np.array([0, low_r[1], low_r[2]])
        high_r_1 = np.array([180, high_r[1], high_r[2]])
        high_r_2 = np.array([high_r[0] - 180, high_r[1], high_r[2]])
        mask_red_1 = cv2.inRange(mask_img, low_r_1, high_r_1)
        mask_red_2 = cv2.inRange(mask_img, low_r_2, high_r_2)
        mask_red = cv2.bitwise_or(mask_red_1, mask_red_2)

    else:
        mask_red = cv2.inRange(mask_img, low_r, high_r)


    return mask_blue, mask_red, mask_green, mask_orange, mask_yellow, mask_white

# Fungsi ini membuat struktur data yang bisa dipakai untuk menelusuri semua contour dari
# warna tertentu beserta vektor hierarki tiap contour (yang dipakai saat mencari parent
# dari contour).
def get_piece_contours_info(masks):
    contours_blue, hierarchy_blue = cv2.findContours(masks[0], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, hierarchy_red = cv2.findContours(masks[1], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, hierarchy_green = cv2.findContours(masks[2], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_orange, hierarchy_orange = cv2.findContours(masks[3], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, hierarchy_yellow = cv2.findContours(masks[4], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_white, hierarchy_white = cv2.findContours(masks[5], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    piece_contours_info = {'blue': [contours_blue, hierarchy_blue],
                        'red': [contours_red, hierarchy_red],
                        'green': [contours_green, hierarchy_green],
                        'orange': [contours_orange, hierarchy_orange],
                        'yellow': [contours_yellow, hierarchy_yellow],
                        'white': [contours_white, hierarchy_white]}
    return piece_contours_info

# Fungsi ini membuat dan mengembalikan teks instruksi berdasarkan warna pusat yang perlu
# ditunjukkan ke kamera. Logikanya mengikuti aturan pada komentar class Cube:
# putih => atas, biru => depan, dst. Sisi yang menghadap ke atas harus benar saat sebuah
# sisi ditunjukkan ke kamera, kalau tidak, sisi yang terlihat tidak bisa ditafsirkan dengan pasti.
def get_instruction_text(color):
    if (color == "blue" or
        color == "red" or
        color == "green" or
        color == "orange"):
        center_facing_up = "white"
    elif color == "white":
        center_facing_up = "green"
    else: # jika center_color == yellow
        center_facing_up = "blue"
    text = (f"Tunjukkan sisi {COLOR_NAMES_ID[color]}, "
            f"pusat {COLOR_NAMES_ID[center_facing_up]} menghadap ke atas")
    return text

# Fungsi ini menggambar teks instruksi di atas gambar dengan huruf putih di atas latar hitam.
def draw_text(img, text, origin):

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 1
    top_left_x = origin[0]
    top_left_y = origin[1]
    bg_color = (0, 0, 0)
    text_color = (255, 255, 255)
    size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    w, h = size
    text_bottom_left = point_type_converter((top_left_x, top_left_y + 1.2*h), float_to_int=True)
    rect_top_left = (top_left_x, top_left_y)
    rect_bottom_right = point_type_converter((top_left_x + w, top_left_y + 1.5*h), float_to_int=True)

    cv2.rectangle(img, rect_top_left, rect_bottom_right, bg_color, -1)
    cv2.putText(img, text, text_bottom_left, font, font_scale, text_color, font_thickness)

    return

# Fungsi ini menelusuri semua bidak tengah dan mendeteksi sisi di sekitarnya dengan
# fungsi detect_face(), yaitu fungsi tempat hampir semua proses computer vision terjadi.
def detect_cube(video):

    for color in COLORS:

        while True:

            cmd, face = detect_face(video, color)


            if cmd == "quit":
                return "quit"
            if cmd == "failed":
                return "failed"
            if cmd == "restart":
                continue
            if cmd == "completed":
                cube.save_face(color, face)
                break
        
    return "detected"

# Fungsi ini dipanggil dari detect_face() untuk menginisialisasi luas relatif contour yang
# dipakai dalam deteksi. Luasnya relatif terhadap luas seluruh sisi. 1.0 atau 100 % adalah
# nilai awal yang bagus karena selama deteksi dicari luas relatif yang paling kecil, dan
# setiap kali ditemukan nilai yang lebih kecil, nilai lama diganti dengannya.
def initialize_areas():
    relative_max = 1.0
    area_array = np.empty([3,3])
    for i in range(3):
        for j in range(3):
            area_array[i][j] = relative_max
    return area_array

# Fungsi ini mengembalikan nilai boolean apakah face_a dan face_b identik.
def faces_match(face_a, face_b):
    for i in range(3):
        for j in range(3):
            if face_a[i][j] != face_b[i][j]:
                return False
    return True


def reverse_dict(og_dict):
    list_of_items = list(og_dict.items())
    reversed_list_of_items = reversed(list_of_items)
    reversed_dict = dict(reversed_list_of_items)
    return reversed_dict

def deg_to_rad(a_deg):
    a_rad = a_deg / 180 * pi
    return a_rad

# Fungsi ini bertugas menemukan kubus di dalam gambar dan menghitung koordinat titik pusat
# tiap bidak. Fungsi ini mengembalikan tiga nilai:
# 1) boolean apakah sebuah sisi ditemukan
# 2) contour dari sisi tersebut
# 3) array numpy berisi titik pusat bidak

# ---------------------------------------------------------------------------
# Fungsi bantu deteksi sisi Rubik
# ---------------------------------------------------------------------------
# Deteksi tidak lagi menganggap semua area terang sebagai satu objek. Program
# mencari kandidat stiker berbentuk kotak dari beberapa hasil threshold, lalu
# memeriksa apakah kandidat-kandidat tersebut benar-benar membentuk pola 3x3.
# Fungsi utama tetap mengembalikan (found, contour_face, piece_centers), jadi
# detect_face(), make_turn(), pembacaan warna, dan solver tidak perlu diubah.

_DET_MIN_STICKER_SIDE = 7.0
_DET_MAX_STICKER_SIDE = 0.42 * min(IMG_WIDTH, IMG_HEIGHT)
_DET_MIN_CELLS = 6
_DET_MAX_GRID_ERROR = 0.36
_DET_MAX_CENTER_OFFSET = 0.44


def _rubik_contour_candidates(mask, max_side):
    """Ambil kandidat bidang kotak dari sebuah mask."""
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    found = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 55:
            continue

        rect = cv2.minAreaRect(contour)
        (cx, cy), (rw, rh), _ = rect
        if rw <= 0 or rh <= 0:
            continue

        short_side = min(rw, rh)
        long_side = max(rw, rh)
        if short_side < _DET_MIN_STICKER_SIDE or long_side > max_side:
            continue
        if long_side / short_side > 1.65:
            continue

        rect_area = rw * rh
        fill_ratio = area / max(rect_area, 1.0)
        if fill_ratio < 0.42:
            continue

        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            continue
        approx = cv2.approxPolyDP(contour, 0.045 * perimeter, True)
        if len(approx) < 4 or len(approx) > 10:
            continue

        side = (rw + rh) / 2.0
        # Kualitas dipakai hanya untuk memilih kandidat terbaik jika beberapa
        # threshold menemukan stiker yang sama.
        square_score = 1.0 - min(1.0, abs(long_side / short_side - 1.0))
        quality = 0.65 * fill_ratio + 0.35 * square_score
        found.append((float(cx), float(cy), float(side), float(quality)))

    return found


def _collect_rubik_sticker_candidates(img):
    """Temukan kandidat stiker dengan threshold terang dan tepi lokal."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    value = hsv[:, :, 2]
    height, width = gray.shape[:2]
    max_side = min(_DET_MAX_STICKER_SIDE, 0.46 * min(width, height))

    candidates = []

    # Otsu membantu menyesuaikan threshold terhadap kondisi terang/gelap.
    otsu_value, _ = cv2.threshold(
        value, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    thresholds = {
        max(35, min(175, int(otsu_value * 0.62))),
        max(45, min(190, int(otsu_value * 0.82))),
        max(55, min(205, int(otsu_value))),
    }

    kernel = np.ones((3, 3), np.uint8)
    for threshold in sorted(thresholds):
        mask = cv2.inRange(value, threshold, 255)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        candidates.extend(_rubik_contour_candidates(mask, max_side))

    # Threshold adaptif membantu saat pencahayaan tidak merata pada sebagian
    # sisi Rubik. Tidak menggunakan segmentasi warna agar tetap berlaku untuk
    # keenam warna stiker.
    adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, -5
    )
    adaptive = cv2.morphologyEx(adaptive, cv2.MORPH_OPEN, kernel, iterations=1)
    candidates.extend(_rubik_contour_candidates(adaptive, max_side))

    # Tepi dipakai sebagai jalur tambahan jika warna stiker dan pencahayaan
    # membuat hasil threshold terang kurang jelas.
    edges = cv2.Canny(gray, 35, 105)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)
    candidates.extend(_rubik_contour_candidates(edges, max_side))

    # Hilangkan kandidat duplikat dari beberapa threshold. Jarak pusat stiker
    # yang berbeda biasanya jauh lebih besar daripada toleransi ini.
    candidates.sort(key=lambda item: (item[3], item[2]), reverse=True)
    unique = []
    for candidate in candidates:
        cx, cy, side, quality = candidate
        duplicate_index = None
        for index, existing in enumerate(unique):
            ex, ey, eside, eq = existing
            distance_px = math.hypot(cx - ex, cy - ey)
            if distance_px < 0.38 * min(side, eside):
                duplicate_index = index
                break
        if duplicate_index is None:
            unique.append(candidate)
        else:
            ex, ey, eside, eq = unique[duplicate_index]
            # Jika kualitasnya hampir sama, kontur yang sedikit lebih besar
            # biasanya mengikuti tepi luar stiker dengan lebih baik.
            if quality > eq + 0.04 or (abs(quality - eq) <= 0.04 and side > eside):
                unique[duplicate_index] = candidate

    # Membatasi jumlah kandidat menjaga waktu pencarian tetap ringan pada
    # latar yang ramai.
    unique.sort(key=lambda item: item[3], reverse=True)
    return unique[:90]


def _group_projected_values(values, tolerance):
    """Kelompokkan koordinat 1D yang seharusnya berada pada satu baris/kolom."""
    ordered = sorted((float(value), index) for index, value in enumerate(values))
    groups = []
    for value, index in ordered:
        if not groups or value - float(np.median([item[0] for item in groups[-1]])) > tolerance:
            groups.append([(value, index)])
        else:
            groups[-1].append((value, index))
    return groups


def _choose_three_grid_lines(groups, sticker_side):
    """Pilih tiga garis paling teratur, meskipun ada kandidat pengganggu."""
    if len(groups) < 3:
        return None

    best_groups = None
    best_score = -float('inf')

    for a in range(len(groups) - 2):
        for b in range(a + 1, len(groups) - 1):
            for c in range(b + 1, len(groups)):
                selected = [groups[a], groups[b], groups[c]]
                centers = [float(np.median([item[0] for item in group]))
                           for group in selected]
                gap_1 = centers[1] - centers[0]
                gap_2 = centers[2] - centers[1]
                if min(gap_1, gap_2) < 0.62 * sticker_side:
                    continue
                if max(gap_1, gap_2) > 2.65 * sticker_side:
                    continue
                gap_ratio = max(gap_1, gap_2) / max(min(gap_1, gap_2), 1.0)
                if gap_ratio > 1.75:
                    continue

                mean_gap = (gap_1 + gap_2) / 2.0
                regularity_penalty = abs(gap_1 - gap_2) / max(mean_gap, 1.0)
                expected_pitch_penalty = abs(mean_gap / sticker_side - 1.15)
                support = sum(min(len(group), 3) for group in selected)
                score = (support * 2.0 - regularity_penalty * 3.0
                         - expected_pitch_penalty * 1.2)
                if score > best_score:
                    best_score = score
                    best_groups = selected

    return best_groups


def _fit_rubik_grid(candidate_group):
    """Validasi pola 3x3 dan hitung empat sudut serta sembilan pusat stiker."""
    if len(candidate_group) < _DET_MIN_CELLS:
        return None

    sticker_side = float(np.median([item[2] for item in candidate_group]))
    if sticker_side < _DET_MIN_STICKER_SIDE:
        return None

    points = np.asarray([[item[0], item[1]] for item in candidate_group], dtype=np.float32)

    # Arah baris/kolom dicari dari pasangan stiker bertetangga. Sudut dinormalisasi
    # setiap 90 derajat sehingga arah horizontal dan vertikal memberi estimasi sama.
    angles = []
    for i in range(len(points) - 1):
        delta = points[i + 1:] - points[i]
        distances = np.linalg.norm(delta, axis=1)
        for vector, distance_px in zip(delta, distances):
            if 0.76 * sticker_side <= distance_px <= 1.48 * sticker_side:
                angle = math.degrees(math.atan2(float(vector[1]), float(vector[0])))
                angle = ((angle + 45.0) % 90.0) - 45.0
                angles.append(angle)

    angle_deg = float(np.median(angles)) if angles else 0.0
    if abs(angle_deg) > 35.0:
        return None

    angle_rad = math.radians(angle_deg)
    axis_x = np.asarray([math.cos(angle_rad), math.sin(angle_rad)], dtype=np.float32)
    axis_y = np.asarray([-math.sin(angle_rad), math.cos(angle_rad)], dtype=np.float32)
    if axis_y[1] < 0:
        axis_y *= -1

    projected_x = points @ axis_x
    projected_y = points @ axis_y
    line_tolerance = max(4.0, 0.40 * sticker_side)
    x_groups = _group_projected_values(projected_x, line_tolerance)
    y_groups = _group_projected_values(projected_y, line_tolerance)
    selected_x = _choose_three_grid_lines(x_groups, sticker_side)
    selected_y = _choose_three_grid_lines(y_groups, sticker_side)
    if selected_x is None or selected_y is None:
        return None

    x_lines = [float(np.median([item[0] for item in group])) for group in selected_x]
    y_lines = [float(np.median([item[0] for item in group])) for group in selected_y]

    # Satu kandidat terbaik untuk setiap sel. Duplikasi/objek latar pada lokasi
    # yang sama tidak menambah jumlah stiker yang dianggap valid.
    cells = {}
    for idx, candidate in enumerate(candidate_group):
        x_value = float(projected_x[idx])
        y_value = float(projected_y[idx])
        col = int(np.argmin([abs(x_value - line) for line in x_lines]))
        row = int(np.argmin([abs(y_value - line) for line in y_lines]))
        dx = abs(x_value - x_lines[col])
        dy = abs(y_value - y_lines[row])
        if dx > 1.45 * line_tolerance or dy > 1.45 * line_tolerance:
            continue

        cell_error = math.hypot(dx, dy)
        key = (row, col)
        previous = cells.get(key)
        candidate_score = candidate[3] - 0.04 * cell_error / max(sticker_side, 1.0)
        if previous is None or candidate_score > previous[0]:
            cells[key] = (candidate_score, candidate)

    if len(cells) < _DET_MIN_CELLS:
        return None
    if {row for row, _ in cells} != {0, 1, 2}:
        return None
    if {col for _, col in cells} != {0, 1, 2}:
        return None

    grid_xy = []
    image_xy = []
    for (row, col), (_, candidate) in cells.items():
        grid_xy.append([1.0, float(col), float(row)])
        image_xy.append([candidate[0], candidate[1]])

    design = np.asarray(grid_xy, dtype=np.float64)
    observed = np.asarray(image_xy, dtype=np.float64)
    if np.linalg.matrix_rank(design) < 3:
        return None

    coefficients, _, _, _ = np.linalg.lstsq(design, observed, rcond=None)
    predicted = design @ coefficients
    residuals = np.linalg.norm(predicted - observed, axis=1)
    rms_error = float(np.sqrt(np.mean(residuals ** 2)))
    if rms_error > max(5.0, _DET_MAX_GRID_ERROR * sticker_side):
        return None

    origin = coefficients[0]
    vector_x = coefficients[1]
    vector_y = coefficients[2]
    pitch_x = float(np.linalg.norm(vector_x))
    pitch_y = float(np.linalg.norm(vector_y))
    if not (0.68 * sticker_side <= pitch_x <= 2.45 * sticker_side):
        return None
    if not (0.68 * sticker_side <= pitch_y <= 2.45 * sticker_side):
        return None
    if max(pitch_x, pitch_y) / max(min(pitch_x, pitch_y), 1.0) > 1.55:
        return None

    # Pastikan orientasi indeks tetap kiri-ke-kanan dan atas-ke-bawah seperti
    # yang diharapkan detect_face() pada kode asli.
    if vector_x[0] < 0:
        return None
    if vector_y[1] < 0:
        return None

    coverage = len(cells)
    quality = float(np.mean([value[1][3] for value in cells.values()]))
    score = coverage * 3.0 + quality - 2.0 * (rms_error / max(sticker_side, 1.0))
    return origin, vector_x, vector_y, rms_error, sticker_side, score, coverage


def find_face_and_get_centers(img, marginal=20):
    """Cari sisi Rubik 3x3 dan kembalikan pusat tiap stiker.

    Parameter dan format return sengaja dipertahankan agar seluruh bagian lain
    dari program tetap kompatibel.
    """
    if img is None or img.size == 0:
        return False, None, None

    height, width = img.shape[:2]
    candidates = _collect_rubik_sticker_candidates(img)
    if len(candidates) < _DET_MIN_CELLS:
        return False, None, None

    best_fit = None
    best_score = -float('inf')
    seen_groups = set()

    # Setiap kandidat dijadikan titik awal pencarian lokal. Ini lebih tahan
    # terhadap benda terang di latar dibanding menggabungkan semua area terang.
    for seed in candidates:
        sx, sy, seed_side, _ = seed
        local_group = []
        for candidate in candidates:
            cx, cy, side, _ = candidate
            size_ratio = side / max(seed_side, 1.0)
            if not (0.58 <= size_ratio <= 1.72):
                continue
            if math.hypot(cx - sx, cy - sy) <= 3.85 * seed_side:
                local_group.append(candidate)

        if len(local_group) < _DET_MIN_CELLS:
            continue
        group_key = tuple(candidates.index(item) for item in local_group)
        if group_key in seen_groups:
            continue
        seen_groups.add(group_key)

        fit = _fit_rubik_grid(local_group)
        if fit is not None and fit[5] > best_score:
            best_fit = fit
            best_score = fit[5]

    if best_fit is None:
        return False, None, None

    origin, vector_x, vector_y, rms_error, sticker_side, score, coverage = best_fit
    face_center = origin + vector_x + vector_y
    center_offset = math.hypot(
        float(face_center[0]) - width / 2.0,
        float(face_center[1]) - height / 2.0
    )
    if center_offset > _DET_MAX_CENTER_OFFSET * min(width, height):
        return False, None, None

    # Pusat stiker berada pada indeks (0..2, 0..2), sehingga batas sisi Rubik
    # diperkirakan setengah jarak antarpusat di luar stiker terluar.
    top_left = origin - 0.5 * vector_x - 0.5 * vector_y
    top_right = origin + 2.5 * vector_x - 0.5 * vector_y
    bottom_right = origin + 2.5 * vector_x + 2.5 * vector_y
    bottom_left = origin - 0.5 * vector_x + 2.5 * vector_y
    box_float = np.asarray(
        [top_left, top_right, bottom_right, bottom_left], dtype=np.float32
    )

    face_area = abs(float(cv2.contourArea(box_float)))
    if face_area < 2200 or face_area > 0.82 * width * height:
        return False, None, None

    # Jangan menerima kandidat yang sebagian besar berada di luar area kamera.
    if (np.min(box_float[:, 0]) < -25 or np.max(box_float[:, 0]) > width + 25
            or np.min(box_float[:, 1]) < -25 or np.max(box_float[:, 1]) > height + 25):
        return False, None, None

    box = np.int32(np.round(box_float)).reshape((-1, 1, 2))
    piece_centers = np.empty((3, 3), dtype='f,f')

    cv2.drawContours(img, [box], 0, (0, 0, 100), 2)
    for row in range(3):
        for col in range(3):
            point = origin + col * vector_x + row * vector_y
            piece_centers[row][col] = (float(point[0]), float(point[1]))
            cv2.circle(
                img, (int(round(point[0])), int(round(point[1]))),
                radius=2, color=(0, 0, 255), thickness=-1
            )

    return True, box, piece_centers


# Fungsi ini membentuk gambar ke format yang diinginkan dari keluaran video webcam.
def get_img(video):
    is_ok, img = video.read()

    if not is_ok:
        print("Gagal membaca video")
        return False, img

    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    img = cv2.flip(img, 1)

    return True, img

# Fungsi ini dipanggil terpisah untuk tiap enam sisi (ditentukan oleh warna pusat)
# kubus. Masukannya adalah gambar video dari webcam dan warna pusat dari sisi yang harus
# dideteksi. Nilai kembalian pertama berisi informasi apakah deteksi berhasil, atau
# terhenti karena error atau perintah 'q' dari pengguna. Nilai kembalian kedua adalah
# array numpy 3 x 3 yang merepresentasikan sisi yang terdeteksi.

# Fungsi ini mencetak sisi yang terdeteksi sebagaimana tampil di layar. Perhatikan bahwa
# sisi yang sebenarnya disimpan ke objek Cube adalah sisi seperti di dunia nyata
# (tidak dicerminkan).
def print_mirrored_face(og_face):
    mirrored_face = initialize_face()
    for i in range(3):
        for j in range(3):
            j_reversed = abs(j - 2)
            mirrored_face[i][j] = og_face[i][j_reversed]
    print()
    print("sisi (dicerminkan seperti di layar):")
    print(mirrored_face)

def detect_face(video, center_color):
    # Detected berarti fungsi sudah menghasilkan suatu deteksi sisi. Verified
    # berarti pengguna sudah memastikan bahwa deteksinya benar dan sisi tersebut boleh
    # disimpan ke objek Cube.
    detected = False
    verified = False

    face = initialize_face()
    face_to_return = initialize_face()
    relative_areas = initialize_areas()
    instruction_text = get_instruction_text(center_color)
    while True:
        success, img = get_img(video)
        if not success:
            return "failed", None
        draw_text(img, instruction_text, origin = (10, 10))
        
        # Ketika sisi sudah terdeteksi tetapi belum diverifikasi, satu-satunya yang dilakukan
        # fungsi ini adalah menunggu pengguna memverifikasinya atau mengulang deteksi
        # dengan perintah keyboard.
        if detected == verified:
        
            masks = get_masks(img)
            face_found, contour_face, piece_centers = find_face_and_get_centers(img)
            piece_contours_info = get_piece_contours_info(masks)


            # Ini biasanya berarti ada gerakan pada kubus (diputar atau dirotasi), sehingga
            # sekarang saatnya menginisialisasi proses deteksi untuk mendeteksi
            # bidak-bidak dari sisi baru yang terlihat.
            if not face_found:
                face = initialize_face()
                relative_areas = initialize_areas()
            else:
                area_face = cv2.contourArea(contour_face)
                min_piece_area = 0.08*area_face
                piece_contours_info = get_piece_contours_info(masks)

                for color in piece_contours_info:
                    contours_i = piece_contours_info[color][0]
                    hierarchy_array = piece_contours_info[color][1]

                    for contour_index, contour_i in enumerate(contours_i):

                        area_cnt = cv2.contourArea(contour_i)
                        # Contour apa pun yang membatasi bidak di dalam sisi harus punya
                        # lebih dari tiga sudut. Contour yang lebih kecil dari luas minimum
                        # satu bidak juga diabaikan sebagai noise.
                        if (len(contour_i) > 3 and
                            area_cnt >= min_piece_area):

                            for i in range(3):
                                for j in range(3):
                                    # Karena gambar dicerminkan sedangkan objek Cube dibentuk
                                    # seperti di dunia nyata, dibutuhkan nilai asli sekaligus
                                    # nilai terbalik dari indeks kolom j.
                                    j_reversed = abs(j - 2)
                                    piece_center = piece_centers[i][j]
                                    if cv2.pointPolygonTest(contour_i, piece_center, False) == 1:
                                        
                                        relative_area = area_cnt / area_face
                                        previous_used = relative_areas[i][j_reversed]
                                        if (relative_area <= previous_used and
                                            not parents_inside_face(contours_i, hierarchy_array,
                                                                    contour_index, contour_face)):

                                            if (i == 1 and j == 1):
                                                # Kalau warna pusat berubah, kemungkinan besar
                                                # kubus sudah dirotasi, jadi sisi harus
                                                # diinisialisasi ulang untuk menghapus nilai
                                                # dari sisi sebelumnya. Warna hanya disimpan ke
                                                # sisi jika sisi yang benar sedang terlihat
                                                # (warna pusat yang terdeteksi sama dengan yang
                                                # diinginkan). Pengecualiannya, kalau sisi yang
                                                # diinginkan sudah terdeteksi dan diverifikasi,
                                                # maka sisi apa pun yang terlihat akan dideteksi
                                                # supaya panah petunjuk bisa digambar untuk
                                                # pengguna agar tahu ke mana harus memutar.
                                                if face[i][j] != color:
                                                    face = initialize_face()
                                                    relative_areas = initialize_areas()
                                                    piece_contours_info = reverse_dict(piece_contours_info)
                                                if color == center_color or verified:
                                                    face[i][j] = color
                                                    relative_areas[i][j] = relative_area


                                            elif face[1][1] == center_color or verified:  
                                                face[i][j_reversed] = color
                                                relative_areas[i][j_reversed] = relative_area
                                            



            if detection_completed(face) and not detected:

                print_mirrored_face(face)
                instruction_text = "Terdeteksi dengan benar? y/n?"
                detected = True
                    
            if verified:
                if center_color == "white":
                    instruction_text = get_instruction_text("yellow")
                    if detection_completed(face):
                        draw_arrows(img, "x'", piece_centers)
                        if face[1][1] == "yellow":
                            return "completed", face_to_return
                if center_color == "yellow":
                    instruction_text = get_instruction_text("blue")
                    if detection_completed(face):
                        draw_arrows(img, "x", piece_centers)
                        if face[1][1] == "blue":
                            return "completed", face_to_return
                if center_color == "blue":
                    instruction_text = get_instruction_text("red")
                    if detection_completed(face):
                        draw_arrows(img, "y'", piece_centers)
                        if face[1][1] == "red":
                            return "completed", face_to_return
                if center_color == "red":
                    instruction_text = get_instruction_text("green")
                    if detection_completed(face):
                        draw_arrows(img, "y'", piece_centers)
                        if face[1][1] == "green":
                            return "completed", face_to_return
                if center_color == "green":
                    instruction_text = get_instruction_text("orange")
                    if detection_completed(face):
                        draw_arrows(img, "y'", piece_centers)
                        if face[1][1] == "orange":
                            return "completed", face_to_return
                if center_color == "orange":
                    instruction_text = get_instruction_text("green")
                    if detection_completed(face):
                        draw_arrows(img, "y", piece_centers)
                        if face[1][1] == "green":
                            return "completed", face_to_return


        # Hapus tanda komentar (uncomment) baris-baris ini untuk memeriksa apakah batas warna
        # yang diatur di bagian awal cocok dengan lingkungan Anda.

        # cv2.imshow('mask_red', masks[1])
        # cv2.imshow('mask_green', masks[2])
        # cv2.imshow('mask_orange', masks[3])
        # cv2.imshow('mask_yellow', masks[4])
        # cv2.imshow('mask_white', masks[5])
        
        
        # Tetap tampilkan panel 3x3 selama proses pemindaian,
        # termasuk setelah sisi sebelumnya dikonfirmasi.
        draw_face(img, face)

        cv2.imshow('CUBE SOLVER', img)

        pressed = cv2.waitKey(1)

        if pressed == ord('q'):
            return "quit", None
        if pressed == ord(' '):
            cube.print_state()
            print()
            print("sisi:")
            print(face)
            
        if (pressed == ord('y') and 
            detected):
            face_to_return = face.copy()
            verified = True
        if pressed == ord('n'):
            return "restart", face
        
# Beberapa fungsi membutuhkan nilai koordinat x dan y berupa float, sebagian lainnya
# membutuhkan int. Fungsi ini dipakai untuk mengonversinya.
def point_type_converter(point, int_to_float = False, float_to_int = False):
    if ((int_to_float == True and float_to_int == True) or
        (int_to_float == False and float_to_int == False)):
        print("point_type_converter: Pilih SATU arah konversi!")
        return point
    x = point[0]
    y = point[1]
    if int_to_float:
        point = (float(x), float(y))

    if float_to_int:
        point = (int(x), int(y))

    return point


# Fungsi ini menggambar panah petunjuk di atas gambar supaya pengguna tahu ke mana harus
# memutar atau merotasi kubus.
def draw_arrows(img, turn, piece_centers):

    top_left = point_type_converter(piece_centers[0][0], float_to_int=True)
    top_mid = point_type_converter(piece_centers[0][1], float_to_int=True)
    top_right = point_type_converter(piece_centers[0][2], float_to_int=True)
    mid_left = point_type_converter(piece_centers[1][0], float_to_int=True)
    mid_right = point_type_converter(piece_centers[1][2], float_to_int=True)
    bottom_left = point_type_converter(piece_centers[2][0], float_to_int=True)
    bottom_mid = point_type_converter(piece_centers[2][1], float_to_int=True)
    bottom_right = point_type_converter(piece_centers[2][2], float_to_int=True)



    arrow_thickness = 3
    arrow_color = (50, 0, 0)
    

    if turn == "U":
        cv2.arrowedLine(img, top_left, top_right, arrow_color, arrow_thickness)
    if turn == "U'":
        cv2.arrowedLine(img, top_right, top_left, arrow_color, arrow_thickness)
    if turn == "D":
        cv2.arrowedLine(img, bottom_right, bottom_left, arrow_color, arrow_thickness)
    if turn == "D'":
        cv2.arrowedLine(img, bottom_left, bottom_right, arrow_color, arrow_thickness)
    if turn == "R" or turn == "B":
        cv2.arrowedLine(img, top_right, bottom_right, arrow_color, arrow_thickness)
    if turn == "R'" or turn == "B'":
        cv2.arrowedLine(img, bottom_right, top_right, arrow_color, arrow_thickness)
    if turn == "L" or turn == "F":
        cv2.arrowedLine(img, bottom_left, top_left, arrow_color, arrow_thickness)
    if turn == "L'" or turn == "F'":
        cv2.arrowedLine(img, top_left, bottom_left, arrow_color, arrow_thickness)
    if turn == "y":
        cv2.arrowedLine(img, top_left, top_right, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, mid_left, mid_right, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, bottom_left, bottom_right, arrow_color, arrow_thickness)
    if turn == "y'":
        cv2.arrowedLine(img, top_right, top_left, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, mid_right, mid_left, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, bottom_right, bottom_left, arrow_color, arrow_thickness)
    if turn == "x":
        cv2.arrowedLine(img, top_right, bottom_right, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, top_mid, bottom_mid, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, top_left, bottom_left, arrow_color, arrow_thickness)
    if turn == "x'":
        cv2.arrowedLine(img, bottom_right, top_right, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, bottom_mid, top_mid, arrow_color, arrow_thickness)
        cv2.arrowedLine(img, bottom_left, top_left, arrow_color, arrow_thickness)

    return

# Fungsi ini menggambar sisi (sebagaimana terdeteksi selama fungsi detect_face()) di layar.
def draw_face(img, face):
    colors_bgr = {"red": (0, 0, 255), "blue": (255, 0, 0), "green": (0, 255, 0),
              "orange": (0, 123, 255), "yellow": (0, 255, 255), "white": (255, 255, 255),
              "gray": (90, 90, 90), "black": (0, 0, 0)}
    
    origin_face = (500, 40)
    piece_width = 30
    piece_height = 30

    for i in range(3):
        for j in range(3):
            j_reversed = abs(j - 2)
            origin_piece_x = origin_face[0] + j*piece_width
            origin_piece_y = origin_face[1] + i*piece_height
            origin_piece = (origin_piece_x, origin_piece_y)
            end_point_piece_x = origin_piece_x + piece_width
            end_point_piece_y = origin_piece_y + piece_height
            end_point_piece = (end_point_piece_x, end_point_piece_y)

            color_name = face[i][j_reversed]
            if color_name == "init":
                color_name = "gray"
            color_value = colors_bgr[color_name]
            
            cv2.rectangle(img, origin_piece, end_point_piece, color_value, -1)

    for i in range(3):

        for j in range(3):
            j_reversed = abs(j - 2)
            origin_piece_x = origin_face[0] + j*piece_width
            origin_piece_y = origin_face[1] + i*piece_height
            origin_piece = (origin_piece_x, origin_piece_y)
            end_point_piece_x = origin_piece_x + piece_width
            end_point_piece_y = origin_piece_y + piece_height
            end_point_piece = (end_point_piece_x, end_point_piece_y)
            
            cv2.rectangle(img, origin_piece, end_point_piece, colors_bgr["black"], 2)

    draw_text(img, text = "DETEKSI", origin = (505, 132))
            

# Fungsi ini dipakai untuk mengawasi dan memandu pengguna agar melakukan putaran dan rotasi
# kubus dengan benar. Strukturnya mengikuti logika fungsi detect_face: baca komentar di sana
# untuk memahami struktur utamanya.
def make_turn(video, turn, previous_center_color, last_turn):
    solved = False
    letter = turn[0]
    # Untuk menyederhanakan, pengguna selalu diminta menunjukkan sisi berpusat merah atau
    # hijau selama proses penyelesaian. Semua gerakan yang mungkin mudah dilakukan dengan
    # salah satu dari kedua posisi kubus tersebut.
    if letter == 'U' or letter == 'D':
        valid_face_centers = ["green", "red"]
    elif letter == 'R' or letter == 'L':
        valid_face_centers = ["green"]
    else: # jika letter == 'F' atau 'B':
        valid_face_centers = ["red"]
    # Menghindari rotasi yang tidak perlu
    if valid_face_centers.count(previous_center_color) > 0:
        center_color = previous_center_color
    else:
        center_color = valid_face_centers[0]

    red_pre_turn = cube.get_face("red")
    green_pre_turn = cube.get_face("green")

    if center_color == "red":
        face_pre_turn = red_pre_turn
    else: # jika center_color == "green"
        face_pre_turn = green_pre_turn

    cube.call_turn(turn)
    face_post_turn = cube.get_face(center_color)

    face_showing = initialize_face()
    relative_areas = initialize_areas()
    instruction_text = get_instruction_text(center_color)

    while True:
        success, img = get_img(video)
        if not success:
            return "failed", None
        
        if not solved:
            draw_text(img, instruction_text, origin = (10, 10))
            masks = get_masks(img)


            face_found, contour_face, piece_centers = find_face_and_get_centers(img)
            if not face_found:
                face_showing = initialize_face()
                relative_areas = initialize_areas()
            else:
                area_face = cv2.contourArea(contour_face)
                min_piece_area = 0.08*area_face
                piece_contours_info = get_piece_contours_info(masks)


                for color in piece_contours_info:
                    contours_i = piece_contours_info[color][0]
                    hierarchy_array = piece_contours_info[color][1]

                    for contour_index, contour_i in enumerate(contours_i):
                        area_cnt = cv2.contourArea(contour_i)

                        if (len(contour_i) > 3 and
                            area_cnt >= min_piece_area):

                            for i in range(3):
                                for j in range(3):
                                    j_reversed = abs(j - 2)
                                    piece_center = piece_centers[i][j]
                                    if cv2.pointPolygonTest(contour_i, piece_center, False) == 1:
                                        
                                        relative_area = area_cnt / area_face
                                        previous_used = relative_areas[i][j_reversed]
                                        if (relative_area <= previous_used and
                                            not parents_inside_face(contours_i, hierarchy_array,
                                                                    contour_index, contour_face)):
                                            if (i == 1 and j == 1):
                                                if face_showing[i][j] != color:
                                                    face_showing = initialize_face()
                                                    relative_areas = initialize_areas()
                                                if color == "red" or color == "green":
                                                    face_showing[i][j] = color
                                                    relative_areas[i][j] = relative_area

                                            elif face_showing[1][1] == "red" or face_showing[1][1] == "green":  
                                                face_showing[i][j_reversed] = color
                                                relative_areas[i][j_reversed] = relative_area
                                            


                if detection_completed(face_showing):

                    if faces_match(face_showing, face_pre_turn):
                        draw_arrows(img, turn, piece_centers)

                    elif faces_match(face_showing, face_post_turn):
                        if not last_turn:
                            return "completed", center_color
                        else:
                            solved = True
                    elif (faces_match(face_showing, green_pre_turn) and
                          center_color == "red"):
                        draw_arrows(img, "y", piece_centers)
                    elif (faces_match(face_showing, red_pre_turn) and
                          center_color == "green"):
                        draw_arrows(img, "y'", piece_centers)

        else: # jika sudah terpecahkan
            draw_text(img, "KUBUS SELESAI!", origin = (240, 10))
            draw_text(img, "Tekan 'q' untuk menutup jendela.", origin = (150, 35))

        cv2.imshow('CUBE SOLVER', img)

        pressed = cv2.waitKey(1)

        if pressed == ord('q'):
            return "quit", None
        if pressed == ord(' '):
            print()
            print("face_showing (sisi yang terlihat):")
            print(face_showing)
            print()
            print("red_pre_turn (sisi merah sebelum putaran):")
            print(red_pre_turn)
            print()
            print("green_pre_turn (sisi hijau sebelum putaran):")
            print(green_pre_turn)
            

        
# Solusi dari fungsi solve() milik Kociemba berupa string di mana putaran ganda
# ditulis seperti "U2" yang berarti "U U". Di sini solusi disimpan dalam list huruf tunggal,
# di mana satu-satunya tambahan setelah huruf hanyalah tanda "'" yang berarti berputar
# berlawanan arah jarum jam.
def reform_solution(solution_str):
    solution_list = solution_str.split()
    result = []
    for turn in solution_list:

        if len(turn) > 1 and turn[1] == "2":
            result.append(turn[0])
            result.append(turn[0])
        else:
            result.append(turn)
    return result

# Fungsi ini dipanggil setelah deteksi selesai. Fungsi ini mengambil solusi untuk acakan
# yang diberikan dari fungsi solve() milik Kociemba lalu menelusuri setiap putaran dalam
# solusi, memanggil fungsi make_turn() untuk menjalankan putaran tersebut.
def solve_cube(video):

    
    solution_str = cube.get_solution()
    solution = reform_solution(solution_str)

    previous_center_color = "none"
    last_turn = False

    for i, turn in enumerate(solution):
        if i == len(solution) - 1:
            last_turn = True
        cmd, previous_center_color = make_turn(video, turn, previous_center_color, last_turn)
        if cmd == "quit":
            return "quit"
        if cmd == "failed":
            return "failed"
    return "solved"

def main():

    video = cv2.VideoCapture(0)
    cmd = detect_cube(video)
    if cmd == "detected":
        cmd = solve_cube(video)
    
    if cmd == "quit":
        print("Program berhenti karena perintah keyboard")
    if cmd == "failed":
        print("Program berhenti karena terjadi error yang tidak terduga")
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
