from flask import Flask, render_template, send_file
import threading
import socket
import csv

app = Flask(__name__)

rows = [] # Holds sensor data, each item is a row tuple. Grabs from logs.csv
BUFFER_SIZE = 1024
ALIVE = True
DIRTY = False

def thread_function(IP, PORT):
    global BUFFER_SIZE, DIRTY

    print("Attempting to listen on port " + str(PORT) + " address " + IP)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(10)

    print('We are listening on ' + IP + ', port ' + str(PORT))
    client_socket, client_address = s.accept()
    print ('Connection established with: ', client_address)
    client_socket.send(bytes("You connected to the server", "utf-8"))

    while 1 :

        while(ALIVE):

            if(DIRTY == True):
                data =  client_socket.recv(BUFFER_SIZE)
                if not data: break
                print("received (dirty): " + data.decode())
                time, temp, bright = parse(data.decode())
                DIRTY = False
            else:
                data =  client_socket.recv(BUFFER_SIZE)
                if not data: break
                print("received: " + data.decode())

                time, temp, bright = parse(data.decode())

                rows.append(tuple((time, temp, bright)))
                addToCSV(time, temp, bright)

        
    client_socket.close()



def parse(data):
    firstHash = data.index('#')
    secondHash = data.index('#', data.index('#')+1)
    return data[:firstHash], data[firstHash + 1: secondHash], data[secondHash + 1:]


def addToCSV(time, temp, bright):
    with open('logs.csv','a') as fd:
        fd.write(time + ',' + temp + ',' + bright)


# TCP METHODS
def acquire_status_TCP(): 
    return ALIVE

def send_control_TCP(flag):
    if flag == 0:
        pass
    elif flag == 1:
        pass
    else:
        pass


# WEBSITE STRUCTURE
@app.route('/', endpoint='home')
def hello_world():
    return render_template('index.html')

@app.route('/on', endpoint='on')
def turn_on():
    global ALIVE 
    ALIVE = True
    # send TCP signal instructing client to turn off
    return render_template('on.html')

@app.route('/off', endpoint='off')
def turn_off():
    global ALIVE, DIRTY
    ALIVE = False
    DIRTY = True
    # send TCP signal instructing client to turn off
    return render_template('off.html')

@app.route('/status', endpoint='status')
def get_status():
    # Get the current status of the sensor circuit
    return render_template('status.html', status = acquire_status_TCP())

@app.route('/log_check', endpoint='log_check')
def log_check():
    # Render Logs in a table (updated on every reload)
    return render_template('logs.html', rows = rows)

@app.route('/download', endpoint='download')
def download():
    # Download csv file!
    return send_file('logs.csv', as_attachment=True)

@app.route('/exit', endpoint='exit')
def exxit():
    return render_template('exit.html')


def readCSV():
    global rows

    with open('logs.csv') as csv_f:
        csv_reader = csv.reader(csv_f, delimiter=',')

        for row in csv_reader:
            rows.append(tuple((row[0], row[1], row[2])))


if __name__ == '__main__':
    ear = threading.Thread(target=thread_function, args=('192.168.1.128', 5005), daemon=True)
    ear.start()

    readCSV()
    
    app.run(host='0.0.0.0', port=80, debug=False)
    #app.run(debug=True)
    #app.run()
