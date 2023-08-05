import requests as r
from urllib.parse import urlparse,parse_qs
from datetime import datetime, timedelta
from typing import List, Union

from .models import Measurement, Location, Device


class Facade:
    """Facade is a class which simplifies your interaction with the SensorBucket API."""
    def __init__(self, url: str, apiKey: str):
        """This class acts as a Facade for the SensorBucket API

        Parameters
        ----------
        url : str
            The base url for the SensorBucket API
        apiKey : str
            API Key used to authenticate with Sensorbucket
        """
        self.url = url
        self.apiKey = apiKey

    def get_locations(self) -> List[Location]:
        """Fetches all the available locations for the authenticated user

        Returns
        -------
        List[Location]
            The locations
        """
        res = r.get(f"{self.url}/api/v1/locations", headers={
            "authorization": f"bearer {self.apiKey}"
        })
        res.raise_for_status()
        return Location.schema().load(res.json()["data"], many=True)

    def get_devices(self) -> List[Device]:
        """Fetches all devices for the authenticated user

        Returns
        _______
        List[Device]
            The list of devices
        """
        res = r.get(f"{self.url}/api/v1/devices", headers={
            "authorization": f"bearer {self.apiKey}"
        })
        res.raise_for_status()
        return Device.schema().load(res.json()["data"], many=True)

    def get_measurements(self,start: Union[datetime, str], end: Union[datetime, str], measurement_type: str = None, location_id: int = None, sensor_code: str = None, limit: int = 100) -> List[Measurement]:
        """Fetches a list of measurements from a given location in a given time window

        Parameters
        ----------
        start : Union[datetime, str]
            The start time of the time window
        end : Union[datetime, str]
            The end time of the time windows
        measurement_type : str
            ID or name of the measurement type
        location_id : Optional[int]
            The location id of the measurements
        sensor_code : Optional[str]
            The sensor which performed the measurements

        Returns
        -------
        List[Measurement]
            A list of measurements

        Raises
        ------
        """

        # Start and End parameters can be datetime objects, but the API expects
        # ISO8601 strings, so convert them
        if type(start) == datetime:
            start = start.isoformat()
        if type(end) == datetime:
            end = end.isoformat()

        # Perform request to API
        query = {
            "location_id": location_id,
            "measurement_type": measurement_type,
            "start": start,
            "end": end,
            "limit": limit
        }

        while True:
            res = r.get(f"{self.url}/api/v1/measurements", params=query, headers={
                "authorization": f"bearer {self.apiKey}"
            })
            res.raise_for_status()
            data = res.json()
            yield Measurement.schema().load(data["data"], many=True)
            if data['next'] == "":
                break
            else:
                qs = parse_qs(urlparse(data['next']).query)
                query["cursor"] = qs.get('cursor')[0]
        

