import socket
import threading
from colorama import Fore, Style, init

# Initialize colorama for colored console output
init(autoreset=True)

# Server configuration
host = "0.0.0.0"
port = 4678

# Server socket setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Dictionary to store clients and nicknames for each chat room
chat_rooms = {'default': {'clients': [], 'nicknames': []}}

# Function to send colored messages to all clients in a specific chat room
def broadcast(message, sender_client=None, chat_room='default'):
    sender_index = chat_rooms[chat_room]['clients'].index(sender_client) if sender_client in chat_rooms[chat_room]['clients'] else -1
    sender_nickname = chat_rooms[chat_room]['nicknames'][sender_index] if sender_index != -1 else "Server"

    formatted_message = f"{Fore.BLUE}[{chat_room}] {sender_nickname}: {Style.RESET_ALL}{message.decode('utf-8')}"

    for client in chat_rooms[chat_room]['clients']:
        if client != sender_client:
            try:
                client.send(formatted_message.encode('utf-8'))
            except socket.error as e:
                if e.errno == socket.errno.EPIPE:  # BrokenPipeError
                    handle_disconnection(client, chat_room)

# Function to handle client disconnection from a specific chat room
def handle_disconnection(disconnected_client, chat_room='default'):
    index = chat_rooms[chat_room]['clients'].index(disconnected_client)
    if index < len(chat_rooms[chat_room]['nicknames']):
        nickname = chat_rooms[chat_room]['nicknames'][index]
        chat_rooms[chat_room]['clients'].remove(disconnected_client)
        disconnected_client.close()

        # Send the updated list of nicknames to the remaining clients in the same chat room
        send_updated_nicknames(chat_room)

        # Print who left the chat
        print(f'{Fore.RED}[{chat_room}] {nickname} left the chat!{Style.RESET_ALL}')

        # Broadcast the departure message to all clients in the same chat room
        broadcast(f'{Fore.RED}[{chat_room}] {nickname} left the chat!{Style.RESET_ALL}\n'.encode("utf-8"), chat_room=chat_room)

        chat_rooms[chat_room]['nicknames'].remove(nickname)

# Function to send the updated list of nicknames to all clients in a specific chat room
def send_updated_nicknames(chat_room='default'):
    nicknames_message = f"{Fore.YELLOW}[{chat_room}] Connected clients: {', '.join(chat_rooms[chat_room]['nicknames'])}{Style.RESET_ALL}\n"
    for client in chat_rooms[chat_room]['clients']:
        try:
            client.send(nicknames_message.encode('utf-8'))
        except socket.error as e:
            if e.errno == socket.errno.EPIPE:  # BrokenPipeError
                handle_disconnection(client, chat_room)

# Function to broadcast the nickname change to all clients in a specific chat room
def broadcast_nickname_change(old_nickname, new_nickname, chat_room='default'):
    message = f'{Fore.YELLOW}[{chat_room}] {old_nickname} changed their nickname to {new_nickname}.{Style.RESET_ALL}\n'
    broadcast(message.encode('utf-8'), chat_room=chat_room)

# Function to change the nickname
def change_nickname(client, new_nickname, chat_room='default'):
    old_index = chat_rooms[chat_room]['clients'].index(client)
    old_nickname = chat_rooms[chat_room]['nicknames'][old_index]

    # Check if the new nickname is already in use
    if new_nickname in chat_rooms[chat_room]['nicknames']:
        client.send(f"{Fore.RED}Error: Nickname '{new_nickname}' is already in use.{Style.RESET_ALL}\n".encode('utf-8'))
    else:
        # Change the nickname
        chat_rooms[chat_room]['nicknames'][old_index] = new_nickname

        # Send a confirmation message to the client
        client.send(f"{Fore.YELLOW}Nickname changed to {new_nickname}.{Style.RESET_ALL}\n".encode('utf-8'))

        # Broadcast the nickname change to all clients in the same chat room
        broadcast_nickname_change(old_nickname, new_nickname, chat_room)

        # Send the updated list of nicknames to all clients in the same chat room
        send_updated_nicknames(chat_room)

# Function to handle the /out command
def handle_out_command(client, chat_room='default'):
    index = chat_rooms[chat_room]['clients'].index(client)
    if index < len(chat_rooms[chat_room]['nicknames']):
        nickname = chat_rooms[chat_room]['nicknames'][index]

        # Remove the client from the current chat room
        chat_rooms[chat_room]['clients'].remove(client)
        chat_rooms[chat_room]['nicknames'].remove(nickname)

        # Send the updated list of nicknames to the remaining clients in the same chat room
        send_updated_nicknames(chat_room)

        # Print who left the chat
        print(f'{Fore.RED}[{chat_room}] {nickname} left the chat!{Style.RESET_ALL}')

        # Broadcast the departure message to all clients in the same chat room
        broadcast(f'{Fore.RED}[{chat_room}] {nickname} left the chat!{Style.RESET_ALL}\n'.encode("utf-8"), chat_room=chat_room)

        # Prompt the client for a new chat room and nickname
        new_chat_room = client.recv(1024).decode('ascii')
        new_nickname = client.recv(1024).decode('ascii')

        # Create the new chat room if it doesn't exist
        if new_chat_room not in chat_rooms:
            chat_rooms[new_chat_room] = {'clients': [], 'nicknames': []}

        # Add the client to the new chat room
        chat_rooms[new_chat_room]['nicknames'].append(new_nickname)
        chat_rooms[new_chat_room]['clients'].append(client)

        print(f'{Fore.GREEN}[{new_chat_room}] {new_nickname} joined the chat!{Style.RESET_ALL}')
        broadcast(f'{Fore.GREEN}[{new_chat_room}] {new_nickname} joined the chat!{Style.RESET_ALL}\n'.encode('utf-8'), sender_client=client, chat_room=new_chat_room)
        client.send("Connected to the server!\n".encode('ascii'))

        # Send the list of nicknames to the new client in the same chat room
        send_updated_nicknames(new_chat_room)

        # Start a new thread to handle the client's messages
        thread = threading.Thread(target=handle, args=(client, new_chat_room))
        thread.start()



# Function to handle client messages in a specific chat room
# Function to handle client messages in a specific chat room
def handle(client, chat_room='default'):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break

            decoded_message = message.decode('utf-8')

            # Check if it's a command to quit
            if decoded_message.lower() == "/quit":
                handle_disconnection(client, chat_room)
                break
            elif decoded_message.lower().startswith("/nickname"):
                new_nickname = decoded_message.split(" ", 1)[1].strip()
                change_nickname(client, new_nickname, chat_room)
            elif decoded_message.lower() == "/out":
                handle_out_command(client, chat_room)
                break
            else:
                broadcast(message, sender_client=client, chat_room=chat_room)
        except socket.error as e:
            if e.errno == socket.errno.EPIPE:  # BrokenPipeError
                handle_disconnection(client, chat_room)
            break



# Function to accept new clients and handle their connections in a specific chat room
def receive():
    while True:
        client, address = server.accept()
        print(f'{Fore.GREEN}Connected with {str(address)}{Style.RESET_ALL}')
        
        # Prompt the client for a chat room and nickname
        chat_room = client.recv(1024).decode('ascii')
        nickname = client.recv(1024).decode('ascii')

        if chat_room not in chat_rooms:
            chat_rooms[chat_room] = {'clients': [], 'nicknames': []}

        chat_rooms[chat_room]['nicknames'].append(nickname)
        chat_rooms[chat_room]['clients'].append(client)

        print(f'{Fore.GREEN}[{chat_room}] {nickname} joined the chat!{Style.RESET_ALL}')
        broadcast(f'{Fore.GREEN}[{chat_room}] {nickname} joined the chat!{Style.RESET_ALL}\n'.encode('utf-8'), sender_client=client, chat_room=chat_room)
        client.send("Connected to the server!\n".encode('ascii'))

        # Send the list of nicknames to the new client in the same chat room
        send_updated_nicknames(chat_room)

        # Start a new thread to handle the client's messages
        thread = threading.Thread(target=handle, args=(client, chat_room))
        thread.start()

# Start the server
print(f"{Fore.CYAN}Server is listening...{Style.RESET_ALL}")
receive()
