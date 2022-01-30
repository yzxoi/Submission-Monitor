# -*- coding: UTF-8 -*-
# encoding: utf-8

import requests
import time
import json
from lxml import etree
from lxml.html import fromstring, tostring

GETFREQ = 300
MAXCOUNT = 50
SMAX = 100
GETTIMEOUT = 20
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

# with open('cookies.json', 'r') as cookiesjson:
# 	cookies = json.load(cookiesjson)

# if len(cookies) == 0:
# 	print('No cookie found.')
# 	quit()

with open("data/users.json", 'r') as usersjson:
	user = json.load(usersjson)

if len(user) == 0:
	print('The plan is empty.')
	quit()

# platform, id, status, score, problem, problem_link, submitter, time, memory, answer, submission_link, submit_time
submissions = []

def GetCFUser(handle):
	global cnt, lastGet, MAXCOUNT, UA, GETTIMEOUT
	try:
		getheader = {
			"user-agent": UA
		}
		response = requests.get("http://codeforces.com/api/user.info?handles=" + str(handle), headers = getheader, timeout = GETTIMEOUT)
	except:
		print("Get Codeforces User failed.")
		return []
	else:
		data = json.loads(response.text)
		if (data['status'] != "OK"):
			print("Response Status Error");
			quit()
		for i in data['result']:
			t_user = []
			t_user.append(i['handle'])
			t_user.append(i['rank'])
		return t_user

def GetCodeforces(now):
	global cnt, lastGet, MAXCOUNT, UA, GETTIMEOUT
	lastGet = time.time()
	try:
		getheader = {
			"user-agent": UA
		}
		response = requests.get("http://codeforces.com/api/user.status" + "?handle=" + str(now['handle']) + "&from=1" + "&count=" + str(MAXCOUNT), headers = getheader, timeout = GETTIMEOUT)
	except:
		print("Get Codeforces Status failed.")
	else:
		# try:
			data = json.loads(response.text)
			if (data['status'] != "OK"):
				print("Response Status Error:" + data['status'] + "; Response Result:" + data['result']);
				quit()
			g_user = GetCFUser(now['handle'])
			for i in data['result']:
				submission = []
				submission.append("Codeforces")
				submission.append(str(i['id']))
				if(i['verdict'] == "OK"):
					submission.append("Accepted")
				elif(i['verdict'] == "WRONG_ANSWER"):
					submission.append("Wrong Answer")
				elif(i['verdict'] == "TIME_LIMIT_EXCEEDED"):
					submission.append("Time Limit Exceeded")
				elif(i['verdict'] == "COMPILATION_ERROR"):
					submission.append("Complile Error")
				elif(i['verdict'] == "RUNTIME_ERROR"):
					submission.append("Runtime Error")
				elif(i['verdict'] == "MEMORY_LIMIT_EXCEEDED"):
					submission.append("Memory Limit Exceeded")
				elif(i['verdict'] == "TESTING"):
					submission.append("Judging")
				elif(i['verdict'] == "SKIPPED"):
					submission.append("Skipped")
				else:
					submission.append("Unknown Error")
				if(i['verdict'] == "OK"):
					try:
						submission.append(str(int(i['problem']['rating'])))
					except:
						try:
							submission.append(str(int(i['problem']['points'])))
						except:
							submission.append("100")
				else:
					submission.append(str(0))
				submission.append("CF"+str(i['problem']['contestId'])+i['problem']['index'] + " " + i['problem']['name'])
				submission.append("https://codeforces.com/problemset/problem/"+str(i['problem']['contestId'])+"/"+i['problem']['index'])
				submission.append(g_user)
				if (i['timeConsumedMillis']):
					submission.append(str(i['timeConsumedMillis'])+" ms")
				else:
					submission.append("0 ms")
				if(i['memoryConsumedBytes']):
					submission.append(str(int(i['memoryConsumedBytes']/1024/1024)) + " MB")
				else:
					submission.append("0 MB")
				submission.append(i['programmingLanguage'])
				submission.append("https://codeforces.com/problemset/submission/"+str(i['author']['contestId'])+"/"+str(i['id']))
				submission.append(i['creationTimeSeconds'])

				submissions.append(submission)
				# file.write(str(i))
		# except:
		# 	print('Get Codeforces Response Parse Error.')

def GetUOJ(now,page):
	global cnt, lastGet, MAXCOUNT, UA, GETTIMEOUT, submissions
	lastGet = time.time()
	try:
		getheader = {
			"user-agent": UA
		}
		response = requests.get("https://uoj.ac/submissions?submitter=" + str(now['handle']) + "&page=" + str(page), headers = getheader, timeout = GETTIMEOUT,verify=False)
	except:
		print("Error No Such Page!")
	else:
		selector=etree.HTML(response.text)
		print(response.text)
		for i in range(1,11):
			try:
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/a/text()')[0]
				submission = []
				submission.append("UOJ")
				submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[4]/a/text()')[0]
				if(content == "100"):
					submission.append("Accepted")
					submission.append(content)
				elif(content == "Compile Error"):
					submission.append("Compile Error")
					submission.append("0")
				else:
					submission.append("Unaccepted")
					submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[2]/a/text()')[0]
				submission.append("UOJ"+content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[2]/a/@href')[0]
				submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[3]/span/text()')[0]
				submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[5]/text()')[0]
				submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[6]/text()')[0]
				submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[7]/a/text()')[0]
				submission.append(content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/a/text()')[0]
				submission.append("https://uoj.ac/submission/"+content)
				content=selector.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[9]/small/text()')[0]
				submission.append(time.mktime(time.strptime(content, "%Y-%m-%d %H:%M:%S")))

				submissions.append(submission)
			except:
				print("Error No Such Element!")

def GetColor(status):
	if(status == "Accepted"):
		return "forestgreen"
	elif(status == "Wrong Answer" or status == "Unaccepted"):
		return "red"
	elif(status == "Time Limit Exceeded"):
		return "sandybrown"
	elif(status == "Complile Error"):
		return "rgb(0, 68, 136)"
	elif(status == "Runtime Error"):
		return "darkorchid"
	elif(status == "Memory Limit Exceeded"):
		return "sandybrown"
	elif(status == "Judging"):
		return "#6cf"
	elif(status == "Skipped"):
		return "grey"
	else:
		return "#e28989"

def GetScoreColor(status):
	if(int(status) > 0):
		return "forestgreen"
	else:
		return "red"

def GetIconName(status):
	if(status == "Accepted"):
		return "done"
	elif(status == "Wrong Answer" or status == "Unaccepted"):
		return "close"
	elif(status == "Time Limit Exceeded"):
		return "access_time"
	elif(status == "Complile Error"):
		return "block"
	elif(status == "Runtime Error"):
		return "clear_all"
	elif(status == "Memory Limit Exceeded"):
		return "memory"
	elif(status == "Judging"):
		return "autorenew"
	elif(status == "Skipped"):
		return "skip_next"
	else:
		return "error"

def GetUserColor(status):
	if(status == "candidate master"):
		return "#a0a"
	elif(status == "master"):
		return "#ff8c00"
	elif(status == "grandmaster"):
		return "red"
	elif(status == "international master"):
		return "#ff8c00"
	elif(status == "expert"):
		return "blue"
	elif(status == "specialist"):
		return "#03a89e"
	elif(status == "pupil"):
		return "green"
	elif(status == "legendary grandmaster"):
		return "red"
	elif(status == "newbie"):
		return "gray"
	else:
		return "black"
def GetTime(now):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))

rk = []
def Sort(l,r):
    if(l>=r):
        return 
    mid = (l+r)/2
    mid=int(mid)
    Sort(l,mid)
    Sort(mid+1,r)
    j = l
    k = mid+1
    stk=[]
    while (j<=mid and k<=r):
        if(submissions[rk[j]][11]>submissions[rk[k]][11]):
            stk.append(rk[j])
            j=j+1
        else:
            stk.append(rk[k])
            k=k+1
    while (j<=mid):
        stk.append(rk[j])
        j=j+1
    while (k<=r):
        stk.append(rk[k])
        k=k+1
    for i in range(0,r-l+1):
        rk[i+l]=stk[i]

lastGet = 0
while True:
	if (time.time() - lastGet > GETFREQ):
		with open("index.html", "w", encoding="utf-8") as file:
			submissions = []
			for i in range(0,len(user)):
				if (user[i]['type'] == 'codeforces'):
					GetCodeforces(user[i])
				elif (user[i]['type'] == 'uoj'):
					GetUOJ(user[i],1)
					GetUOJ(user[i],2)
					GetUOJ(user[i],3)
			rk = []
			for i in range(0,len(submissions)):
				rk.append(i)
			Sort(0,len(submissions)-1)
			file.write('<!DOCTYPE html><html><head><meta http-equiv="refresh" content="300"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><title>Submission Monitor</title><link rel="shortcut icon" href="./favicon.ico" type="image/x-icon"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mdui@1.0.2/dist/css/mdui.min.css" /><link rel="stylesheet" href="monitor.css" /></head><body><div id="app"><div id="header"><div class="header-container"><div class="title">提交记录监视器<div class="subtitle">Submission Monitor</div></div></div></div><div id="monitor" class="container item mdui-card"><div class="mdui-table-fluid"><table class="mdui-table mdui-table-hoverable"><thead><tr><th>平台</th><th>状态</th><th>分数</th><th>题目</th><th>提交者</th><th>用时</th><th>内存</th><th>答案</th><th>提交时间</th></tr></thead><tbody>')
			for j in range(0,min(SMAX,len(submissions))):
				i=submissions[rk[j]]
				if (i[0]=='Codeforces'):
					file.write('<tr>')
					file.write('<td><a href="https://codeforces.com/"><img src="./Codeforces.png" /> Codeforces</a></td>')
					file.write('<td><a style="color:' + GetColor(i[2]) + ';vertical-align: middle;" href="' + i[10] + '"><i class="mdui-icon material-icons" style="height: 26px;">' + GetIconName(i[2]) + '</i> ' + i[2] + '</a></td>')
					file.write('<td><span style="color:' + GetScoreColor(i[3]) + ';">' + i[3] + '</span></td><td><a style="color:#4183c4;" href="' + i[5] + '">' + i[4] + '</td>')
					if(i[6][1] == "legendary grandmaster"):
						file.write('<td><a href="https://codeforces.com/profile/' + i[6][0] + '">' + '<span style="color:black;">' + i[6][0][0] + '</span>' + '<span style="color:red;">' + i[6][0][1:] + '</span>' + '</a></td>')
					else:
						file.write('<td><a href="https://codeforces.com/profile/' + i[6][0] + '" style="color:' + GetUserColor(i[6][1]) + ';">' + i[6][0] + '</a></td>')
					file.write('<td>' + i[7] + '</td><td>' + i[8] + '</td><td><span>' + i[9] + '</spane></td><td>' + GetTime(i[11]) + '</td>')
					file.write('</tr>')
				elif (i[0]=='UOJ'):
					file.write('<tr>')
					file.write('<td><a href="https://uoj.ac/"><img style="height:16px;" src="./UOJ.png" /> UOJ</a></td>')
					file.write('<td><a style="color:' + GetColor(i[2]) + ';vertical-align: middle;" href="' + i[10] + '"><i class="mdui-icon material-icons" style="height: 26px;">' + GetIconName(i[2]) + '</i> ' + i[2] + '</a></td>')
					file.write('<td><span style="color:' + GetScoreColor(i[3]) + ';">' + i[3] + '</span></td><td><a style="color:#4183c4;" href="' + i[5] + '">' + i[4] + '</td>')
					file.write('<td><a style="color:rgb(75, 175, 178);" href="https://uoj.ac/user/profile/' + str(i[6]) + '">' + str(i[6]) + '</a></td>')
					file.write('<td>' + i[7] + '</td><td>' + i[8] + '</td><td><span>' + i[9] + '</spane></td><td>' + GetTime(i[11]) + '</td>')
					file.write('</tr>')
			file.write('</tbody></table></div></div><div id="footer"><div class="container"><p>Powered By <a href="https://github.com/yzxoi/Submission-Monitor" target="_blank" rel="noopener noreferrer">yzxoi Submission Monitor</a></p></div></div></div><script src="https://cdn.jsdelivr.net/npm/mdui@1.0.2/dist/js/mdui.min.js"></script></body></html>')
			file.close()
			print("done")
