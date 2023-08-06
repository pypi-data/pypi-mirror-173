import asyncio
import json
import logging
import os
import random
from datetime import date, datetime, timedelta

import requests
import requests_async
from fastapi import WebSocket
from pydantic import ValidationError
from ..logging.app_logger import write_external_service_data
from .municipality import Municipality
from ..services.mock_data import get_mock_managed_meeting_points, get_mock_slots


class Editor:
    slug: str
    name: str
    api_url: str
    _test_mode: bool

    def __init__(self, slug: str, name: str, api_url: str, test_mode: bool):
        self.slug = slug
        self.name = name
        self.api_url = api_url
        self._test_mode = test_mode

    def get_managed_meeting_points(self):
        _logger = logging.getLogger("root")
        points = []
        if self._test_mode:
            points = get_mock_managed_meeting_points(self)
        else:
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                response = requests.get(
                    f"{self.api_url}/getManagedMeetingPoints",
                    headers=headers,
                    timeout=20,
                )
                write_external_service_data(_logger, response)
                if response.status_code in [200]:
                    points = response.json()
                else:
                    raise Exception(f"Status code not handled : {response.status_code}")
            except Exception as get_meeting_points_e:
                _logger.error(
                    "Error while getting meeting points for %s : %s",
                    self.name,
                    str(get_meeting_points_e),
                )

        valid_meeting_points = []
        for point in points:
            point["_editor_name"] = self.name
            point["_internal_id"] = str(point["id"])
            try:
                Municipality.parse_obj(point)
                valid_meeting_points.append(point)
            except ValidationError as meeting_point_validation_e:
                _logger.error(
                    "Error while validating meeting point : %s \nError: %s",
                    point,
                    meeting_point_validation_e,
                )

        return valid_meeting_points

    async def get_available_time_slots(self, meeting_points, start_date, end_date):
        _logger = logging.getLogger("root")
        result = {}
        if self._test_mode:
            await asyncio.sleep(random.randint(3, 12))
            for meeting_point in meeting_points:
                meeting_point_slots = get_mock_slots(
                    meeting_point, start_date, end_date
                )
                result[meeting_point["_internal_id"]] = meeting_point_slots
        else:
            # this sleep is necessary to not block other async operations
            await asyncio.sleep(0.0000001)
            meeting_point_ids = [x["_internal_id"] for x in meeting_points]
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                parameters = {
                    "start_date": start_date or date.today(),
                    "end_date": end_date or (date.today() + timedelta(days=150)),
                    "meeting_point_ids": meeting_point_ids,
                }
                response = await requests_async.get(
                    f"{self.api_url}/availableTimeSlots",
                    headers=headers,
                    params=parameters,
                    timeout=15,
                    verify=False,
                )
                write_external_service_data(_logger, response)
                if response.status_code in [200]:
                    result = response.json()
                else:
                    raise Exception(
                        f"Status code not handled : {response.status_code} : {response.reason}"
                    )
            except Exception as get_meeting_points_e:
                _logger.error(
                    "Error while getting available time slots for %s : %s",
                    self.name,
                    str(get_meeting_points_e),
                )

        if (not start_date) and (not end_date):
            return result

        filtered_dates_result = {}
        try:
            for meeting_point_id in result:
                filtered_dates_result[meeting_point_id] = []
                for available_timeslot in result[meeting_point_id]:
                    timeslot_datetime = None
                    for datetime_format in ["%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%S%z"]:
                        try:
                            timeslot_datetime = datetime.strptime(
                                available_timeslot["datetime"], datetime_format
                            ).date()
                            break
                        except ValueError:
                            pass
                    if (
                        (not timeslot_datetime)
                        or (start_date and (timeslot_datetime < start_date))
                        or (end_date and (timeslot_datetime > end_date))
                    ):
                        _logger.debug(
                            "[%s] DATE OUT OF RANGE : %s",
                            self.name,
                            str(timeslot_datetime),
                        )
                    else:
                        filtered_dates_result[meeting_point_id].append(
                            available_timeslot
                        )
        except Exception as checking_date_filter_e:
            _logger.error(
                "[%s] Checking date filter error : %s",
                self.name,
                str(checking_date_filter_e),
            )
            return {}
        return filtered_dates_result

    async def search_slots_in_editor(
        self, meeting_points, start_date, end_date, websocket: WebSocket = None
    ):
        editor_meeting_points = []
        editor_meeting_points_with_slots = []
        for meeting_point in meeting_points:
            if meeting_point["_editor_name"] == self.name:
                editor_meeting_points.append(meeting_point)
        if editor_meeting_points:
            slots = await self.get_available_time_slots(
                editor_meeting_points, start_date, end_date
            )
            for meeting_point in editor_meeting_points:
                if (
                    meeting_point["_internal_id"] in slots
                    and slots[meeting_point["_internal_id"]]
                ):
                    meeting_point["available_slots"] = slots[
                        meeting_point["_internal_id"]
                    ]
                    editor_meeting_points_with_slots.append(meeting_point)
            if websocket:
                json_string = json.dumps(editor_meeting_points_with_slots, default=str)
                await websocket.send_text(json_string)
        return editor_meeting_points_with_slots

    async def search_meetings(self, application_ids):
        _logger = logging.getLogger("root")
        await asyncio.sleep(0.00001)
        meetings = {}
        if not self._test_mode:
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                parameters = {"application_ids": application_ids}
                response = await requests_async.get(
                    f"{self.api_url}/searchApplicationIds",
                    headers=headers,
                    params=parameters,
                    timeout=5,
                    verify=False,
                )
                write_external_service_data(_logger, response)
                if response.status_code in [200]:
                    meetings = response.json()
                else:
                    raise Exception(f"Status code not handled : {response.status_code}")
            except Exception as search_meetings_e:
                _logger.error(
                    "Error while seachring meetings by application ID for %s : %s",
                    self.name,
                    str(search_meetings_e),
                )
        else:
            await asyncio.sleep(random.randint(3, 5))
        return meetings


def init_all_editors():
    citopia_editor = Editor(
        "citopia", "Citopia", "https://pro.rendezvousonline.fr/api", False
    )
    synbird_editor = Editor(
        "synbird", "Synbird", "https://sync.synbird.com/ants", False
    )
    esii_editor = Editor(
        "esii", "ESII", "https://api.esii-orion.com/ants/api/public/1/ants", False
    )
    troov_editor = Editor("troov", "Troov", "https://qa-api.troov.com/api", False)
    rdv_360_editor = Editor("rdv360", "RDV360", "http://ants.rdv360.com/api", False)
    mega_editor = Editor("mega", "Mega", "https://www.mega.com", True)
    orionRDV_editor = Editor("orionRDV", "OrionRDV", "https://orionrdv.com/", True)
    if os.environ.get("MOCK_EDITORS") in ["True", True]:
        return [citopia_editor, mega_editor, orionRDV_editor, synbird_editor]
    else:
        return [
            citopia_editor,
            synbird_editor,
            esii_editor,
            troov_editor,
            rdv_360_editor,
        ]
