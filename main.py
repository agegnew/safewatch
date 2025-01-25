from fastapi import FastAPI
from API.live_feed import get_live_feed  # Import the live feed logic from livefeed.py

app = FastAPI()

# 1. Live CCTV Feed - Delegate to livefeed.py
@app.get("/api/live-feed")
async def live_feed(camera: int = 1):  # Optional query parameter for camera selection
    return await get_live_feed(camera=camera)

# 2. Stored Videos
@app.get("/api/stored-videos")
async def get_stored_videos():
    return {
        "success": True,
        "videos": [
            {
                "id": "123",
                "title": "Test Video 1",
                "url": "http://camera-server-ip:port/videos/test1.mp4",
                "timestamp": "2025-01-24T15:30:00Z"
            },
            {
                "id": "124",
                "title": "Test Video 2",
                "url": "http://camera-server-ip:port/videos/test2.mp4",
                "timestamp": "2025-01-24T16:00:00Z"
            }
        ]
    }

# 3. Active Emergencies
@app.get("/api/emergencies/active")
async def get_active_emergencies():
    return {
        "success": True,
        "emergencies": [
            {
                "id": "e1",
                "description": "Fire detected in Warehouse A",
                "location": "Warehouse A",
                "timestamp": "2025-01-24T14:45:00Z",
                "status": "active"
            },
            {
                "id": "e2",
                "description": "Unauthorized entry at Gate B",
                "location": "Gate B",
                "timestamp": "2025-01-24T15:00:00Z",
                "status": "active"
            }
        ]
    }

# 4. Close Emergency
@app.post("/api/emergencies/close")
async def close_emergency(emergency_id: str):
    return {
        "success": True,
        "message": f"Emergency {emergency_id} closed successfully"
    }

# 5. Closed Emergencies
@app.get("/api/emergencies/closed")
async def get_closed_emergencies():
    return {
        "success": True,
        "emergencies": [
            {
                "id": "e1",
                "description": "Fire detected in Warehouse A",
                "location": "Warehouse A",
                "timestamp": "2025-01-24T14:45:00Z",
                "closed_at": "2025-01-24T15:15:00Z",
                "status": "closed"
            }
        ]
    }

# 6. System Status
@app.get("/api/system/status")
async def get_system_status():
    return {
        "success": True,
        "cameras_online": 8,
        "cameras_offline": 2,
        "total_cameras": 10,
        "last_updated": "2025-01-24T16:30:00Z"
    }

# 7. Notifications
@app.get("/api/notifications")
async def get_notifications():
    return {
        "success": True,
        "notifications": [
            {
                "id": "n1",
                "message": "New emergency: Fire detected in Warehouse A",
                "timestamp": "2025-01-24T14:45:00Z"
            },
            {
                "id": "n2",
                "message": "System update: All cameras are online",
                "timestamp": "2025-01-24T15:30:00Z"
            }
        ]
    }
