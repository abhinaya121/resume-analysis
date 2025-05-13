from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as mplt
from pyresparser import ResumeParser

global uname, job_id

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def Aboutus(request):
    if request.method == 'GET':
       return render(request, 'Aboutus.html', {})

def Feedback(request):
    if request.method == 'GET':
       return render(request, 'Feedback.html', {})

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username from signup where username = '"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == email:
                    status = 'Given Username already exists'
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,email_id,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Signup Process Completed'
        context= {'data':status}
        return render(request, 'Signup.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    uname = username
                    option = 1
                    break
        if option == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == "admin" and password == "admin":
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)          

def PostJobs(request):
    if request.method == 'GET':
       return render(request, 'PostJobs.html', {})

def Feedback(request):
    if request.method == 'GET':
        return render(request, 'Feedback.html', {})

def Aboutus(request):
    if request.method == 'GET':
        return render(request, 'Aboutus.html', {})     

def FeedbackAction(request):
    if request.method == 'POST':
        global uname
        uname = "XYZ"
        today = date.today()
        feedback = request.POST.get('t1', False)
        rank = request.POST.get('t2', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO feedback(username,feedback,feedback_date,feedback_rank) VALUES('"+uname+"','"+feedback+"','"+str(today)+"','"+rank+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Your feedback accepted and admin will review & getback'
        context= {'data':status}
        return render(request, 'Feedback.html', context)        

def PostJobsAction(request):
    if request.method == 'POST':
        job = request.POST.get('t1', False)
        details = request.POST.get('t2', False)
        company = request.POST.get('t3', False)
        salary = request.POST.get('t4', False)
        skills = request.POST.getlist('t5')
        skills = ','.join(skills)
        today = date.today()
        status = 'none'
        job_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select count(job_id) from postjob")
            rows = cur.fetchall()
            for row in rows:
                job_id = row[0]
        job_id = job_id + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO postjob(job_id,job_name,job_details,skills,post_date,company_name,salary) VALUES('"+str(job_id)+"','"+job+"','"+details+"','"+skills+"','"+str(today)+"','"+company+"','"+salary+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Job details posted with ID : '+str(job_id)
        context= {'data':status}
        return render(request, 'PostJobs.html', context)       

def ViewFeedback(request):
    if request.method == 'GET':
        output = '<table border=1><tr>'
        output+='<td><font size="" color="black">Feedback</td>'
        output+='<td><font size="" color="black">Feedback Date</td>'
        output+='<td><font size="" color="black">Feedback Rank</td></tr>'
        rank = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM feedback")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td></tr>'
                rank.append(row[3])
        output += "</table><br/><br/><br/>"
        unique, count = np.unique(np.asarray(rank), return_counts=True)
        mplt.pie(count,labels=unique,autopct='%1.1f%%')
        mplt.title('Feedback Ranking Graph')
        mplt.axis('equal')
        mplt.show()
        context= {'data': output}
        return render(request, 'ViewFeedback.html', context)
    
def getScore(job_id, skills):
    require_skills = None
    score = 0
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select skills FROM postjob where job_id='"+job_id+"'")
        rows = cur.fetchall()
        for row in rows:
            require_skills = row[0]
    require_skills = require_skills.strip().split(",")
    for i in range(len(skills)):
        skills[i] = skills[i].lower().strip()
    for i in range(len(require_skills)):
        require_skills[i] = require_skills[i].lower()
    print(require_skills)    
    found_skills = [x for x in skills if x in require_skills]
    if len(found_skills) > 0:
        if len(found_skills) >= len(require_skills):
            score = 100
        else:
            score = len(found_skills) / len(require_skills)
            score = score * 100
    return score       
    

def UploadResumeAction(request):
    if request.method == 'POST':
        global uname
        job_id = request.POST.get('t1', False)
        myfile = request.FILES['t2']
        fname = request.FILES['t2'].name
        today = date.today()
        fs = FileSystemStorage()
        filename = fs.save('ResumeAnalysisApp/static/resumes/'+fname, myfile)
        data = ResumeParser('ResumeAnalysisApp/static/resumes/'+fname).get_extracted_data()
        skills = data['skills']
        score = getScore(job_id, skills)
        data = str(data)
        data = data.replace("'", "")
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO upload_resume(job_id,username,resume_name,upload_date,resume_json,resume_score) VALUES('"+str(job_id)+"','"+uname+"','"+fname+"','"+str(today)+"','"+str(data)+"','"+str(score)+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Your resume submitted with score : '+str(score)
        context= {'data':status}
        return render(request, 'UserScreen.html', context)
        
        

def UploadResume(request):
    if request.method == 'GET':
        job_id = request.GET.get('t1', False)
        output = '<tr><td><font size="" color="black">Job&nbsp;ID</b></td><td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value="'+job_id+'" readonly/></td></tr>'
        context= {'data':output}
        return render(request, 'UploadResume.html', context)

def ViewJobs(request):
    if request.method == 'GET':
        output = '<table border=1><tr><th><font size="" color=black>Job ID</font></th>'
        output+='<td><font size="" color="black">Job Name</td>'
        output+='<td><font size="" color="black">Job Details</td>'
        output+='<td><font size="" color="black">Suggested Skills</td>'
        output+='<td><font size="" color="black">Posted Date</td>'
        output+='<td><font size="" color="black">Company Name</td>'
        output+='<td><font size="" color="black">Salary</td>'
        output+='<td><font size="" color="black">Tips</td>'
        output+='<td><font size="" color="black">Upload Result</td></tr>'
        rank = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM postjob")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                output+='<td><font size="" color="black">Must be Proficient</td>'
                output+='<td><a href=\'UploadResume?t1='+str(row[0])+'\'><font size=3 color=black>Click Here to Upload Resume</font></a></td></tr>'                
        output += "</table><br/><br/><br/>"
        context= {'data': output}
        return render(request, 'UserScreen.html', context)
    
def ViewScore(request):
    if request.method == 'GET':
        output = '<table border=1><tr><th><font size="" color=black>Job ID</font></th>'
        output+='<td><font size="" color="black">Username</td>'
        output+='<td><font size="" color="black">Resume Name</td>'
        output+='<td><font size="" color="black">Upload Date</td>'
        output+='<td><font size="" color="black">Resume JSON Data</td>'
        output+='<td><font size="" color="black">Resume Score</td></tr>'
        rank = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeanalysis',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM upload_resume")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td></tr>'                
        output += "</table><br/><br/><br/>"
        context= {'data': output}
        return render(request, 'ViewFeedback.html', context)


    

