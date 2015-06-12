workspace = "/home/monitor/Workspace/"
import sys
sys.path.insert(0, workspace +"echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp
from pydub import AudioSegment
import collections
import urllib2
import datetime

codegen_path = os.path.abspath(workspace+"echoprint-codegen/echoprint-codegen")

import simplejson as json
import simplejson.scanner

part_length = 30

radios= { 'MinKiyal': '1', 'Obondoru': '2','Tumar': '3', 'Sanjyra': '4','ManasJanyrygy': '5', 'MaralFM': '6','KyrgyzRadiosu': '7', 'OK': '8'}

def getNowTime():
	return time.strftime('%H:%M:%S')

def getNowDate():
	return time.strftime('%Y-%m-%d')
		
def getNowDateTime():
	return time.strftime('%Y-%m-%d %H:%M:%S')	

def codegen(file, start=0, duration=part_length):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)                      
    	r = p.communicate()
	
	try:
		code = json.loads(r[0])
	except simplejson.scanner.JSONDecodeError:
		return None
    	
	return code

def process_file(filename,t):

	codes = codegen(filename)
	if codes is None:
		return -2
	if len(codes) == 0:
		return -3
	if "code" not in codes[0]:
		return -4

        decoded = fp.decode_code_string(codes[0]["code"])
        result = fp.best_match_for_query(decoded)
        
	if result.TRID:
		#Melody is recognized
                track_id = result.TRID
                global last,time
                #Insert tracks only once
                if (last == 0) or (last != track_id):
                        last=track_id
			mytime = time + datetime.timedelta(seconds=t)
			
			conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
			db = conn.cursor()
                        db.execute("""INSERT INTO test_played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,date,mytime.time(),radio_id))
                        conn.commit()
                	db.close()
			conn.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
                print "Usage: python file_identify.py filename"
                exit()

        filename = sys.argv[1]
	last = 0
	date = None
	time = None
	
	x = filename.split('/')[2].split('.')[0].split('_')
	radio = x[0]
	if radio == 'KG':
		radio_id = radios[x[1]]
		date = x[2]
		time = datetime.datetime(1999,1,1,int(x[3][:2]),00,00)
	else:
		radio_id = radios[radio]
		date = x[1]
		time = datetime.datetime(1999,1,1,int(x[2][:2]),00,00)
	
        segment = AudioSegment.from_mp3(filename)

        one_minute = part_length * 1000
        length = len(segment)
        parts = length/one_minute
			
        for i in range(parts):
                part = segment[i*one_minute:(i+1)*one_minute]
                part.export(workspace+"PyMusic/missed/"+"%09d"%i+".mp3", format="mp3",bitrate="80k")
			
	t = 0
        # Process files sorted by modified time
        files = sorted(glob(workspace+'PyMusic/missed/*.mp3'))
        print "Number of files: "+ str(len(files))
        for filename in files:
                process_file(filename,t)
		t = t+part_length
	
