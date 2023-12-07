# TCPchat

Detailed Working/Analysis/Features/Design

Detailed Working
The server script (server.py) sets up a socket and binds it to the specified host and port to start the function. It then enters the incoming state while waiting for an incoming connection. To handle multiple clients simultaneously, servers can communicate simultaneously without blocking other clients by leveraging threading. Chat rooms facilitate chatroom management, and dictionaries dynamically create new chat rooms as clients join.

Commands are a fundamental aspect of server functionality. They recognize and interpret commands such as changing nicknames (/nicknames), leaving chat rooms (/out), and shutting down applications (/quit). They provide a comprehensive, user-friendly command interface by implementing features that can handle nickname changes, client disconnections, and switching chat rooms. The Colorama library is integrated to improve console output with color text to distinguish between chat rooms, nicknames, and system messages.

Analysis
The server's architecture is designed to scale effectively thanks to a multi-threaded model that can handle multiple clients simultaneously. The implementation of user-friendly commands improves the usability of applications, making it intuitive for users to interact with the chat system. The dynamic creation of chat rooms that provide flexibility and adaptability to the changing needs of users is a notable feature.

Features
The server boasts several key features that contribute to the feature. Message broadcasting ensures that a client's message is efficiently forwarded to all other clients within the same chat room. The option for clients to change their nicknames using the /nickname command adds a personalized touch to the user experience. The dynamic creation of chat rooms allows users to set up new rooms instantly, enhancing the flexibility of chat applications. The color output promoted by the Colorama library improves the visual appeal and readability of the console interface.

Design
The server design features a powerful multi-threading model that simultaneously handles tasks to stay responsive. It utilizes chatroom dictionaries to separate concerns and organize information about connected clients. Command-driven interactions with clients are easy to use, making servers user-friendly. It facilitates modularity and maintenance by configuring features that can handle specific tasks. Dynamic management of client sockets and chat rooms reflects adaptability to changing server environments.

Implementation Details/Methodology/Testing

Implementation Details
The Python code provided implements a simple client-server conversation application that features a server script (server.py ) and a client script (client.py ). Servers utilize sockets and multi-reads to facilitate simultaneous communication with multiple clients. By integrating the Colorram library, it improves console output with color text, providing a visually appealing user experience.

Server.py includes implementations such as initializing a server socket, handling incoming connections, and managing chat rooms through chat_rooms. Servers efficiently handle disconnecting clients, changing nicknames, and switching chat rooms to ensure a seamless user experience. The methodology involves simultaneously managing various tasks, such as broadcasting messages, interpreting commands, and handling errors with socket-related issues, using threading.

Client.py uses threads to establish a socket connection to the server to simultaneously manage the sending and receiving of client-side messages. The client script asks users to select a chat room and a nickname to participate in a continuous loop for input and message exchange. It also interprets certain commands, such as changing nicknames or leaving chat rooms, to show a user-friendly and intuitive interface.

Methodology
The client script (client.py) follows a structured approach to user interaction and command interpretation. Upon execution, the client initiates user interactions by urging the user to make important decisions, such as selecting a chat room and selecting a unique nickname. Afterwards, the client seamlessly transitions to a continuous loop, ensuring continuous message exchange with the server. This loop accommodates both sending user-input messages and receiving messages from other participants in a selected chat room.

The client script also presents a robust approach to command interpretation. It identifies specific commands, such as changing nicknames (/nicknames), leaving chat rooms (/out), and shutting down applications (/out), and actively monitors user input. Upon recognizing the command, the client immediately generates the appropriate message and sends it to the server for further processing. This makes it easy and simple for the user to participate in the chat application, which improves the overall usefulness and efficiency of the client script.

Testing
 Server scripts (server.py) require individual testing of functions responsible for key tasks such as message broadcasting, nickname changes, chat room management, and server ending. Similarly, client scripts (client.py ) must be thoroughly vetted for functionality that includes sending and receiving messages, interpreting commands, and elements of the user interface. Also it needs to ensure that the intended client in each chat room sends, receives, and displays messages correctly. It is also necessary to test the dynamic management of chat rooms and concurrent connections to ensure smooth operation. It requires checking continuous loops to send and receive messages to ensure a smooth, user-friendly experience. Most importantly, command testing is required to ensure that the client script correctly interprets commands such as changing nicknames (/nicknames), leaving chat rooms (/out), and shutting down applications (/quit). At the same time, you should test the server's response to these commands to ensure that expected actions are performed correctly.
