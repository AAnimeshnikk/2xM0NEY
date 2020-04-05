from DB_connector import *
data.execute("DELETE FROM Accounts WHERE acc_id = '983670270'")
database.commit()