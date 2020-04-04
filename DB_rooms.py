from DB_connector import *

def SetRoomOnline(room_id, value):
    data.execute("UPDATE Rooms SET room_online = %s WHERE room_id = '%s'" % (value, room_id))
    database.commit()

def GetRoomsOnline():
    data.execute("SELECT room_online FROM Rooms")
    result = data.fetchall()
    onlines = {}
    for x in range(1, 21):
        onlines[str(x)] = result[x-1][0]
    return onlines

def GetRoomOnline(room_id):
    data.execute("SELECT room_online FROM Rooms WHERE room_id = '%s'" % room_id)
    return data.fetchall()[0][0]


def GetRoomsTypes():
    data.execute("SELECT room_type FROM Rooms")
    result = data.fetchall()
    types = {}
    for x in range(1, 21):
        types[str(x)] = result[x - 1][0]
    return types

def GetRoomType(room_id):
    data.execute("SELECT room_type FROM Rooms WHERE room_id = '%s'" % room_id)
    return data.fetchall()[0][0]

def AddUserToRoom(room_id, acc_id):
    data.execute("SELECT room_usersData FROM Rooms WHERE room_id = '%s'" % room_id)
    strdata = data.fetchall()[0][0]
    strdata += "user*%s:0;" % acc_id
    data.execute("UPDATE Rooms SET room_usersData = '%s' WHERE room_id = '%s'" % (strdata, room_id))
    database.commit()

def RemoveUserFromRoom(room_id, acc_id):
    data.execute("SELECT room_usersData FROM Rooms WHERE room_id = '%s'" % room_id)
    strdata = data.fetchall()[0][0]
    start_index = strdata.index("user*%s"%acc_id)
    subsrt = strdata[start_index:]
    stop_index = start_index+subsrt.index(";")+1
    strdata = strdata.replace(strdata[start_index:stop_index], "")
    data.execute("UPDATE Rooms SET room_usersData = '%s' WHERE room_id = '%s'" % (strdata, room_id))
    database.commit()

def RemoveAllUsersFromRoom(room_id):
    data.execute("UPDATE Rooms SET room_usersData = '%s' WHERE room_id = '%s'" % ("", room_id))
    database.commit()


def SetUserMoneyRate(room_id, acc_id, value):
    data.execute("SELECT room_usersData FROM Rooms WHERE room_id = '%s'" % room_id)
    strdata = data.fetchall()[0][0]
    start_index = strdata.index("user*%s" % acc_id)
    subsrt = strdata[start_index:]
    stop_index = start_index + subsrt.index(";") + 1
    strdata = strdata.replace(strdata[start_index:stop_index], "user*%s:%s;" % (acc_id, value))
    data.execute("UPDATE Rooms SET room_usersData = '%s' WHERE room_id = '%s'" % (strdata, room_id))
    database.commit()

def GetUserMoneyRate(room_id, acc_id):
    data.execute("SELECT room_usersData FROM Rooms WHERE room_id = '%s'" % room_id)
    strdata = data.fetchall()[0][0]
    start_index = strdata.index("user*%s" % acc_id) + 5 + len(str(acc_id)) + 1
    stop_index = start_index + strdata[start_index:].index(";")
    return strdata[start_index:stop_index]

def GetAllUsersMoneyRate(room_id):
    data.execute("SELECT room_usersData FROM Rooms WHERE room_id = '%s'" % room_id)
    strdata = data.fetchall()[0][0]

    result = {}

    for x in range(int(GetRoomOnline(room_id))):
        result[strdata[5:strdata.index(":")]] = strdata[strdata.index(":")+1:strdata.index(";")]
        strdata = strdata[strdata.index(";")+1:]

    return result

def GetRoomRateOfMoney(room_id):
    data.execute("SELECT room_rateOfMoney FROM Rooms WHERE room_id = '%s'" % room_id)
    return data.fetchall()[0][0]