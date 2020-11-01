import socket as so
from settings import *
import logging.config

logging.config.fileConfig('logger.conf')
logger = logging.getLogger(name='Texter.TexterServer')

s = so.socket()
logger.info('Socket successfully crated')

port = 1026

s.bind(('', port))
logger.info(f'Socket binded to {port} port')

s.listen()
logger.info('Socket is listening')

while True:
    conn, address = s.accept()
    logger.info(f'Got a connection from {address}')
    with open(FILENAME, 'r') as file:
        lines_str = ''.join(file.readlines())
        file.close()

        to_send = lines_str.encode('utf-8')
        logger.info(f'File contains {len(to_send)} bytes of data. Sending to remote socket')
        conn.send(len(to_send).to_bytes(16, 'big'))
        conn.send(to_send)

        logger.info('Successfully sent file to remote')

        logger.info(f'Waiting for response from {address}')
        while True:
            try:
                byte_data = conn.recv(1)
            except so.error as e:
                byte_data = END_BYTE
                logger.error(f'Lost connection with {address}')
            if byte_data == SAVE_BYTE:
                logger.info(f'Updating file from {address}')
                data_size = int.from_bytes(conn.recv(16), 'big')
                data = conn.recv(data_size)
                data_str = data.decode('utf-8')
                logger.info(f'Got {len(data)} / {data_size} bytes of data')
                with open(FILENAME, 'w') as file_:
                    file_.write(data_str)
                    logger.info(f'Wrote data from {address} to file')
            elif byte_data == END_BYTE:
                logger.info(f'Connection with {address} closed by remote')
                break

    conn.close()
    logger.info('program stopped')
