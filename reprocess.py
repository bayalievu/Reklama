workspace = "/home/monitor/Workspace/"
import sys
sys.path.insert(0, workspace+"echoprint-server/API")
import MySQLdb
import os
import time    
import fp
import datetime

def reprocess(fid,decoded,date_played,time_played,radio,radio_id):

        result = fp.best_match_for_query(decoded)
        if result.TRID and result.TRID not in ignored_songs:
		logfile.write("Melody is recognized: "+result.TRID+",")
		#Melody is recognized
		track_id = result.TRID
		current = convertTimeToMinutes(time_played)
		global last_time,last_radio,recognized,last_date
		#Insert only tracks which differ more than 5 minutes, it is do to prevent repeated insert from different parts of the same track
		if (last_radio is None) or (last_date is None) or (last_date != date_played) or (last_radio != radio_id) or (last_time == 0) or (current - last_time > 5):
			last_time=current
			last_radio=radio_id 
			last_date = date_played
			recognized = recognized + 1
			
			db = conn.cursor()    	
	   		logfile.write("Inserting track_id: " + track_id	+ " for fingerprint " +str(fid)+'\n')
	   		db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,date_played,time_played,radio_id))
	   		conn.commit()
			db.close()
				
			db = conn.cursor()    	
	   		logfile.write("Updating fingerprint " +str(fid)+ " as "+track_id +'\n')
			db.execute("""update fingerprint set status = 'Y', track_id = %s, time_identified=%s  where id = %s""",(track_id,getNowDateTime(),fid))
	   		conn.commit()
			db.close()
		else:			
			logfile.write("Track is already recognized from previous fingerprint "+radio+str(date_played)+":"+str(time_played)+'\n')
			db = conn.cursor()    	
	   		logfile.write("Updating fingerprint " +str(fid)+ " as Y" +'\n')
			db.execute("""update fingerprint set status = 'Y', time_identified=%s  where id = %s""",(getNowDateTime(),fid))
	   		conn.commit()
			db.close()
	return 0
		
def convertTimeToMinutes(t):
	(h, m, s) = str(t).split(':')
	result = int(h) * 60 + int(m)
	return result

def getNowTime():
	return time.strftime('%H:%M:%S')

def getNowDate():
	return time.strftime('%Y-%m-%d')
		
def getNowDateTime():
	return time.strftime('%Y-%m-%d %H:%M:%S')	

def melodyAddedYesterday():
	yesterday = datetime.datetime.now() + datetime.timedelta(-1)
	yesterday = yesterday.strftime('%Y-%m-%d') + '%'
	
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
        cursor = conn.cursor()

	cursor.execute("""select count(*) from uploaded_song where approved_flag =1 and melody_added_flag = 1 and melody_declined_flag = 0 and uploaded_date like %s""",(yesterday,))
	row = cursor.fetchone()
	
	if row[0] > 0:
		return True
	else:
		return False
	
	cursor.close()
	conn.close()

if __name__ == "__main__":
	import traceback
	logfile = open(workspace+"PyMusic/logs/reprocess"+getNowDateTime(), 'w',1)
	logfile.write(getNowDateTime()+'\n')
        last_time=0
	recognized = 0
	last_radio=None
	last_date=None
	
        ignored_songs =[]
        ignored_songs.append('TROWTHB14D0E92A254')

        conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	cursor = conn.cursor()

        try:
		if melodyAddedYesterday():
        		sevenDaysAgo = datetime.datetime.now() + datetime.timedelta(-7)
        		sevenDaysAgo = sevenDaysAgo.strftime('%Y-%m-%d')
			cursor.execute("""SELECT * FROM fingerprint where status='N' and date_played>=%s and date_played<=%s and radio_id not in (10,11,12,13) order by radio_id,date_played,time_played""",(sevenDaysAgo,getNowDate()))
			logfile.write(cursor._executed+'\n')
                	results = cursor.fetchall()
                	for row in results:
				fid = row[0]
				decoded = row[1]
				radio = row[2]
				date_played = row[3]
				time_played = row[4]
				radio_id = row[7]
				reprocess(fid,decoded,date_played,time_played,radio,radio_id)
		else:
			logfile.write("No melodies added yesterday, reprocessing will not start\n")
        except cursor.Error, e:
                logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
		cursor.close()
		logfile.close()
		conn.close()	
	except KeyboardInterrupt:
		logfile.write("Program was interrupted using keyboard"+'\n')
        	cursor.close()
		logfile.close()
		conn.close()	
		exit()
	except:
		logfile.write(str(traceback.format_exc()))
		raise
	
	logfile.write(getNowDateTime()+'\n')
	logfile.write("Songs recognized: " + str(recognized)+'\n')
	cursor.close()
	logfile.close()
	conn.close()	
