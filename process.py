import MySQLdb
import sys
import os
import subprocess32
from transliterate import translit
from glob import glob
import simplejson as json
workspace = "/home/ulan/"
sys.path.insert(0, workspace + "echoprint-server/API")
import fp
import time
codegen_path = os.path.abspath(workspace+"echoprint-codegen/echoprint-codegen")

def getNowTime():
        return time.strftime('%H:%M:%S')

def getNowDate():
        return time.strftime('%Y-%m-%d')

def getNowDateTime():
       return time.strftime('%Y-%m-%d %H:%M:%S')
	
companies = {}

def codegen(file):
    proclist = [codegen_path, os.path.abspath(file)]
    p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)
    code = p.communicate()[0]
    return json.loads(code)

def parse_json(c):
        code = c["code"]
        m = c["metadata"]
        if "track_id" in m:
            trid = m["track_id"].encode("utf-8")
        else:
            trid = fp.new_track_id()
        length = m["duration"]
        version = m["version"]
        artist = m.get("artist", None)
        title = m.get("title", None)
        release = m.get("release", None)
        decoded = fp.decode_code_string(code)

        data = {"track_id": trid,
            "fp": decoded,
            "length": length,
            "codever": "%.2f" % version
        }

        if artist: data["artist"] = artist
        if release: data["release"] = release
        if title: data["track"] = title

    	return data

def process_file(absoluteFilename,c):
	#Get filename from absolute path
	filename = absoluteFilename.split('/')[-1].split("-")	
	
	#Get company from filename
	company=filename[0].strip()
        logfile.write(absoluteFilename+'\n')
	
	#Get reklama name from filename
	name = filename[1].strip()
	
	#Get language
	language = filename[2].strip().split(".")[0]

	#Add artists to Database
	company_id=addCompanyToDb(company)
	
	#Get track id
	code = parse_json(c[0])	
	track_id =code["track_id"]
	length = code["length"]
	
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="reklama",charset='utf8')
	db = conn.cursor()
	
	try:
		#Insert into melody table
	   	db.execute("""INSERT INTO reklama(track_id,company_id,name,filename,length,language,date_added,status,company) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(track_id,company_id,name,absoluteFilename,length,language,getNowDate(),'Y',company))
	   	logfile.write("Inserted track to database "+track_id+'\n')
	   	conn.commit()
		
		#Save fingerprint in Solr
		fp.ingest(code, do_commit=False)
    		fp.commit()
	except db.Error, e:
           	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
	   	conn.rollback()
	
	db.close()
	conn.close()


def addCompanyToDb(company):
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="reklama",charset='utf8')
	db = conn.cursor()
	company_id = None
	
	s = company.decode("utf-8")	
	if not s in companies.keys():
                try:
                        db.execute("""INSERT INTO company(name) VALUES (%s)""",(s,))
                        conn.commit()
			company_id = db.lastrowid
			companies[s]=company_id
                except db.Error, e:
                        logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
                        conn.rollback()
	else:
		company_id = companies[s]
	
	db.close()
	conn.close()
	return company_id

def getCompanies():
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="reklama",charset='utf8')
        db = conn.cursor()

        sql = "SELECT * FROM company"

        try:
                db.execute(sql)
                results = db.fetchall()
                for row in results:
			i = row[0]
                        name = row[1].strip()
                        companies[name]=i
	except db.Error, e:
        	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
	
	db.close()
	conn.close()

#Check if reklama fingerprint is already in Solr
def reklamaExists(filename,c):
	decoded = fp.decode_code_string(c[0]["code"])
        result = fp.best_match_for_query(decoded)
        if result.TRID:
		logfile.write(filename+" is already in the database\n")
        	return True
	else:
		return False


if __name__ == "__main__":
	if len(sys.argv) < 2:
        	print "Usage: python process.py mp3path"
                exit()

        mp3path = sys.argv[1]
	
	getCompanies()

	logfile = open(workspace+'Reklama/logs/logfileProcess'+getNowDateTime(), 'w', 1)
	
	files = glob(mp3path)
	files.sort()
    	for filename in files:
		c=codegen(filename)
        	if c is None or len(c)==0 or "code" not in c[0]:
			logfile.write("No code is generated for: " + filename+'\n')
			continue
 		#Add melody if it does not already exists
		if not reklamaExists(filename,c):
       			process_file(filename,c)

	logfile.close()
