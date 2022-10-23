from geoalchemy2 import func
from geopy import geocoders

from dashboard_app.models.orm_settings import Session

geocoders.options.default_user_agent = "1"
geocoders.options.default_timeout = 7
geolocator = geocoders.Nominatim()


def get_coordinates(address):
    coordinates = geolocator.geocode(query=address, namedetails=False, addressdetails=False)
    return [coordinates.latitude, coordinates.longitude]


def get_address(address):
    coordinates = geolocator.geocode(query=address, addressdetails=True)
    add = coordinates.raw["address"]
    return f"{add['road']} {add['house_number']}, {add['postcode']} {add['city']}"


def coordinates_to_point(latitude, longitude):
    with Session() as session:
        point = session.query(func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)).scalar()
    return point
