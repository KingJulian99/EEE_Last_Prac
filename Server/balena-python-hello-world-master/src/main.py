from flask import Flask, render_template
import threading
import socket

app = Flask(__name__)

def thread_function(IP, PORT):
    print("We are threading baby")
    BUFFER_SIZE = 20
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))

    while(True):
        s.listen(1)
        conn, addr = s.accept()
        print ('Connection address:', addr)
        
        data = conn.recv(BUFFER_SIZE)
        if data:
            print ("received data:", data)
            conn.send()

        conn.close()



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/on')
def turn_on():
    # send TCP signal instructing client to turn off
    return render_template('on.html')

@app.route('/off')
def turn_off():
    # send TCP signal instructing client to turn off
    return render_template('off.html')

if __name__ == '__main__':
    IP = '196.24.166.233'
    PORT = 5005
    ear = threading.Thread(target=thread_function, args=(IP, PORT), daemon=True)
    ear.start()
    app.run(host='0.0.0.0', port=80)
