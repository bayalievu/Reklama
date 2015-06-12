workspace = "/home/monitor/Workspace/"
import sys
sys.path.insert(0, workspace+"echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp
import traceback

codegen_path = os.path.abspath(workspace + "echoprint-codegen/echoprint-codegen")

import simplejson as json
import simplejson.scanner

# In sesonds
time_shift = 10
part_duration = 30
number_of_parts = part_duration/time_shift
default_song_duration = 240

def codegen(file, start=0, duration=part_duration):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)                      
    	r = p.communicate()
	
	try:
		code = json.loads(r[0])
	except simplejson.scanner.JSONDecodeError:
		logfile.write(getNowDateTime()+":Json cannot be decoded "+str(r[0])+"\n")
		return None
    	
	return code

def process_file(filename):

	codes = codegen(filename)
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
	
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	
	last_tracks.append(result.TRID)
	global last_unknown,last_known
        if result.TRID and result.TRID not in ignored_songs:
                #Melody is recognized
                track_id = result.TRID
                #Insert tracks only once
                if ((last_known == 0) or (last_known != track_id)) and moreThanMatchesInLastTracks(track_id,1):
                        last_known=track_id

                        try:
				db = conn.cursor()
                                db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,getNowDate(),getNowTime(),radio_id))
                                conn.commit()
				db.close()
                        except db.Error, e:
                                logfile.write(getNowDateTime())
                                logfile.write(":Error %d: %s\n" % (e.args[0],e.args[1]))
                                conn.rollback()
				raise

	elif radio_id not in ignored_fp_radios and (convertTimeToSeconds(getNowTime())-last_unknown>part_duration or convertTimeToSeconds(getNowTime())-last_unknown<0) and result.TRID is None:
		last_unknown = convertTimeToSeconds(getNowTime())
		db = conn.cursor()    	
		db.execute("""INSERT INTO fingerprint(fp,radio,date_played,time_played,time_identified,status,radio_id,track_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(decoded,radio,getNowDate(),getNowTime(),None,'N',radio_id,None))
                conn.commit()
                db.close()
	
	conn.close()

def moreThanMatchesInLastTracks(track,match):
	c = 0
	for x in last_tracks:
		if x == track:
			c = c + 1
	return c > match

def convertTimeToSeconds(t):
        (h, m, s) = str(t).split(':')
        result = int(h)*60*60 + int(m)*60 + int(s)
        return result

def getNowTime():
       return time.strftime('%H:%M:%S')

def getNowDate():
       return time.strftime('%Y-%m-%d')
       
def getNowDateTime():
       return time.strftime('%Y-%m-%d %H:%M:%S')       
	

if __name__ == "__main__":
 	import urllib2
	import collections
        from datetime import datetime
        from datetime import timedelta
       
	if len(sys.argv) < 4:
                print "Usage: python test.py radio radio_id stream"
                exit()

	ignored_songs =['TROWTHB14D0E92A254']

	last_known=0
	last_unknown = 0
        radio = sys.argv[1]
	radio_id = sys.argv[2]
        stream = sys.argv[3]
        ignored_fp_radios = ['10','11','12','13']
	
	logfile = open(workspace+"PyMusic/logs/radio"+radio+"TestIdentify"+getNowDateTime(), 'w',1)
	last_tracks = collections.deque(maxlen=default_song_duration/time_shift)	
	
	try:	
	   	url=urllib2.urlopen(stream)
	
		files = collections.deque(maxlen=number_of_parts)       
		
		while True:
                	filename = workspace+"PyMusic/wavs/parts"+radio+getNowDateTime()+'.mp3'
                	f=file(filename, 'wb')

                	# Basically a timer
                	t_start = datetime.now()
                	t_end = datetime.now()
                	t_end_old = t_end

                	# Record in chunks until
                	while t_end-t_start < timedelta(seconds=time_shift):
                        	f.write(url.read(1024))
                        	t_end = datetime.now()
                	f.close()
			
			if (len(files) == number_of_parts):
				files.append(f)
				
				merged_file = workspace+"PyMusic/wavs/merged"+radio+getNowDateTime()+'.mp3'
                        	big_file=file(merged_file, 'wb')
				
				for x in files:
					t = open(os.path.abspath(x.name),'r')
					big_file.write(t.read())
					t.close()
				big_file.close()
				
				try:		
					process_file(merged_file) 
				except IOError:
					logfile.write(getNowDateTime()+":Unexpected error:" + str(traceback.format_exc()))
				
			else:
				files.append(f)
			
	except KeyboardInterrupt:
		logfile.close()
		url.close()
		f.close()
		exit()
	except:
    		logfile.write(getNowDateTime()+":Unexpected error:" + str(traceback.format_exc()))
    		raise
