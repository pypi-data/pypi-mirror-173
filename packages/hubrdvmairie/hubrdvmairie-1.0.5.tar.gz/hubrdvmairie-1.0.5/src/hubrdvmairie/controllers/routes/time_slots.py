from datetime import date
from typing import Any, List

from fastapi import APIRouter, Query
from pydantic import Required
from ...models.municipality import MunicipalityWithSlots
from ...services.search_time_slots import search_slots

router = APIRouter()


@router.get(
    "/SlotsFromPosition",
    response_model=List[MunicipalityWithSlots],
    responses={
        200: {
            "description": "Slots successfully found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "1213",
                            "name": "Mairie ANNEXE LILLE-SECLIN",
                            "longitude": 3.0348016639327,
                            "latitude": 50.549140395451,
                            "public_entry_address": "89 RUE ROGER BOUVRY 59113 SECLIN",
                            "zip_code": "59113",
                            "city_name": "SECLIN",
                            "website": "http://www.ville-seclin.fr",
                            "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                            "available_slots": [
                                {
                                    "datetime": "2022-12-19T10:00Z",
                                    "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:00Z",
                                },
                                {
                                    "datetime": "2022-12-19T10:20Z",
                                    "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:20Z",
                                },
                                {
                                    "datetime": "2022-12-19T10:40Z",
                                    "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:40Z",
                                },
                                {
                                    "datetime": "2022-12-19T11:00Z",
                                    "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T11:00Z",
                                },
                            ],
                        },
                        {
                            "id": "456456",
                            "name": "Mairie de Quartier de Lille-Sud",
                            "longitude": 3.0475818403133,
                            "latitude": 50.612875943839,
                            "public_entry_address": "83 Rue du Faubourg des Postes",
                            "zip_code": "59000",
                            "city_name": "LILLE-SECLIN",
                            "website": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud",
                            "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                            "available_slots": [
                                {
                                    "datetime": "2022-12-19T10:00Z",
                                    "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:00Z",
                                },
                                {
                                    "datetime": "2022-12-19T10:20Z",
                                    "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:20Z",
                                },
                                {
                                    "datetime": "2022-12-19T10:40Z",
                                    "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:40Z",
                                },
                                {
                                    "datetime": "2022-12-19T11:00Z",
                                    "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T11:00Z",
                                },
                            ],
                        },
                    ]
                }
            },
        }
    },
)
async def slots_from_position(
    longitude: float = Query(default=Required, example=2.352222),
    latitude: float = Query(default=Required, example=48.856613),
    start_date: date = Query(default=Required, example="2022-11-01"),
    end_date: date = Query(default=Required, example="2022-11-30"),
    radius_km: int = Query(default=40, enum=[20, 40, 60]),
) -> Any:
    """
    Search Slots from position.
    """
    result = await search_slots(longitude, latitude, start_date, end_date, radius_km)

    return result
