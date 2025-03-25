from typing import List

from fastapi import WebSocket

# Store connected WebSocket clients
connected_clients: List[WebSocket] = []


async def websocket_endpoint(websocket: WebSocket):
    """Handles new WebSocket connection."""
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Here you can process incoming messages
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_clients.remove(websocket)
        await websocket.close()


async def broadcast(message: str):
    """Send a message to all connected WebSocket clients."""
    for connection in connected_clients:
        await connection.send_text(message)
