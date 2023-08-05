"""
Classes and functions for parsing home-assistant data.
"""
from typing import Tuple

from urllib.parse import urlparse
import pandas as pd
from sqlalchemy import create_engine, text

from . import config, functions


def db_from_hass_config(path=None, **kwargs):
    """Initialize a database from HASS config."""
    if path is None:
        path = config.find_hass_config()

    url = config.db_url_from_hass_config(path)
    return HassDatabase(url, **kwargs)


def get_db_type(url):
    return urlparse(url).scheme.split("+")[0]


def stripped_db_url(url):
    """Return a version of the DB url with the password stripped out."""
    parsed = urlparse(url)

    if parsed.password is None:
        return url

    return parsed._replace(
        netloc="{}:***@{}".format(parsed.username, parsed.hostname)
    ).geturl()


class HassDatabase:
    """
    Initializing the parser fetches all of the data from the database and
    places it in a master pandas dataframe.
    """

    def __init__(self, url, *, fetch_entities=True):
        """
        Parameters
        ----------
        url : str
            The URL to the database.
        """
        self.url = url
        self.entities = None
        try:
            self.engine = create_engine(url)
            print("Successfully connected to database", stripped_db_url(url))
            if fetch_entities:
                self.fetch_entities()
        except Exception as exc:
            if isinstance(exc, ImportError):
                raise RuntimeError(
                    "The right dependency to connect to your database is "
                    "missing. Please make sure that it is installed."
                )

            print(exc)
            raise

        self.db_type = get_db_type(url)

    def perform_query(self, query, **params):
        """Perform a query."""
        try:
            return self.engine.execute(query, params)
        except:
            print(f"Error with query: {query}")
            raise

    def fetch_entities(self) -> None:
        """Fetch entities for which we have data."""
        query = text(
            """
            SELECT DISTINCT(entity_id) FROM states
            """
        )
        response = self.perform_query(query)

        # Parse the domains from the entities.
        self.entities = [e[0] for e in response]
        print(f"There are {len(self.entities)} entities with data")

    def fetch_all_sensor_data(self, limit=50000, get_attributes=False) -> pd.DataFrame:
        """
        Fetch data for all sensor entities.

        Arguments:
        - limit (default: 50000): Limit the maximum number of state changes loaded.
            If None, there is no limit.
        - get_attributes: If True, LEFT JOIN the attributes table to retrieve event's attributes.
        """
        
        if get_attributes:
            query = """
                SELECT entity_id, state, last_updated, shared_attrs
            """
        else:
            query = """
                SELECT entity_id, state, last_updated
            """
        
        query += "FROM states"
        
        if get_attributes:
            query += """
                LEFT JOIN state_attributes ON states.attributes_id = state_attributes.attributes_id
            """
            
        query += """
            WHERE
                entity_id  LIKE '%sensor%'
            AND
                state NOT IN ('unknown', 'unavailable')
            ORDER BY last_updated DESC
            """
        
        if limit is not None:
            query += f"LIMIT {limit}"
        df = pd.read_sql_query(query, self.url)
        print(f"The returned Pandas dataframe has {df.shape[0]} rows of data.")
        return df

    def fetch_all_data_of(self, sensors: Tuple[str], limit=50000, get_attributes=False) -> pd.DataFrame:
        """
        Fetch data for sensors.

        Arguments:
        - limit (default: 50000): Limit the maximum number of state changes loaded.
            If None, there is no limit.
        - get_attributes: If True, LEFT JOIN the attributes table to retrieve event's attributes.
        """
        sensors_str = str(tuple(sensors))
        if len(sensors) == 1:
            sensors_str = sensors_str.replace(",", "")

        if get_attributes:
            query = """
                SELECT entity_id, state, last_updated, shared_attrs
            """
        else:
            query = """
                SELECT entity_id, state, last_updated
            """

        query += "FROM states"
        
        if get_attributes:
            query += """
                LEFT JOIN state_attributes ON states.attributes_id = state_attributes.attributes_id
            """
            
        query += f"""
            WHERE
                entity_id IN {sensors_str}
            AND
                state NOT IN ('unknown', 'unavailable')
            ORDER BY last_updated DESC
            """

        if limit is not None:
            query += f"LIMIT {limit}"
            
        df = pd.read_sql_query(query, self.url)
        print(f"The returned Pandas dataframe has {df.shape[0]} rows of data.")
        return df
