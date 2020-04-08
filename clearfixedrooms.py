from database import *

conn = NewConnectionToFixedRoomsDatabase()

for x in range(1, 11):
    conn.ClearUsersFromRoom(x)
    conn.UpdateRoomCurrentOnline(x, 0)

conn.CommitToDatabase()
conn.CloseConnection()
del conn