from fastapi import APIRouter

router = APIRouter()

# Stored Videos API
@router.get("/api/stored-videos")
async def get_stored_videos():
    # Placeholder for stored videos data
    # Replace with dynamic logic to fetch local video files
    videos = [
        {
            "id": "123",
            "title": "Test Video 1",
            "url": "file:///path/to/videos/test1.mp4",  # Update with actual local path
            "timestamp": "2025-01-24T15:30:00Z"
        },
        {
            "id": "124",
            "title": "Test Video 2",
            "url": "file:///path/to/videos/test2.mp4",  # Update with actual local path
            "timestamp": "2025-01-24T16:00:00Z"
        }
    ]
    return {
        "success": True,
        "videos": videos
    }
