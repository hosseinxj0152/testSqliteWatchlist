import sqlite3
import random
def createConnection(db_name):  
    con = sqlite3.connect(db_name)
    con.isolation_level = None
    return con.cursor(), con

def createMainTable(cur, table_name):
    query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                                        id INTEGER PRIMARY KEY,
                                                        Name TEXT, 
                                                        Duration TIME,
                                                        Score INTEGER,
                                                        UNIQUE(
                                                              id,
                                                              Name,
                                                              Duration,
                                                              Score
                                                        )
                                                        );
                                      '''
    cur.execute(query)

def createSecondaryTable(cur, table_name):
    query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                                        id INTEGER PRIMARY KEY,
                                                        initial_id INTEGER, 
                                                        Name TEXT, 
                                                        Duration TIME,
                                                        Score INTEGER
                                                        );             
             '''
    cur.execute(query)
    add_to_watched(cur)

def add_to_watched(cur):
    query = '''CREATE TRIGGER IF NOT EXISTS add_to_watched 
                AFTER UPDATE ON watchlist 
                BEGIN   
                  INSERT INTO watchedCourses (
                                      initial_id,
                                      Name,
                                      Duration,
                                      Score)
                    VALUES (
                            OLD.id,
                            OLD.Name,
                            OLD.Duration,
                            NEW.Score
                    );
                END;
                '''
    cur.execute(query)

def insertCourse(cur, Name, Duration = None, Score = None):
    if Duration == None and Score == None:
        cur.execute(''' INSERT INTO watchlist (Name) VALUES (?);''', (Name,))
    elif Duration == None:
        cur.execute(''' INSERT INTO watchlist (Name, Score) VALUES (?, ?);''',
                    (Name, Score,))
    elif Score == None:
        cur.execute(''' INSERT INTO watchlist (Name, Duration) VALUES (?, ?);''',
                    (Name, Duration,))
    else:
        cur.execute(''' INSERT INTO watchlist (Name, Duration, Score) 
                    VALUES (?, ?, ?);''',
                    (Name, Duration, Score,))
  
def getRandomCourse(cur):
    # #cur.execute('''SELECT * FROM watchlist 
    #                   WHERE id IN (SELECT id FROM watchlist ORDER BY RANDOM())
    #                    Limit 1''')    
    #return cur.fetchall()
    return random.choice(viewTable(cur,'watchlist'))

def viewTable(cur,table_name):
    query = f'''SELECT * FROM {table_name}'''
    cur.execute(query)
    res=[]
    rows = cur.fetchall()
    for row in rows:
        res.append(row)
    return res

def dropTable(cur):
    cur.execute('''DROP TABLE watchlist''')

def deleteCourse(cur, Name):
    cur.execute('''DELETE FROM watchlist WHERE Name = ?''', [Name]);
  
def rateCourse(cur, Name, Score):
    cur.execute('''UPDATE watchlist
                      SET Score = ? 
                        WHERE Name = ?
                ''', (Score, Name))
  