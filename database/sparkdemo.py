import sshtunnel
from pyspark.sql import SparkSession


DB_HOST="mjn-dw.cwdlk16xyvmj.rds.cn-northwest-1.amazonaws.com.cn"
DB_PORT = 1433
DB_USER = 'dxg'
DB_PSW = 'dxg!@#963$%sds'

SERVER_HOST = '52.82.80.128'
SERVER_USER = 'centos'
SERVER_PORT = 22
#私钥的绝对路径（win下从盘符开始，Unix下从根目录开始）
P_KEY = 'd:\\datax\\datacon\\MJN-Kettle-KeyPair.pem'


spark = (
    SparkSession
    .builder
    .appName("mjn_dl_dxg_0422")
    .getOrCreate()
)
server = sshtunnel.SSHTunnelForwarder(
    ssh_address_or_host=(SERVER_HOST,SERVER_PORT),
    ssh_username=SERVER_USER,
    ssh_pkey=P_KEY,
    remote_bind_address=(DB_HOST,DB_PORT)
)
server.start()
df = (spark.read
      .format('jdbc')
      .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
      .option('url',f'jdbc:sqlserver://127.0.0.1:{server.local_bind_port}')
      .option('user',DB_USER)
      .option('dbtable','temp_db.dbo.cellphone2md5ym0422')
      .option('password',DB_PSW).load())

count = df.count().collect()
print(count)
server.stop()

