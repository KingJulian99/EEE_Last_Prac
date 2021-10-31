from flask import Flask, render_template
import threading
import socket

app = Flask(__name__)

rows = [('10:45:50','23.3C', '12.04'), ('10:46:0','23.3C', '12.01'), ('10:46:10','23.2C', '12.00')] # Holds sensor data, each item is a row tuple. 

def thread_function(IP, PORT):
    print("We are threading baby")
    BUFFER_SIZE = 512

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(1)

    while(True):
        client_socket, client_address = s.accept()
        print ('Connection established with: ', client_address)
        
        client_socket.send(bytes("Aweeeeee Sebbie!", "utf-8"))

# TCP METHODS
def acquire_status_TCP(): #TODO
    return True

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
    # send TCP signal instructing client to turn off
    return render_template('on.html')

@app.route('/off', endpoint='off')
def turn_off():
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

@app.route('/log_download', endpoint='download')
def download():
    # Download csv file!
    return render_template('index.html')

if __name__ == '__main__':
    IP = '196.24.166.233'
    PORT = 5005
    #ear = threading.Thread(target=thread_function, args=(IP, PORT), daemon=True)
    #ear.start()
    #app.run(host='0.0.0.0', port=80)
    app.run()
