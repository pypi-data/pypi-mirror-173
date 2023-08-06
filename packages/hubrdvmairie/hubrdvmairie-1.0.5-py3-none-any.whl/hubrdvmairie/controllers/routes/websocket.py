import json
import logging
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ...controllers.routes.time_slots import search_slots

logging.getLogger("uvicorn.error").setLevel(logging.ERROR)

router = APIRouter()


@router.websocket("/SlotsFromPositionStreaming")
async def slots_from_position_streaming(websocket: WebSocket):
    _logger = logging.getLogger("root")
    try:
        await websocket.accept()
        while True:
            raw_data = await websocket.receive_text()
            start_time = datetime.now()
            data = json.loads(raw_data)
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])
            start_date = None
            try:
                if "start_date" in data:
                    start_date = datetime.strptime(
                        data["start_date"], "%Y-%m-%d"
                    ).date()
            except ValueError:
                pass
            end_date = None
            try:
                if "end_date" in data:
                    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            except ValueError:
                pass
            radius_km = int(data["radius_km"])

            await search_slots(
                longitude,
                latitude,
                start_date,
                end_date,
                radius_km,
                websocket=websocket,
            )

            await websocket.send_text("end_of_search")
            _logger.info(
                "End of websocket search",
                extra={
                    "extra_info": {
                        "type": "access",
                        "searchCriteria": data,
                        "searchLocation": {"lat": latitude, "lon": longitude},
                        "response_time": (datetime.now() - start_time).microseconds
                        / 1000,
                        "protocol": "websocket",
                        "realip": websocket.client.host,
                    }
                },
            )
    except WebSocketDisconnect:
        _logger.debug("Client disconnected.")
    except Exception as websocket_e:
        _logger.error("Error during websocket connexion : %s", websocket_e)
