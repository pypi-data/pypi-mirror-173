from dataclasses import dataclass, field
from typing import Optional
from dataclasses_json import dataclass_json
from datetime import datetime
from marshmallow import fields


@dataclass_json
@dataclass
class Location:
    """Represents a static measurement location of an organisation

    Attributes
    ----------
    id : int
        The location id of the measurements
    name : str
        ID or name of the measurement type
    organisation : int
        The start time of the time window
    latitude : float
        The latitude coordinate
    longitude : float
        The longitude coordinate
    """
    id: int
    name: str
    organisation: str
    latitude: float
    longitude: float

@dataclass_json
@dataclass
class DeviceSensor:
    """A sensor attached to a device. A sensor produces measurements

    Attributes
    ----------
    code : str
        internal sensor code
    description : str
        internal sensor description
    measurement_type : str
        the type of measurement this sensor produces (unused)
    external_id : str
        the id used by the end device to identify this sensor
    configuration : dict
        sensor specific configuration
    """
    code: str
    description: str
    measurement_type: str
    external_id: str
    configuration: dict

@dataclass_json
@dataclass
class Device:
    """A device

    Attributes
    ----------
    id : int
        the id of this device
    code : str
        the internal code for this device
    description : str
        the internal description for this device
    organisation : str
        the organisation that owns this device
    sensor
        a list of sensors attached to this device
    configuration : dict
        device specific configuration
    location : Location
        the location linked to this device
    """
    id: int
    code: str
    description: str
    organisation: str
    sensors: list[DeviceSensor]
    configuration: dict
    location: Location

@dataclass_json
@dataclass
class Measurement:
    """Represents a measurement with all metadata. Note that properties contain 
    the value at the moment of the measurement. To filter, use the `Id` properties


    Attributes
    ----------
    uplink_message_id : str
        A UUID that identifies the uplink message that resulted in this measurement
    device_id : int
        The device identifier
    device_code : str
        The device code
    device_description : str
        The device description
    device_configuration : dict
        The configured properties for this device
    timestamp : DateTime
        The timestamp at which this measurement took place
    value : float
        The measured value
    measurement_type : str
        The type of measurement
    measurement_type_unit : str
        The unit of the measurement type
    metadata : dict
        Additional data associated with this measurement
    longitude : float
        The longitude coordinate associated with this measurement
        Only set if the device provides a location with the measurement
    latitude : float
        Optional the latitude coordinate associated with this measurement
        Only set if the device provides a location with the measurement
    location_id : int
        Optional the id of the location which is linked to this device
    location_name : str
        The name of the location which is linked to this device
    location_longitude : float
        The longitude coordinate of the location which is linked to this device
    location_latitude : float
        The latitude coordinate of the location which is linked to this device
    sensor_code : str
        A code identifying the sensor that performed the measurement
    sensor_description : str
        The description of the sensor that performed the measurement
    sensor_external_id : str
        The device's sensor specific ID used to match incoming measurement with this sensor
        A null value represents the default/fallback sensor on which measurements will be linked to
    sensor_configuration : dict
        Optional configuration for the sensor

    """
    uplink_message_id: str
    device_id: int
    device_code: str
    device_description: str
    # Timestamp is defined with a custom encoder/decoder to encode/decode from
    # ISO8601 which the API returns/expects
    timestamp: datetime = field(
        metadata={'dataclasses_json': {
            'encoder': datetime.isoformat,
            'decoder': datetime.fromisoformat,
            'mm_field': fields.DateTime(format='iso')
        }}
    )
    value: float
    measurement_type: str
    measurement_type_unit: str
    longitude: Optional[float]
    latitude: Optional[float]
    location_id: Optional[int]
    location_name: Optional[str]
    location_longitude: Optional[float]
    location_latitude: Optional[float]
    sensor_code: Optional[str]
    sensor_description: Optional[str] 
    sensor_external_id: Optional[str]
    # defaults
    device_configuration: Optional[dict] = field(default_factory=dict)
    metadata: Optional[dict] = field(default_factory=dict)
    sensor_configuration: Optional[dict] = field(default_factory=dict)
