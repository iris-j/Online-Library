import pymysql
pymysql.install_as_MySQLdb()

# 打开数据库连接
db = pymysql.connect("localhost","root","","online_library_db")
# 使用cursor（）方法来获取操作句柄
cursor = db.cursor();
# 使用execute方法来执行SQL语句
cursor.execute("SELECT VERSION()")
# 使用fetchone()方法获取一条数据库
data = cursor.fetchone()

print("Database version : %s "% data)
# 关闭数据库连接
db.close()

