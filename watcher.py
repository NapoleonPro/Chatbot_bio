import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFChangeHandler(FileSystemEventHandler):
    """Handles file system events for the PDF file."""
    def on_modified(self, event):
        if event.src_path.endswith("Biodata.pdf"):
            print(f"Perubahan terdeteksi pada {event.src_path}. Menjalankan setup_vector.py...")
            try:
                # Menjalankan skrip setup_vector.py
                subprocess.run(["python3", "setup_vector.py"], check=True)
                print("✅ Database vektor berhasil diperbarui.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Gagal memperbarui database vektor: {e}")
            except FileNotFoundError:
                print("❌ Perintah 'python3' tidak ditemukan. Pastikan Python 3 terinstal.")

if __name__ == "__main__":
    path = "data"  # Direktori yang diawasi
    event_handler = PDFChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False) # recursive=False karena file ada di root 'data'

    print(f"Mengawasi perubahan pada direktori: {path}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()