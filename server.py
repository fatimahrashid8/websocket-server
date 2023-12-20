import asyncio
import json
import websockets
import uuid

# Constants
DEFAULT_ROOM_CAPACITY = 2

# Global variables
connected = set()
rooms = {}  # Format: {'room_id': (set([websocket1, websocket2]), capacity)}


async def register(websocket):
    connected.add(websocket)


async def unregister(websocket):
    connected.remove(websocket)
    for room_id, (members, capacity) in rooms.items():
        if websocket in members:
            members.discard(websocket)
            leave_message = json.dumps({"action": "player_left", "room_id": room_id})
            await broadcast_message(room_id, leave_message)


async def room_management(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                error_message = json.dumps({"error": "Invalid JSON format"})
                await websocket.send(error_message)
                continue

            action = data.get('action')

            if action == 'create_room':
                room_capacity = data.get('capacity', DEFAULT_ROOM_CAPACITY)
                room_id = str(uuid.uuid4())
                while room_id in rooms:
                    room_id = str(uuid.uuid4())
                rooms[room_id] = (set([websocket]), room_capacity)
                await websocket.send(json.dumps({"action": "room_created", "room_id": room_id}))

            elif action == 'join_room':
                room_id = data.get('room_id')
                if room_id in rooms:
                    members, capacity = rooms[room_id]
                    if len(members) < capacity:
                        members.add(websocket)
                        await websocket.send(json.dumps({"action": "joined_room", "room_id": room_id}))
                        join_message = json.dumps({"action": "player_joined", "room_id": room_id})
                        await broadcast_message(room_id, join_message, exclude=websocket)
                    else:
                        await websocket.send(json.dumps({"action": "room_full", "room_id": room_id}))
                else:
                    await websocket.send(json.dumps({"action": "room_not_found", "room_id": room_id}))

            elif action == 'leave_room':
                room_id = data.get('room_id')
                if room_id in rooms:
                    members, _ = rooms[room_id]
                    members.discard(websocket)
                    await websocket.send(json.dumps({"action": "left_room", "room_id": room_id}))

            elif action == 'broadcast':
                room_id = data.get('room_id')
                broadcast_msg = data.get('message')
                await broadcast_message(room_id, broadcast_msg, exclude=websocket)

    finally:
        await unregister(websocket)


async def broadcast_message(room_id, message, exclude=None):
    if room_id in rooms:
        members, _ = rooms[room_id]
        tasks = [asyncio.create_task(ws.send(message)) for ws in members if ws != exclude]

        if tasks:
            await asyncio.wait(tasks)


async def main():
    async with websockets.serve(room_management, "localhost", 1234):
        await asyncio.Future()

asyncio.run(main())
