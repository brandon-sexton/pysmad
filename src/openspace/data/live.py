import requests

from openspace.coordinates.states import LiveVector, LiveVectorSet
from openspace.estimation.obs import LiveOpticalObservation, LiveOpticalSet
from openspace.messages import Alerts
from openspace.time import Epoch


class Query:

    DEFAULT_QUERY_DELTA: float = 1.5
    BASE_URL: str = "https://unifieddatalibrary.com/udl/"
    QUERY_COUNT: str = "count"
    VECTOR_QUERY: str = "statevector"
    EO_OBS_QUERY: str = "eoobservation"
    BURN_QUERY: str = "maneuver"
    EPOCH_MAP: dict = {VECTOR_QUERY: "?epoch=", EO_OBS_QUERY: "?obTime=", BURN_QUERY: "?eventStartTime="}
    QUERY_MAX: int = 10000

    def __init__(self, creds: str):

        self.credentials: str = creds
        self.query_max: int = Query.QUERY_MAX

    def _build_basic_query(self, type: str) -> str:
        return "".join([Query.BASE_URL, type, Query.EPOCH_MAP[type]])

    def _build_count_query(self, base_url: str) -> str:
        return "/".join([base_url, Query.QUERY_COUNT])

    def _add_epoch_filter(self, url: str, start: str, end: str) -> str:
        return "".join([url, "..".join([start, end])])

    def _add_source_filter(self, url: str, source: str) -> str:
        return "&source=".join([url, source])

    def _add_sat_id_filter(self, url: str, sat_id: str) -> str:
        return "&idOnOrbit=".join([url, sat_id])

    def _add_data_mode_filter(self, url: str) -> str:
        return "&dataMode=".join([url, "REAL"])

    def get_vector_set(self, start: Epoch, end: Epoch, source: str = None, sat_id: str = None) -> LiveVectorSet:
        msg = self.get_state_vector_json(start, end, source, sat_id)
        states = LiveVectorSet()
        for state in msg:
            states.process_vector(LiveVector(state))
        return states

    def _set_max_results(self, url: str) -> str:
        return "&".join([url, "".join(["maxResults=", str(self.query_max)])])

        # for state in msgs:
        #     scc = state['idOnOrbit']
        #     ep = Epoch.from_udl_string(state['epoch'])
        #     if scc not in states:
        #         states[scc] = GCRF(
        #             ep,
        #             Vector3D(state['xpos'], state['ypos'], state['zpos']),
        #             Vector3D(state['xvel'], state['yvel'], state['zvel'])
        #         )
        #     elif ep.value > states[scc].epoch.value:
        #         states[scc] = GCRF(
        #             ep,
        #             Vector3D(state['xpos'], state['ypos'], state['zpos']),
        #             Vector3D(state['xvel'], state['yvel'], state['zvel'])
        #         )

    def get_maneuver_list(self):
        url = "https://unifieddatalibrary.com/udl/maneuver?eventStartTime=%3E" + self.start_epoch
        msgs = self.get_json(url)
        sccs = {}
        for msg in msgs:
            sccs[msg["idOnOrbit"]] = True
        print(len(sccs.keys()), "possible maneuvers reported by Kratos.")
        return [key for key in sccs.keys()]

    def get_optical_set(self, start: Epoch, end: Epoch, source: str = None, sat_id: str = None) -> LiveOpticalSet:
        msg = self.get_eo_observation_json(start, end, source, sat_id)
        obs = LiveOpticalSet()
        for ob in msg:
            obs.process_observation(LiveOpticalObservation(ob))
        return obs

    def get_eo_observation_json(self, start: Epoch, end: Epoch, source: str = None, sat_id: str = None):
        return self.get_json(Query.EO_OBS_QUERY, start, end, source, sat_id)

    def get_state_vector_json(self, start: Epoch, end: Epoch, source: str = None, sat_id: str = None):
        return self.get_json(Query.VECTOR_QUERY, start, end, source, sat_id)

    def get_json(self, type: str, start: Epoch, end: Epoch, source: str = None, sat_id: str = None):

        # filter by data type
        url = self._build_basic_query(type)

        # filter by date range
        url = self._add_epoch_filter(url, start.to_udl_string(), end.to_udl_string())

        # filter by data source
        if source is not None:
            url = self._add_source_filter(url, source)

        # filter by satellite ID
        if sat_id is not None:
            url = self._add_sat_id_filter(url, sat_id)

        # filter max results
        url = self._set_max_results(url)

        # filter for real data
        url = self._add_data_mode_filter(url)

        # perform query and print status
        Alerts.print_query_start(url)
        results = requests.get(url, headers={"Authorization": self.credentials}, verify=None).json()
        count = len(results)
        if len(results) == self.query_max:
            Alerts.print_query_max_warning()
        if count > 0:
            Alerts.print_successful_query(count)

        return results
