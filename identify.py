workspace = "/home/ulan/"
import sys
sys.path.insert(0, workspace+"echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp
import traceback
import collections
import urllib2

codegen_path = os.path.abspath(workspace + "echoprint-codegen/echoprint-codegen")

import simplejson as json
import simplejson.scanner

time_shift = 5
min_duration = 5
max_duration = 20
last_tracks = collections.deque(maxlen=5)

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
	
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="reklama",charset='utf8')
	
        if result.TRID:
                #Melody is recognized
                track_id = result.TRID
		last_tracks.append(track_id)
		global last_known
		#Insert tracks only once
		if ((last_known == None or last_known[0] != track_id) and moreThanMatchesInLastTracks(track_id,1)) or (moreThanMatchesInLastTracks(track_id,3) and moreThan2MinutesDifference(getNowTime())):
			last_known = (track_id,getNowTime())
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

def moreThanMatchesInLastTracks(track,match):
        c = 0
        for x in last_tracks:
                if x == track:
                        c = c + 1
        return c > match

def moreThan2MinutesDifference(t):
	difference =  convertTimeToMinutes(t) - convertTimeToMinutes(last_known[1]) 
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
	last_known = None

	logfile = open(workspace+"Reklama/logs/radio"+radio+"ReklamaIdentify"+getNowDateTime(), 'w',1)
	
	all_files = []
	for i in range(min_duration/time_shift,max_duration/time_shift):
		all_files.append(collections.deque(maxlen=i))
	
	try:	
	   	url=urllib2.urlopen(stream)
		while True:
			#Read 5 seconds from 80Kb/s(10KB/s) stream (This number should change if stream bandwidth changes)
                        f = url.read(1024*10*time_shift)
			
			for i in range(min_duration/time_shift,max_duration/time_shift):
				files = all_files[i-min_duration/time_shift]
				files.append(f)				
	
				if (len(files) == i):
					merged_file = workspace+"Reklama/wavs/merged"+radio+getNowDateTime()+"_"+str(i*time_shift)+'.mp3'
                        		big_file=open(merged_file, 'wb')
				
					for x in files:
						big_file.write(x)
					big_file.close()
				
					if process_file(merged_file,i*time_shift) != 0:
						os.remove(merged_file)
						
	except:
    		logfile.write(getNowDateTime()+":Unexpected error:" + str(traceback.format_exc()))
    		raise
