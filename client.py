import socket
import threading
from colorama import Fore, Style, init
import sys

# Initialize colorama for colored console output
init(autoreset=True)

host = "0.0.0.0"
port = 4678

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Function to join a chat room
def join_chat_room():
    global chat_room
    chat_room = choose_chat_room()
    client.send(chat_room.encode('ascii'))

# Function to choose a chat room
def choose_chat_room():
    return input(f"{Fore.BLUE}Choose a chat room: {Style.RESET_ALL}")

# Function to choose a nickname
def choose_nickname():
    return input(f"{Fore.BLUE}Choose a nickname: {Style.RESET_ALL}")

# Function to receive and print messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print(f"{Fore.RED}Person left from the server.{Style.RESET_ALL}")
            break

# Function to send messages to the server
def write():
    while True:
        message = input()
        print(f"{Fore.BLUE}{' ' * 40}{nickname}: {message}{Style.RESET_ALL}")

        if message.lower() == "/quit":
            client.send(message.encode('utf-8'))
            client.close()
            break
        elif message.lower().startswith("/nickname"):
            new_nickname = message.split(" ", 1)[1]
            client.send(f"/nickname {new_nickname}".encode('utf-8'))
            update_nickname(new_nickname)  # Update nickname locally
        elif message.lower() == "/out":
            handle_out_command()
        else:
            client.send(message.encode('utf-8'))

# Function to handle the /out command
def handle_out_command():
    client.send("/out".encode('utf-8'))
    print(f"{Fore.YELLOW}You left the chat room.{Style.RESET_ALL}")

    # After leaving, choose a new chat room to join
    global chat_room
    chat_room = choose_chat_room()
    client.send(chat_room.encode('ascii'))

    # Choose a new nickname
    global nickname
    nickname = choose_nickname()
    client.send(nickname.encode('ascii'))
    
    # Join the new chat room
    join_chat_room()


# Function to update the local nickname
def update_nickname(new_nickname):
    global nickname
    nickname = new_nickname
    print(f"{Fore.YELLOW}Your nickname has been updated to {new_nickname}.{Style.RESET_ALL}")

# Start two threads for receiving and writing messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Initial setup: choose a chat room and a nickname
join_chat_room()
nickname = choose_nickname()
client.send(nickname.encode('ascii'))

write_thread = threading.Thread(target=write)
write_thread.start()

# Wait for both threads to finish before exiting
write_thread.join()
receive_thread.join()

# Close the client socket
client.close()
sys.exit(0)
