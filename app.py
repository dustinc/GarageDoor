
from flask import Flask
import time
import RPi.GPIO as io


io.setmode(io.BCM)
io.setwarnings(False)

DOOR = 4
SENSOR_A = 17 # OPEN DOOR POSITION
SENSOR_B = 27 # CLOSED DOOR POSITION

io.setup(DOOR, io.OUT)

io.setup(SENSOR_A, io.IN, pull_up_down=io.PUD_UP)
io.setup(SENSOR_B, io.IN, pull_up_down=io.PUD_UP)

io.output(DOOR, True)

DOOR_STATE = [
  'CLOSED',
  'TRANSIT',
  'OPEN'
]

# 0 closed, 1 in transit / partially open, 2 open
def getDoorState():
  door_state = 0
  if io.input(SENSOR_A) and not io.input(SENSOR_B):
    #print('Door is CLOSED')
    door_state = 0
  if not io.input(SENSOR_A) and io.input(SENSOR_B):
    #print('Door is OPEN')
    door_state = 2
  if io.input(SENSOR_A) and io.input(SENSOR_B):
    #print('Door in TRANSIT or is PARTIALLY OPEN')
    door_state = 1
  return door_state


# Setup web server

app = Flask(__name__)


@app.route('/')
def index():
  door_state = getDoorState()
  return 'Door status is %s'%(DOOR_STATE[door_state])

@app.route('/press')
def press():
  io.output(DOOR, False)
  time.sleep(0.5)
  io.output(DOOR, True)
  return 'Pressed'


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
