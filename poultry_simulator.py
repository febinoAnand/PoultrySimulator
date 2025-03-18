from flask import Flask,render_template,request
import serial
import time
import threading
import serial.tools.list_ports

weightValue = 0.0
isConnected = False
startGetValue = False
comport = ""

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("template.html")


@app.route("/vhl",methods=['POST'])
def VHLSchedule():
    print(str(request.json).replace("'",'"'))
    return '{"message":"Test OK","response":"Successfull","status":"1"}'


@app.route('/init')
def initStatus():
	global isConnected,comport
	status = "%s,%s,%s"%(isConnected,weightValue,comport)
	return status

@app.route('/toggleConnect')
def toggle():

	global isConnected,s,t,comport

	comport = str(request.args.get('comport'))
	print (comport)

	if not isConnected and comport != "" :
		try:
			s = serial.Serial(port=comport, baudrate=9600)
			isConnected = True
			t = threading.Thread(target=getvalue, args=(1,))
			readThread = threading.Thread(target=readValue, args=(1,))
			t.start()
			readThread.start()
		except Exception as e:
			isConnected = False
			print(e)

	elif isConnected:
		isConnected = False
		if s.is_open: s.close()
		if t.is_alive():    startGetValue = False

	# print ("Connection status="+str(isConnected))
	return str(isConnected)

@app.route('/getComList')
def getComList():
	connectedHTML = [""]
	htmlContent = '<option value="%s">%s</option>'
	htmlresponse = ""
	comlist = serial.tools.list_ports.comports()
	for n,element in enumerate(comlist):
		dev = element.device
		htmlresponse += htmlContent%(dev,dev)
		connectedHTML.append(dev)
		# print("%d. %s"%(n+1,str(dev)))
	return htmlresponse

@app.route('/setValue')
def setValue():
	global weightValue
	weightValue = request.args.get('value')
	return (str(isConnected))

def readValue(data):
	global startGetValue,s,weightValue,printWeight

	while(startGetValue):
		bs = s.readline()
		bs = bs.decode("utf-8").strip()
		print("received->",bs)

		if bs.find("CREATE")>-1:
			scheduleNo = ""
			try:
				scheduleNo = bs[7:]
			except Exception as e:
				print("Not Valid Schedule",e)

			if scheduleNo == "":
				response = "SCHEDULE_NO_ERROR" + "\r\n"			
			else:
				response = f"SCHEDULE_01_{scheduleNo}_CREATED" + "\r\n"
			s.write(response.encode('utf-8'))

		elif bs.find("LIST")>-1:
			response = """S01:004502\nS02:004503\nS03:004504\nS04:004505\nS05:004506\nS06:004507\nS07:004508\nS08:004509\nS09:004510\nS10:004511\n"""
			s.write(response.encode('utf-8'))

		elif bs.find("READ")>-1:
			response =   """S01 : C01 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C02 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C03 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C04 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C05 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C06 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C07 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C08 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C09 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C10 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C11 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C12 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C13 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C14 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C15 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C16 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C17 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C18 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C19 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C20 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C21 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C22 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C23 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C24 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C25 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C26 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C27 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C28 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C29 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C30 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C31 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C32 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C33 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C34 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C35 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C36 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C37 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C38 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C39 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C40 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C41 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C42 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C43 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C44 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C45 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C46 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C47 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C48 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C49 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00
S01 : C50 : EMP : 000000 : BC : 01 : LOA : 000000 : HC : 00\n"""
			s.write(response.encode('utf-8'))

		elif bs.find("CLEAR") > -1:
			response = "WAIT.."
			s.write(response.encode("utf-8"))
			time.sleep(2)
			response = "CLEARED"
			s.write(response.encode("utf-8"))
			time.sleep(2)

		elif bs.find("CLEARMEM") > -1:
			response = "WAIT.."
			s.write(response.encode("utf-8"))
			time.sleep(2)
			response = "CLEARED"
			s.write(response.encode("utf-8"))
			time.sleep(2)

		elif bs.find("SE") > -1:
			response = "EMPTY_WEIGHT_STORED"
			s.write(response.encode("utf-8"))

		elif bs.find("SL") > -1:
			response = "LOAD_WEIGHT_STORED"
			s.write(response.encode("utf-8"))
			
		elif bs.find("GETWEI") > -1:
			fmt = lambda x : "%05d" % x + str(x%1)[1:5]
			val = fmt(round(float(weightValue),3))
			val = val + '\r\n'
			s.write(val.encode("utf-8"))
			time.sleep(.5)

		elif bs.find("W.POLL=1") > -1:
			printWeight = True

		elif bs.find("W.POLL=0") > -1:
			printWeight = False

def getvalue(i):
	global startGetValue,s,weightValue, printWeight
	startGetValue = True
	printWeight = True
	while(startGetValue):
		# if float(weightValue) <= 0.0:
		# 	val = "00000.0\r\n"
		# else:
		# 	val = "%.3f\r\n" % (float(weightValue),)

		# fmt = lambda x : "%05d" % x + str(x%1)[1:5]
		# val = fmt(round(float(weightValue),3))
		# val = val + '\r\n'
		
		# val = "0"+str(float(weightValue))+"\r\n"
		# print(val)
		if printWeight:
			fmt = lambda x : "%05d" % x + str(x%1)[1:5]
			val = fmt(round(float(weightValue),3))
			val = val + '\r\n'
			s.write(val.encode("utf-8"))
		time.sleep(.5)

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=82,debug=True)