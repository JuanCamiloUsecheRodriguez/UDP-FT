import socket, threading, os, hashlib,sys
from time import sleep

# Pool Size
SIZE=60000
# Hash MD5 del archivo
hasher = hashlib.md5()

# Create a UDP socket
class udp_transfer:
    socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    def __init__(self):
        server_address = ('localhost', 10000)

        # Argumentos dentro de la ejecucion del archivo
        numCli = int(sys.argv[1]) #Numero de Clientes
        fileName = sys.argv[2] #Nombre del archivo

        print('Conexion inicializada en la direccion {} con el puerto {}'.format(*server_address))

        self.socketServidor.bind(server_address)
        print('\nEsperando a recibir el mensaje')
        threads = []
        idCli =1
        while numCli > 0:
            data, address =self. socketServidor.recvfrom(SIZE)
            if data == b'Listo':
                size = os.path.getsize(fileName)
                print(' Tamaño del archivo : {}'.format(str(size)))

                print('Creando los Threads..')
                send_thread = threading.Thread(target=self.send_file, args=( address, fileName, idCli))
                threads.append(send_thread)
                numCli = numCli-1
                idCli =idCli+1
                print("Numero de clientes restantes: ",numCli)
                print('Inicializando los Threads..')
        for thread in threads:
            thread.start()

    def send_file(self, address, fileName, idCli):
        i = 0
        size = os.path.getsize(fileName)
        bytesEnv = 0
        print(' Tamaño del archivo : {}'.format(str(size)))
        with open(fileName, 'rb') as file:
            data = file.read(SIZE)
            while data != bytes(''.encode()):
                sent = self.socketServidor.sendto(data, address)
                data = file.read(SIZE)
                print('{}. Enviados {} bytes a la direccion {}'.format(i,sent, address))
                i = i +1
                bytesEnv = bytesEnv+sent
                if sent != SIZE:
                    sent = self.socketServidor.sendto(b'Fin', address)
                    print('Enviados {} bytes a la direccion {}'.format(sent, address))
                    break
            buf = file.read()
            print('Generando el Hash del Servidor para el archivo ' + fileName)
            hasher.update(buf)
            hashServidor = hasher.hexdigest()

            # Envios desde el Servidor al Cliente
            self.socketServidor.sendto(fileName.encode('utf-8'), address)
            self.socketServidor.sendto(str(os.path.getsize(fileName)).encode('utf-8'), address)
            self.socketServidor.sendto(str(idCli).encode('utf-8'), address)
            self.socketServidor.sendto(str(hashServidor).encode('utf-8'), address)
            self.socketServidor.sendto(str(bytesEnv).encode('utf-8'), address)
            self.socketServidor.sendto(str(i).encode('utf-8'), address)








udp = udp_transfer()

