from pydub import AudioSegment
import sys
sys.path.insert(0, "/home/ulan/echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp

last=0
codegen_path = os.path.abspath("/home/ulan/echoprint-codegen/echoprint-codegen")

import simplejson as json


def codegen(file, start=0, duration=30):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)                      
    	r = p.communicate()
	code = r[0]      
    	return json.loads(code)

def process_file(filename,radio):
	now_time = time.strftime('%H:%M:%S')
	now_date = time.strftime('%Y-%m-%d')
	db = conn.cursor()
    	
	codes = codegen(filename)
	track_id = None
    	if len(codes)>0 and "code" in codes[0]:
        	decoded = fp.decode_code_string(codes[0]["code"])
        	result = fp.best_match_for_query(decoded)
        	if result.TRID:
			track_id = result.TRID
		else:
			#Insert melody to unknown fingerprints table with status 'N'
			logfile.write("No match found for the file, inserting unknown melody to fingerprint table")
                        db.execute("""INSERT INTO fingerprint(fp,radio,date_played,time_played,time_identified,status) VALUES (%s,%s,%s,%s,%s,%s)""",(decoded,radio,now_date,now_time,None,'N'))
                        conn.commit()		
			db.close()	
			return -1
		
    	else:
        	logfile.write("Couldn't decode "+file+'\n')
		db.close()
		return -2
	
	global last
	#Insert tracks only once
	if (last == 0) or (last != track_id):
		last=track_id

		try:
	   		logfile.write("Inserting track_id: " + track_id	+ " for file: " + filename+'\n')
	   		db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played) VALUES (%s,%s,%s,%s)""",(track_id,radio,now_date,now_time))
	   		conn.commit()
		except db.Error, e:
           		logfile.write("Error %d: %s\n" % (e.args[0],e.args[1]))
	   		conn.rollback()
	else:
		logfile.write("Track is already recognized from other file "+filename+'\n')
	
	db.close()
	
	return 0

if __name__ == "__main__":
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')
	radio = "KG Obondoru"
	import alsaaudio, wave, numpy

	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
	inp.setchannels(2)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	logfile = open('logfileMicIdentify', 'w')
        last_result = -1	
	while True:
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		filename = 'wavs/mic'+now+'.wav'	
		w = wave.open(filename, 'w')
		w.setnchannels(2)
		w.setsampwidth(2)
		w.setframerate(44100)
		#Record 30 seconds and recognize
    		for i in range(int(30*44.1)):
			l, data = inp.read()
    			a = numpy.fromstring(data, dtype='int16')
    			w.writeframes(data)
		w.close()

		result = process_file(filename,radio) 
		if result == 0 or last_result == 0:
			os.remove(filename)
		last_result = result

	logfile.close()
	conn.close()	


