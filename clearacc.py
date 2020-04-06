import mysql.connector
database = mysql.connector.connect(  # connecting to database
            host="sql7.freemysqlhosting.net",
            user="sql7330856",
            passwd="N2i39Qde6k",
            database="sql7330856"
        )

sql_data_executor = database.cursor()
sql_data_executor.execute("DELETE * FROM Accounts")
database.commit()
sql_data_executor.close()
database.close()
