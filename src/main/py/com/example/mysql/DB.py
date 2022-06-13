import mysql.connector


class DB(object):

    connection = None

    # The init method or constructor
    def __init__(self, uuid=None):
        self.connection = mysql.connector.connect(
            user="operate",
            password="p@SSW0rd",
            host="mysqlserver",
            port="3306",
            database="SANDBOXDB",
            autocommit=False
        )
        print(self.connection)


    def saveAndCommit(self):

        cursor = self.connection.cursor()
        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = ("John", "Highway 21")
        cursor.execute(sql, val)

        self.connection.commit()
        print(cursor.rowcount, "record inserted.")

    def close(self):
        # Disconnecting from the server
        self.connection.close()