from influxdb_client import Buckets
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


class DmsInflux2Async(InfluxDBClientAsync):
    def __init__(self, url=None, token=None, org=None, enable_gzip=True, timezone_offset: int = None,
                 timeout=20_000):
        self.query_str = None
        self.predicates = None

        self.time_offset = timezone_offset
        self.time_shift = f'{timezone_offset}h' if timezone_offset is not None else None

        super().__init__(url=url, token=token, org=org, enable_gzip=enable_gzip, timeout=timeout)

    def buckets_api(self) -> Buckets:
        return Buckets(self)
