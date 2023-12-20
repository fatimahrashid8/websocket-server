# WebSocket Server

## Description

This WebSocket server facilitates real-time communication for applications, such as multiplayer games or chat systems. It supports creating rooms, joining rooms, broadcasting messages within rooms, and leaving rooms.

## WebSocket Server Testing Guide Using Postman

This guide provides step-by-step instructions for manually testing the WebSocket server's features using Postman.

### Prerequisites

- Ensure you have Postman installed on your system.
- The WebSocket server should be running and accessible.

### Steps to Connect to the WebSocket Server

1. **Open Postman**: Launch Postman and select the "New" button.
2. **Create WebSocket Request**: Choose "WebSocket Request" from the options.
3. **Enter Server URL**: In the request URL field, type in your WebSocket server URL (e.g., `ws://localhost:1234`).
4. **Connect**: Click "Connect" to establish a WebSocket connection.

### Testing Different Actions

#### 1. Create Room
- **Action**: Request to create a new room.
- **Sample JSON Message**:
  ```json
  { "action": "create_room", "capacity": 2 }
- **Expected Response**:
  ```json
  { "action": "room_created", "room_id": "unique_room_id" }

### 2. Join Room

- **Action**: Request to join an existing room.
- **Sample JSON Message**:
  ```json
  { "action": "join_room", "room_id": "unique_room_id" }
- **Expected Response**:
  ```json
  { "action": "joined_room", "room_id": "unique_room_id" }

### 3. Broadcast Message

- **Action**: Send a message to all members in the room.
- **Sample JSON Message**:
  ```json
  { "action": "broadcast", "room_id": "unique_room_id", "message": "Hello everyone" }

### 4. Leave Room

- **Action**: Request to leave the room.
- **Sample JSON Message**:
  ```json
  { "action": "leave_room", "room_id": "unique_room_id" }
- **Expected Response**:
  ```json
  { "action": "left_room", "room_id": "unique_room_id" }

### Notes
- Replace unique_room_id with the actual room ID received from the server.
