"""Jembatan browser <-> cube_solver_final.py, TANPA mengubah file tersebut.

Ide: program desktop dijalankan di thread sendiri, per pengunjung. Tiga hal yang
biasanya menyentuh perangkat keras/GUI diganti:
  cv2.VideoCapture(0)  -> Session (frame datang dari browser)
  cv2.imshow(...)      -> frame hasil disimpan lalu dikirim balik ke browser
  cv2.waitKey(1)       -> tombol (y/n/q) yang ditekan di halaman web
"""
import importlib.util
import os
import queue
import threading
import time
import uuid

import cv2
import numpy as np

SOLVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cube_solver_final.py")
MAX_SESSIONS = 4      # batas pengunjung bersamaan (tiap sesi memakai CPU)
IDLE_TIMEOUT = 30     # detik tanpa frame -> sesi ditutup
ALLOWED_KEYS = {"y", "n", "q"}


class CV2Shim:
    """Meniru modul cv2, tapi tiga fungsi di atas diarahkan ke Session."""

    def __init__(self, session):
        self._session = session

    def __getattr__(self, name):          # fungsi cv2 lain: pakai yang asli
        return getattr(cv2, name)

    def VideoCapture(self, *args, **kwargs):
        return self._session

    def imshow(self, winname, img):
        self._session.set_output(img)

    def waitKey(self, delay=0):
        return self._session.pop_key()

    def destroyAllWindows(self):
        pass


class Session:
    """Satu pengunjung = satu salinan program + satu thread."""

    def __init__(self):
        self.id = uuid.uuid4().hex
        self.last_seen = time.time()
        self.closed = False
        self.done = False
        self.error = None
        self._frame = None
        self._frame_ready = threading.Event()
        self._out_ready = threading.Event()
        self._output = b""
        self._keys = queue.Queue()
        self.mod = None
        self.thread = threading.Thread(target=self._run, daemon=True)

    # ---- dipanggil program desktop (Session berperan sebagai objek "video") ----
    def read(self):
        # Program minta frame berikutnya = frame sebelumnya sudah selesai diolah.
        # (Beberapa jalur kode, mis. saat sebuah sisi selesai, tidak memanggil imshow.)
        self._out_ready.set()
        while True:
            self._frame_ready.wait(timeout=1.0)
            if self.closed:
                return False, None
            if self._frame_ready.is_set():
                self._frame_ready.clear()
                return True, self._frame.copy()

    def release(self):
        pass

    def set_output(self, img):
        ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if ok:
            self._output = buf.tobytes()
        self._out_ready.set()

    def pop_key(self):
        try:
            return ord(self._keys.get_nowait())
        except queue.Empty:
            return -1

    # ---- dipanggil Flask ----
    def submit(self, jpeg_bytes):
        """Terima satu frame dari browser, tunggu hasil olahannya, kembalikan JPEG."""
        self.last_seen = time.time()
        img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None or self.done:
            return self._output
        self._out_ready.clear()
        self._frame = img
        self._frame_ready.set()
        self._out_ready.wait(timeout=3.0)
        return self._output

    def push_key(self, key):
        if key in ALLOWED_KEYS:
            self._keys.put(key)

    def close(self):
        self.closed = True
        self._frame_ready.set()

    def _run(self):
        try:
            # Salinan modul BARU per sesi -> variabel global `cube` terpisah tiap pengunjung.
            spec = importlib.util.spec_from_file_location("cube_solver_" + self.id, SOLVER_PATH)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.cv2 = CV2Shim(self)
            self.mod = mod
            mod.main()
        except Exception as e:  # jangan biarkan thread mati diam-diam
            self.error = repr(e)
        finally:
            self.done = True
            self._out_ready.set()


SESSIONS = {}
_LOCK = threading.Lock()


def create_session():
    with _LOCK:
        if len(SESSIONS) >= MAX_SESSIONS:
            return None
        s = Session()
        SESSIONS[s.id] = s
    s.thread.start()
    return s


def get_session(sid):
    return SESSIONS.get(sid)


def close_session(sid):
    with _LOCK:
        s = SESSIONS.pop(sid, None)
    if s:
        s.close()


def _reaper():
    while True:
        time.sleep(5)
        now = time.time()
        for s in list(SESSIONS.values()):
            if now - s.last_seen > IDLE_TIMEOUT:
                close_session(s.id)


threading.Thread(target=_reaper, daemon=True).start()
