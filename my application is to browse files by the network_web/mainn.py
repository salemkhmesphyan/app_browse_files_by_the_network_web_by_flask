# -*- coding:utf8 -*-
"""
programmer by en:salem khmes phyan
"""
import os
import sys

from flask import Flask,render_template,request,send_file,flash,redirect,url_for,session
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret"
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
@app.route("/",methods=['GET','POST'])#methods=['GET']
def home():
	s=os.getcwd()
	#f=s+'/static/vid'
	lifil=['img','sound','vid']
	litbl=['tb1','tb2','tb3']
	all_tbl=[]
	#y=os.listdir(f)
	trns='0'
	a=1
	b=1
	msg=''
	im=0;sou=0;vi=0
	db=sqlite3.connect("db_home.db")
	db.row_factory=sqlite3.Row
	db.execute('create table if not exists tb1(ID integer primary Key autoincrement,namedb text,path text)')
	db.execute('create table if not exists tb2(ID integer primary Key autoincrement,namedb text,path text)')
	db.execute('create table if not exists tb3(ID integer primary Key autoincrement,namedb text,path text)')
	db.commit()
	f=db.cursor()
	for tb in litbl:
		f.execute("select * from {}".format(tb))
		df=f.fetchall()
		if len(df)>0:
			for p in df:
				all_tbl.append(p[1])
	for n in lifil:
		for m in os.listdir(s+'/static/'+n):
			if m in all_tbl:
				pass
			else:
				if b==1:
					im+=1
				elif b==2:
					sou+=1
				else:vi+=1
		b+=1
	if im>0:
		msg=str(im)+'هناك صور جديدة'	
	if sou>0:
		if msg=='':
			msg=str(im)+'هناك مقاطع صوت جديدة '
		else:
			msg=msg+' '+str(sou)+'ومقاطع صوت جديدة '
	if vi>0:
		if msg=='':
			msg=str(im)+'هناك مقاطع فيديو جديدة '
		else:
			msg=msg+' '+str(vi)+'ومقاطع فيديو جديدة '	
	if msg!='':
		flash(msg)			
	db.close()	
	return render_template('home1.html',a=a,trns=trns)
@app.route("/addfiles",methods=['GET','POST'])#methods=['GET']
def addfiles():#page hom
	trns='0'
	return render_template('ded.html',trns=trns)
@app.route("/addfile",methods=['GET','POST'])#methods=['GET']
def addfile():#page hom
	s=os.getcwd()
	
	lifile=[]
	db1=sqlite3.connect("db_home.db")
	db1.row_factory=sqlite3.Row
	got= request.form
	typ=str(got['sele'])
	if typ=='image':
		#~ db2=db1.execute("select * from tb1")
		#~ for h in db2:
		f=s+'/static/img/'
		y=os.listdir(f)
			
		target=os.path.join(APP_ROOT,'static/img/')
	elif typ=='video':
		f=s+'/static/vid/'
		y=os.listdir(f)
		target=os.path.join(APP_ROOT,'static/vid/')
	else:
		f=s+'/static/sound/'
		y=os.listdir(f)
		target=os.path.join(APP_ROOT,'static/sound/')
	if not os.path.isdir(target):
		os.mkdir(target)
	for fill in request.files.getlist("data"):
		filename=fill.filename
		if filename in y:
			flash(u"الملف موجود")
			
		else:
			
			dest="/".join([target,filename])
			fill.save(dest)
			if typ=='image':
				db1.execute("insert into tb1(namedb,path) values(?,?)",(filename,'img/'+filename))
				db1.commit()
			elif typ=='video':
				db1.execute("insert into tb3(namedb,path) values(?,?)",(filename,'vid/'+filename))
				db1.commit()
			else:
				db1.execute("insert into tb2(namedb,path) values(?,?)",(filename,'sound/'+filename))
				db1.commit()
			#dest="/".join([target,filename])
	flash(u"تم اضافة الملف بنجاح")
	return redirect(url_for('addfiles'))
@app.route("/show<var>",methods=['GET','POST'])#methods=['GET']
def show(var):#page hom
	db1=sqlite3.connect("db_home.db")
	cb=db1.cursor()
	#cb.execute("select * from sections where section='{}'".format(nb))
	#db2=cb.fetchall()
	ln=''
	if var=='1':
		trns='1'
		cb.execute("select distinct namedb,path from tb1")
		db2=cb.fetchall()
		ln=len(db2)
	elif var=='2':
		trns='2'
		cb.execute("select distinct namedb,path from tb2")
		db2=cb.fetchall()
		ln=len(db2)
	else:
		trns='3'
		cb.execute("select distinct namedb,path from tb3")
		db2=cb.fetchall()
		ln=len(db2)
	
	
	return render_template('video.html',d=var,db2=db2,trns=trns,ln=ln)
@app.route("/showone<var>",methods=['GET','POST'])#methods=['GET']
def showone(var):#page hom
	num=0
	db1=sqlite3.connect("db_home.db")
	db1.row_factory=sqlite3.Row
	#print(var[:3])
	if var[:3]=='img':
		num='1'
		trns='1'
		var="img/"+var[3:]
		db2=db1.execute("select distinct namedb,path from tb1")
	elif var[:3]=='vid':
		num='2'
		trns='2'
		var="vid/"+var[3:]
		db2=db1.execute("select distinct namedb,path from tb3")
	else:
		num='3'
		trns='3'
		var="sound/"+var[5:]
		db2=db1.execute("select distinct namedb,path from tb2")
	
	
	return render_template('sond.html',trns=trns,var=var,num=num,db2=db2)
@app.route("/search<var_s>",methods=['POST'])#methods=['GET']
def search(var_s):
	db1=sqlite3.connect("db_home.db")
	cb=db1.cursor()
	#cb.execute("select * from sections where section='{}'".format(nb))
	#db2=cb.fetchall()
	ln=''
	data = request.form
	worser=(data['ser'])
	if var_s=='1':
		trns='1'
		cb.execute("select distinct namedb,path from tb1 where namedb like '%{}%'".format(worser))
		db2=cb.fetchall()
		ln=len(db2)
	elif var_s=='2':
		trns='2'
		cb.execute("select distinct namedb,path from tb2 where namedb like '%{}%'".format(worser))
		db2=cb.fetchall()
		ln=len(db2)
	else:
		trns='3'
		cb.execute("select distinct namedb,path from tb3 where namedb like '%{}%'".format(worser))
		db2=cb.fetchall()
		ln=len(db2)
	return render_template('ser.html',trns=trns,d=var_s,db2=db2,ln=ln)
@app.route("/delfile<var_de>",methods=['GET','POST'])#methods=['GET']
def delfile(var_de):
	s=os.getcwd()
	rr='0'
	delf=''
	db1=sqlite3.connect("db_home.db")
	db1.row_factory=sqlite3.Row
	#print(var[:3])
	if var_de[:3]=='img':
		rr='1'
		
		db2=db1.execute("delete from tb1 where namedb='{}'".format(var_de[3:]))
		db1.commit()
		f=s+'/static/img/'
		os.remove(f+var_de[3:])
		delf=var_de[3:]
	elif var_de[:3]=='vid':
		rr='3'
		#var[3:]
		db2=db1.execute("delete from tb3 where namedb='{}'".format(var_de[3:]))
		db1.commit()
		f=s+'/static/vid/'
		os.remove(f+var_de[3:])
		delf=var_de[3:]
	else:
		rr='2'
		db2=db1.execute("delete from tb2 where namedb='{}'".format(var_de[5:]))
		db1.commit()
		f=s+'/static/sound/'
		os.remove(f+var_de[5:])
		delf=var_de[5:]
	if delf!='':
		flash(delf+" "+"تم حذف الملف")
	return redirect(url_for('show',var=rr))
if __name__ == "__main__":
	app.run(debug=True)
