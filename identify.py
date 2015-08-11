workspace = "/home/monitor/Reklama/"
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import sys
sys.path.insert(0, workspace+"echoprint-server/API")
import fp
import traceback
import collections
import urllib2

codegen_path = os.path.abspath(workspace + "echoprint-codegen/echoprint-codegen")

import simplejson as json
import simplejson.scanner

time_shift = 2
min_duration = 28
max_duration = 28

def codegen(file,duration,start=0):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)                      
    	r = p.communicate()
	
	try:
		code = json.loads(r[0])
	except simplejson.scanner.JSONDecodeError:
		logfile.write(getNowDateTime()+":Json cannot be decoded "+str(r[0])+"\n")
		return None
    	
	return code

def process_file(filename,length):
	codes = codegen(filename,length)
	if codes is None:
		return -2
	if len(codes) == 0:
		logfile.write(getNowDateTime()+":Codegen returned empty list\n")
		return -3
	if "code" not in codes[0]:
		logfile.write(getNowDateTime()+":No code is returned by codegen\n")
		return -4

	track_id = None
        decoded = fp.decode_code_string(codes[0]["code"])
        result = fp.best_match_for_query(decoded)
	
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="reklama",charset='utf8')
	
        if result.TRID:
                #Melody is recognized
                track_id = result.TRID
		global last_track,last_time
		#Insert tracks only once
		if (last_track == None or moreThan2MinutesDifference(getNowTime(),last_time) or last_track != track_id):
			last_track = track_id
			last_time = getNowTime()
                	try:
				db = conn.cursor()
                        	db.execute("""INSERT INTO played_reklama(track_id,radio,date_played,time_played,radio_id,length,filename) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(track_id,radio,getNowDate(),getNowTime(),radio_id,length,filename))
                        	conn.commit()
				db.close()
                	except db.Error, e:
                        	logfile.write(getNowDateTime())
                        	logfile.write(":Error %d: %s\n" % (e.args[0],e.args[1]))
                        	conn.rollback()
				raise
			conn.close()
			return 0
	else:
		conn.close()
		return -1

def convertTimeToMinutes(t):
        (h, m, s) = str(t).split(':')
        result = int(h) * 60 + int(m)
        return result

def moreThan2MinutesDifference(t,last_time):
	difference =  convertTimeToMinutes(t) - convertTimeToMinutes(last_time) 
	if difference > 2 or difference < 0:
		return True
	else:
		return False

def getNowTime():
       return time.strftime('%H:%M:%S')

def getNowDate():
       return time.strftime('%Y-%m-%d')
       
def getNowDateTime():
       return time.strftime('%Y-%m-%d %H:%M:%S')       
	
if __name__ == "__main__":
	if len(sys.argv) < 4:
                print "Usage: python identify.py radio radio_id stream"
                exit()

        radio = sys.argv[1]
	radio_id = sys.argv[2]
        stream = sys.argv[3]
	last_track = None
	last_time = None

	logfile = open(workspace+"Reklama/logs/radio"+radio+"ReklamaIdentify"+getNowDateTime(), 'w',1)
	
	try:	
		number_files = max_duration/time_shift
		files = collections.deque(maxlen=number_files)
	   	url=urllib2.urlopen(stream)
		while True:
			#Read 2 seconds from 80Kb/s(10KB/s) stream (This number should change if stream bandwidth changes)
                        f = url.read(1024*10*time_shift)
			files.append(f)				
	
			if (len(files) == number_files):
				merged_file = workspace+"Reklama/wavs/merged"+radio+getNowDateTime()+"_"+str(time_shift)+'.mp3'
                        	big_file=open(merged_file, 'wb')
				
				for x in files:
					big_file.write(x)
				big_file.close()
				
				try:
					if process_file(merged_file,max_duration) != 0:
						os.remove(merged_file)
				except IOError:
                                	logfile.write(getNowDateTime()+":Unexpected error:" + str(traceback.format_exc()))

						
	except:
    		logfile.write(getNowDateTime()+":Unexpected error:" + str(traceback.format_exc()))
    		raise
