from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter()

@router.get("/reverse")
async def reverse_geocode(lat: float = Query(...), lon: float = Query(...)):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&email=your-email@example.com"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raises an HTTPError if the status is 4xx/5xx
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Geocoding service unavailable: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Geocoding failed: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
