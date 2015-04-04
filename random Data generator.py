import time
import random
import time
import sqlite3

class database():

    def db_init(self):
        conn = sqlite3.connect("dieselLevel.db")
        c=conn.cursor()
        try:
            #c.execute("DROP TABLE table1")
            c.execute("CREATE TABLE table1(device TEXT,level TEXT,time TEXT)")
            conn.close()
        except Exception as e:
            print ('db_init ERROR:'+str(e))
            pass
        finally:
            conn.close()
    def fetchData(self):
        conn=sqlite3.connect("dieselLevel.db")
        c=conn.cursor()
        c.execute("SELECT * FROM table1 ORDER BY time desc")
        data=c.fetchall()
        conn.close()
        return data
    def insertDb(self,device,level,currentTime):
        conn=sqlite3.connect("dieselLevel.db")
        c=conn.cursor()
        c.execute("INSERT INTO table1 values(?,?,?)",( device,str(level),str(currentTime) ))
        conn.commit()
        conn.close()
    def deleteDb(self,time,level):
        conn=sqlite3.connect("dieselLevel.db")
        c=conn.cursor()
        sql = "DELETE FROM table1 WHERE time=? and level=?"
        c.execute(sql,[time,level])
        conn.commit()
        conn.close()
    def dataFilter(self,fromTime,toTime):
        conn=sqlite3.connect("dieselLevel.db")
        c=conn.cursor()
        #sql = "DELETE FROM table1 WHERE time=? and level=?"
        sql = "SELECT * FROM table1 where time>=? and time<=?"
        c.execute(sql,[fromTime,toTime])
        conn.commit()
        conn.close()

    def randomDate(start, end, format, prop=random.random()):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formated in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        time = time.strftime(format, time.localtime(ptime))
        time = time.strptime(time, '%Y-%m-%d %H:%M:%S')
        return time


        """def randomDate(start, end, prop=random.random()):
        return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', prop)"""
    def randomPacket(self):
        i=1
        self.db_init()
        while i in range(1,2):
            device='d'
            date=randomDate("2012-01-01 1:30:00", "2016-01-01 4:50:00", random.random())
            level=str(random.randrange(100, 900, 2))
            
            #self.insertDb(device,level,date)
            i=i+1



def Main():
    
    i=1
    db=database()
    db.db_init()
    while i in range(1,100):
        device='d'
        date=randomDate("2012-01-01 1:30:00", "2016-01-01 4:50:00", random.random())
        level=str(random.randrange(100, 900, 2))
       	
        db.insertDb(device,level,date)
        i=i+1
     
	    

if __name__=='__main__':
    Main()
