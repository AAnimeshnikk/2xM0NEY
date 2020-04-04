from DB_connector import *

def GetRoomsOnline():
    data.execute("SELECT room_online FROM Rooms")
    result = data.fetchall()
    onlines = {}
    for x in range(1, 21):
        onlines[str(x)] = result[x-1][0]
    return onlines

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

