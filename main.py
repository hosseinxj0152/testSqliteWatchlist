from functions import *

cur, con = createConnection('CourseWatchlist.db')

createMainTable(cur,'watchlist')
createSecondaryTable(cur, 'watchedCourses')

#insertCourse(cur, 'SQL Essentials Training')
#insertCourse(cur, 'Creating a Business Plan')
#insertCourse(cur, 'Foundations, Data, Data, Evevrywhere')
#rateCourse(cur, 'SQL Essentials Training', 8)


print(getRandomCourse(cur))

#print(viewTable(cur, 'watchlist'))
print(viewTable(cur, 'watchedCourses'))
con.commit()
