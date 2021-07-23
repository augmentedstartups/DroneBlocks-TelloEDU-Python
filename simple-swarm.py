# This example script demonstrates how to use Python to fly Tello in a box mission
# This script is part of our course on Tello drone programming
# https://learn.droneblocks.io/p/tello-drone-programming-with-python/

# Import the necessary modules
import socket
import threading
import time

# IP and port of Tello
NumberOfDrones = [0,1,2,3,4]
tello_address = [('192.168.242.144', 8889), ('192.168.242.162', 8889), ('192.168.242.162', 8889), ('192.168.242.247', 8889),('192.168.242.25', 8889),('192.168.242.24', 8889)]
local_address = [('', 9010),('', 9011),('', 9012),('', 9013),('', 9014)] # IP and port of local computer
sock = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM),socket.socket(socket.AF_INET, socket.SOCK_DGRAM),socket.socket(socket.AF_INET, socket.SOCK_DGRAM),socket.socket(socket.AF_INET, socket.SOCK_DGRAM),socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]# Create a UDP connection that we'll send the command to

# Bind to the local address and port
for i in NumberOfDrones:
  sock[i].bind(local_address[i])

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
  # Try to send the message otherwise print the exception
  try:
    for i in NumberOfDrones:
      sock[i].sendto(message.encode(), tello_address[i])
      print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  time.sleep(delay)

# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response1, ip_address = sock[0].recvfrom(128)
      response2, ip_address = sock[1].recvfrom(128)
      response3, ip_address = sock[2].recvfrom(128)
      response4, ip_address = sock[3].recvfrom(128)
      response5, ip_address = sock[4].recvfrom(128)
      print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8'))
      print("Received message: from Tello EDU #2: " + response2.decode(encoding='utf-8'))
      print("Received message: from Tello EDU #3: " + response3.decode(encoding='utf-8'))
      print("Received message: from Tello EDU #4: " + response4.decode(encoding='utf-8'))
      print("Received message: from Tello EDU #5: " + response5.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      for i in NumberOfDrones:
        sock[i].close()
        print("Error receiving: " + str(e))
        break
# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Each leg of the box will be 100 cm. Tello uses cm units by default.
box_leg_distance = 100

# Yaw 90 degrees
yaw_angle = 90

# Yaw clockwise (right)
yaw_direction = "cw"

# Put Tello into command mode
send("command", 5)
send("battery?", 5)

# Send the takeoff command
send("takeoff", 8)

# # Loop and create each leg of the box
# for i in range(4):
#   # Fly forward
#   send("forward " + str(box_leg_distance), 4)
#   # Yaw right
#   send("cw " + str(yaw_angle), 3)

# Land
send("land", 2)

# Print message
print("Mission completed successfully!")

# Close the socket
for i in NumberOfDrones:
  sock[i].close()