import mysql.connector
import time
from threading import Thread
from datetime import date

ID = "id"
TELEGRAM_NAME = "telegram_name"
USER_NAME = "user_name"
PRIMARY_NAME = "primary_name"
BALANCE = "balance"
REGISTRATION_DATE = "registration_date"


class NewConnectionToAccountsDatabase:
    def __init__(self):
        self.__database = mysql.connector.connect(  # connecting to database
            host="sql7.freemysqlhosting.net",
            user="sql7330856",
            passwd="N2i39Qde6k",
            database="sql7330856"
        )

        self.__sql_data_executor = self.__database.cursor()

        self.__changes = []

    def CommitToDatabase(self):
        for change in self.__changes:
            self.__sql_data_executor.execute(change)
        self.__database.commit()

    def GetFullAccountDataByID(self, id):
        try:
            data = {}
            self.__sql_data_executor.execute("SELECT * FROM Accounts WHERE id = %s" % id)
            result = self.__sql_data_executor.fetchall()[0]
            data["id"] = result[0]
            data["telegram_name"] = result[1]
            data["user_name"] = result[2]
            data["primary_name"] = result[3]
            data["balance"] = result[4]
            data["registration_time"] = result[5]
            return data
        except:
            raise ValueError("There are no users with '%s' id" % id)

    def GetFullAccountDataByTelegramName(self, telegram_name):
        try:
            data = {}
            self.__sql_data_executor.execute("SELECT * FROM Accounts WHERE telegram_name= '%s'" % telegram_name)
            result = self.__sql_data_executor.fetchall()[0]
            data["id"] = result[0]
            data["telegram_name"] = result[1]
            data["user_name"] = result[2]
            data["primary_name"] = result[3]
            data["balance"] = result[4]
            data["registration_time"] = result[5]
            return data
        except:
            raise ValueError("There are no users with '%s' telegram_name" % telegram_name)

    def GetFullAccountDataByUserName(self, user_name):
        try:
            data = {}
            self.__sql_data_executor.execute("SELECT * FROM Accounts WHERE user_name= '%s'" % user_name)
            result = self.__sql_data_executor.fetchall()[0]
            data["id"] = result[0]
            data["telegram_name"] = result[1]
            data["user_name"] = result[2]
            data["primary_name"] = result[3]
            data["balance"] = result[4]
            data["registration_time"] = result[5]
            return data
        except:
            raise ValueError("There are no users with '%s' user_name" % user_name)

    def CreateNewAccount(self, id):
        try:
            self.__changes.append("INSERT INTO Accounts(id, telegram_name, user_name, primary_name, balance, registration_date) VALUES(%s, '@UnknownTelegramUser', 'UnknownUser', 'telegram_name', 0, '%s')" % (
                id, str(date.today()).replace("-", " ").replace("-", " ")
            ))
        except:
            raise ValueError("Invalid argument")

    def UpdateTelegramName(self, id, updated_telegram_name):
        try:
            self.__changes.append("UPDATE Accounts SET telegram_name = '%s' WHERE id = %s" % (updated_telegram_name, id))
        except:
            raise ValueError("Invalid Arguments")

    def UpdateUserName(self, id, updated_user_name):
        try:
            self.__changes.append("UPDATE Accounts SET user_name = '%s' WHERE id = %s" % (updated_user_name, id))
        except:
            raise ValueError("Invalid Arguments")

    def UpdatePrimaryName(self, id, updated_primary_name):
        try:
            self.__changes.append("UPDATE Accounts SET primary_name = '%s' WHERE id = %s" % (updated_primary_name, id))
        except:
            raise ValueError("Invalid Arguments")

    def UpdateBalance(self, id, updated_balance):
        try:
            self.__changes.append("UPDATE Accounts SET balance = %s WHERE id = %s" % (updated_balance, id))
        except:
            raise ValueError("Invalid Arguments")

    def CloseConnection(self):
        self.__sql_data_executor.close()
        self.__database.close()

