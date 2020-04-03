from DB_connector import *


#GET BLOCK
def AccountExistsByID(acc_id):
    data.execute("SELECT acc_id FROM Accounts WHERE acc_id = '%s'" % acc_id) # command for sql
    accountExists = data.fetchall() # result
    if len(accountExists) != 0:
        return True
    else:
        return False

def GetAccountDataByID(acc_id):
    data.execute("SELECT * FROM Accounts WHERE acc_id = '%s'" % acc_id) # command for sql
    try:
        _accountData = data.fetchall()[0]  # result
        accountData = {}
        accountData["acc_id"] = _accountData[0]
        accountData["acc_name"] = _accountData[1]
        accountData["acc_username"] = _accountData[2]
        accountData["acc_showRealName"] = _accountData[3]
        accountData["acc_balance"] = _accountData[4]
    except:
        raise ValueError("unknown id: '%s'" % acc_id)
    return accountData

def CreateNewAccount(acc_id, acc_name): # create new account for user
    data.execute("INSERT INTO Accounts(acc_id, acc_name, acc_username, acc_showRealName, acc_balance) VALUES('%s', '%s', 'Unknown', 'TRUE', '0')"
                 % (acc_id, acc_name))
    database.commit()

def SetAccountDataElement(acc_id, element, value): # update the database elementt o value by acc_id
    data.execute("UPDATE Accounts SET %s = '%s' WHERE acc_id = %s" % (element, value, acc_id))
    database.commit()






