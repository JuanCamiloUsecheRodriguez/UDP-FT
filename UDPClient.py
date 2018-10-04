import socket, os, sys, threading, hashlib, time, logging
from time import gmtime, strftime

from sys     import stderr
import logging
from logging import getLogger, StreamHandler, Formatter, DEBUG

#Log del proceso de transferencia

log  = getLogger()
os.makedirs(os.path.dirname('./logs/udp.log'), exist_ok=True)
logging.basicConfig(format='%(message)s', filename='./logs/udp.log',  level=logging.DEBUG)
strHan = StreamHandler(stderr)
strHan.setLevel(DEBUG)
formatter  = Formatter(' %(message)s')
strHan.setFormatter(formatter)
log.addHandler(strHan)
log.setLevel(DEBUG)
idCli = ''

# Tamaño del Pool
SIZE=60000
# Hash MD5 para el Cliente
hasher = hashlib.md5()

# Create a UDP socket
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('157.253.205.19', 10000)
message = b'Listo'
showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
log.info('%s#%s', 'FECHA', showtime)

try:
    # Send data
    print('Conexion Exitosa!')
    sent = socketCliente.sendto(message, server_address)
    start_time = time.time()
    filename = './recibido/'+sys.argv[1]
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    numPaquetes = 0
    bytesReceived = 0
    with open(filename, 'wb+') as formatter:
        data, address = socketCliente.recvfrom(SIZE)
        while data != bytes(''.encode()):
            formatter.write(data)
            data, address = socketCliente.recvfrom(SIZE)
            numPaquetes = numPaquetes + 1
            print("data ",data)
            print(bytesReceived)
            print(len(data))
            bytesReceived = bytesReceived + len(data)
            print("La wea que estoy sumando ",bytesReceived)

            if data == b'Fin':
                bytesReceived = bytesReceived + len(data)
                print("La wea que estoy sumando pero en el fin ", bytesReceived)
                break

        buf = formatter.read()
        print('Generando el Hash del Cliente para el archivo recibido ' )
        hasher.update(buf)
        hashCliente = hasher.hexdigest()

        nomArchivoR, address = socketCliente.recvfrom(SIZE)
        log.info('%s#%s', 'NOMBRE_ARCHIVO', nomArchivoR.decode('utf-8'))

        tamArchivoR, address = socketCliente.recvfrom(SIZE)
        log.info('%s#%s', 'TAMANO_ARCHIVO', tamArchivoR.decode('utf-8'))

        idClienteR, address = socketCliente.recvfrom(SIZE)
        idCli = idClienteR.decode('utf-8')
        log.info('%s#%s', 'ID_CLIENTE', idClienteR.decode('utf-8'))

        hashServidor, address = socketCliente.recvfrom(SIZE)
        hashServidor = hashServidor.decode('utf-8')

        log.info('%s#%s', 'HASH_SERVIDOR', hashServidor)
        log.info('%s#%s', 'HASH_CLIENTE', hashCliente)

        if hashServidor == hashCliente:
            log.info('ENVIO_ARCHIVO#EXITOSO')
        else:
            log.info('ENVIO_ARCHIVO#FALLO')

        bytesSent, address = socketCliente.recvfrom(SIZE)
        bytesSent = bytesSent.decode('utf-8')
        log.info('%s#%s', 'BYTES_ENVIADOS', bytesSent)

        log.info('%s#%s', 'BYTES_RECIBIDOS', bytesReceived)

        numPaquetesServ, address = socketCliente.recvfrom(SIZE)
        numPaquetesServ = numPaquetesServ.decode('utf-8')
        numPaquetesCli = numPaquetes

        log.info('%s#%s', 'PAQUETES_ENVIADOS', numPaquetesServ)
        log.info('%s#%s', 'PAQUETES_RECIBIDOS', numPaquetes)


finally:
    print('Cerrando el Socket..')
    elapsed_time = time.time() - start_time
    log.info('%s#%s', 'TIEMPO_TOTAL', elapsed_time)
    log.info('------------------------------')
    # clean up file handlers
    logging.shutdown()
    os.rename('./logs/udp.log', './logs/udp{}.log'.format(idCli))

    socketCliente.close()
