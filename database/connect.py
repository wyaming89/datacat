import sshtunnel
import pymssql
DB_HOST="database_host"
DB_PORT = 1433
DB_USER = 'database_user'
DB_PWS = 'datapassword'

SERVER_HOST = 'ssh_server'
SERVER_USER = 'ssh_user'
SERVER_PORT = 22
#私钥的绝对路径（win下从盘符开始，Unix下从根目录开始）
P_KEY = 'absolute path pkey'

def connect():
    server = sshtunnel.SSHTunnelForwarder(
    ssh_address_or_host=(SERVER_HOST,SERVER_PORT),
    ssh_username=SERVER_USER,
    ssh_pkey=P_KEY,
    remote_bind_address=(DB_HOST,DB_PORT)
)

    server.start()
    conn = pymssql.connect(
        server='127.0.0.1',
        port=server.local_bind_port,
        database='temp_db',
        user=DB_USER,
        password=DB_PWS
    )
    cursor = conn.cursor()
    return cursor, server
    

def execute(sqltxt:str):
    cursor, server = connect()
    cursor.execute(sqltxt)
    data = cursor.fetchall()
    print(data)
    cursor.close()
    server.stop()
    
    

if __name__ == '__main__':
    sqltxt = "select top 10 * from dbo.tablename"
    execute(sqltxt)