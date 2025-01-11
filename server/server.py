import datetime
from time import sleep
import configparser
import mysql.connector
import requests

config = configparser.ConfigParser()
config.read("server_config.ini")
mysql_config = config['mysql']


def fetch_data(url):
    try:
        response = requests.get(url)
        # 检查请求是否成功
        response.raise_for_status()
        result = response.json()
        # 确保返回的数据是字典
        if not isinstance(result, dict):
            raise ValueError("返回的数据不是有效的字典")
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return {}
    except ValueError as ve:
        print(f"数据解析错误: {ve}")
        return {}


mydb = mysql.connector.connect(
    host=mysql_config['host'],
    port=mysql_config['port'],
    user=mysql_config['user'],
    password=mysql_config['password'],
    database=mysql_config['database']
)
myCursor = mydb.cursor()

if __name__ == '__main__':
    while True:
        try:
            myCursor.execute(
                """ select ip,url from sys_server_monitor where enable = 1""")
            l = myCursor.fetchall()
            for index, ip in enumerate(l):
                data = fetch_data(ip[1])
                print(datetime.datetime.now(), data)
                # 将数据保存到数据库中，根据ip
                sql = "update sys_server_monitor set update_time = now() ,cpu_percent = %s,mem_used = %s,mem_free=%s,mem_total= %s,mem_percent=%s,disk_used=%s,disk_free=%s,disk_total=%s,disk_percent=%s where ip=%s"
                myCursor.execute(sql, (
                    data['cpu_percent'],
                    data['mem_used'], data['mem_free'], data['mem_total'], data['mem_percent'],
                    data['disk_used'], data['disk_free'], data['disk_total'], data['disk_percent'], ip[0]))
                mydb.commit()
            sleep(10)
        except Exception as ex:
            print(ex)
