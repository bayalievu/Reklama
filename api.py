#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by Brian Whitman on 2010-06-16.
Copyright (c) 2010 The Echo Nest Corporation. All rights reserved.
"""
from __future__ import with_statement

import web
import fp
import re
import MySQLdb
import time

try:
    import json
except ImportError:
    import simplejson as json

# Very simple web facing API for FP dist

urls = (
    '/query', 'query',
    '/identify', 'identify',
    '/query?(.*)', 'query',
    '/identify?(.*)', 'identify',
    '/ingest', 'ingest',
)


class ingest:
    def POST(self):
        params = web.input(track_id="default", fp_code="", artist=None, release=None, track=None, length=None, codever=None)
        if params.track_id == "default":
            track_id = fp.new_track_id()
        else:
            track_id = params.track_id
        if params.length is None or params.codever is None:
            return web.webapi.BadRequest()
        
        # First see if this is a compressed code
        if re.match('[A-Za-z\/\+\_\-]', params.fp_code) is not None:
           code_string = fp.decode_code_string(params.fp_code)
           if code_string is None:
               return json.dumps({"track_id":track_id, "ok":False, "error":"cannot decode code string %s" % params.fp_code})
        else:
            code_string = params.fp_code

        data = {"track_id": track_id, 
                "fp": code_string,
                "length": params.length,
                "codever": params.codever }
        if params.artist: data["artist"] = params.artist
        if params.release: data["release"] = params.release
        if params.track: data["track"] = params.track
        fp.ingest(data, do_commit=True, local=False)

        return json.dumps({"track_id":track_id, "status":"ok"})
        
    
class query:
    def POST(self):
        return self.GET()
        
    def GET(self):
        stuff = web.input(fp_code="")
        response = fp.best_match_for_query(stuff.fp_code)
        return json.dumps({"ok":True, "query":stuff.fp_code, "message":response.message(), "match":response.match(), "score":response.score, \
                        "qtime":response.qtime, "track_id":response.TRID, "total_time":response.total_time})

last_tracks={}
class identify:
    def POST(self):
        return self.GET()
        
    def GET(self):
	track_id = None
        stuff = web.input(fp_code="",radio="")

	decoded = fp.decode_code_string(stuff.fp_code)
        response = fp.best_match_for_query(decoded)
	print response.TRID
 	
	if response.TRID:
        	track_id = response.TRID
		radio = stuff.radio
	        #Insert tracks only once
		if radio not in last_tracks or last_tracks[radio] != track_id:
                	last_tracks[radio] = track_id
                	now = time.strftime('%Y-%m-%d %H:%M:%S')

                	db = conn.cursor()

                	try:
                        	print "Inserting track_id: " + track_id
                        	db.execute("""INSERT INTO played_melody(track_id,melody_id,radio,time_played) VALUES (%s,%s,%s,%s)""",(track_id,None,radio,now))
                        	conn.commit()
                	except db.Error, e:
                        	print "Error %d: %s" % (e.args[0],e.args[1])
                        	conn.rollback()
        	else:
                	print "Track is already recognized from other file"
	else:
                print "No match found for the code"

        return json.dumps({"ok":True, "query":stuff.fp_code, "message":response.message(), "match":response.match(), "score":response.score, \
                        "qtime":response.qtime, "track_id":response.TRID, "total_time":response.total_time})




application = web.application(urls, globals())#.wsgifunc()
conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')
        
if __name__ == "__main__":
    application.run()

