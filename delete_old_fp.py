import MySQLdb
import time    

def getNowDateTime():
	return time.strftime('%Y-%m-%d %H:%M:%S')	

if __name__ == "__main__":
	import datetime
	import traceback
	start_date = datetime.datetime.now() + datetime.timedelta(-30)
	logfile = open("/home/monitor/Workspace/PyMusic/logs/delete_old_fp_log", 'a',1)
	logfile.write(getNowDateTime()+'\n')
	logfile.write("Deleting fingerprint older than(inclusive):"+start_date.strftime('%Y-%m-%d')+'\n')
	
        conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	cursor = conn.cursor()

        try:
                
		cursor.execute("""delete FROM fingerprint where date_played<=%s""",(start_date.strftime('%Y-%m-%d'),))
		conn.commit()
		logfile.write(cursor._executed+'\n')
        
	except cursor.Error, e:
                logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
		logfile.close()
		cursor.close()
		conn.close()
		exit()	
	except:
		logfile.write(str(traceback.format_exc()))	
		raise
	logfile.write(getNowDateTime()+'\n')
	logfile.close()
	cursor.close()
	conn.close()	
