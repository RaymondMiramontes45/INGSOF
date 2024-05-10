from logger_base import log
import sys
import psycopg2 as db


class Connection:
    _DATABASE = 'xddddddddddddddddddddd'
    _USERNAME = 'postgres'
    _PASSWORD = 'None'
    _DB_PORT = '5432'
    _HOST = 'localhost'
    _connection = None
    _cursor = None
    charset='utf8mb4'
    client_encoding='UTF8'

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            try:
                cls._connection = db.connect(
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    port=cls._DB_PORT,
                    host=cls._HOST,
                    database=cls._DATABASE
                )
                log.debug(f'CONEXION A DB EXITOSA: {cls._connection}')
                return cls._connection
            except Exception as e:
                sys.exit()
        else:
            return cls._connection

    @classmethod
    def get_cursor(cls):
        if cls._cursor is None:
            try:
                cls._cursor = cls.get_connection().cursor()
                log.debug(f'CURSOR CREADO: {cls._cursor}')
                return cls._cursor
            except Exception as e:
                log.error(f'FALLA EN LA CRECION DE CURSOR: {e}')
        else:
            return cls._cursor

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            log.debug('CONEXION CERRADA')
        else:
            log.debug('NO HAY CONEXION ABIERTA')
            return


if __name__ == '__main__':
    Connection.get_connection()
    Connection.get_cursor()
    Connection.close_connection()