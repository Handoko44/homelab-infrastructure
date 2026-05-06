import paramiko
import os
from datetime import datetime

# Konfigurasi MikroTik berdasarkan topologi Anda
MT_IP = "10.30.0.1" # Ganti dengan IP Mikrotik anda 
MT_USER = "USER_ANDA" # Pastikan user ini sudah dibuat di MikroTik
MT_PASS = "PASSWORD_ANDA"
BACKUP_DIR = "backups"

def run_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"config_{timestamp}.rsc"
    filepath = os.path.join(BACKUP_DIR, filename)

    try:
        print(f"[*] Menghubungkan ke {MT_IP}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(MT_IP, username=MT_USER, password=MT_PASS, timeout=10)

        print("[*] Mengambil konfigurasi...")
        stdin, stdout, stderr = client.exec_command("/export compact")
        config_data = stdout.read().decode('utf-8')

        with open(filepath, "w") as f:
            f.write(config_data)

        print(f"[+] Berhasil! File disimpan di: {filepath}")

    except Exception as e:
        print(f"[!] Gagal: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_backup()
