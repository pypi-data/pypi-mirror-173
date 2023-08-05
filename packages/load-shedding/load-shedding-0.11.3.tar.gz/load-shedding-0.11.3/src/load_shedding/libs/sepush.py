#      A python library for getting Load Shedding schedules.
#      Copyright (C) 2021  Werner Pieterson
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
import http
import json
from typing import Any, Dict, List

import certifi
import urllib3


class SePushError(Exception):
    pass


ESKOM = "eskom"
CITY_OF_CAPE_TOWN = "capetown"


class SePush:
    base_url = "https://us-central1-sepush-app.cloudfunctions.net/sepush-serverless-business-api-staging-http/business/2.0"
    token = ""

    def __init__(self, token=None):
        if token:
            self.token = token

    def areas_search(self, text: str) -> List[Dict]:
        url = f"{self.base_url}/areas_search?text={text}"
        data = """{"areas":[{"id":"capetown-2-milnerton","name":"Milnerton (2)","region":"City of Cape Town"},{"id":"eskde-10-milnertonsp2cityofcapetownwesterncape","name":"Milnerton SP 2 (10)","region":"Eskom Direct, City of Cape Town, Western Cape"},{"id":"eskde-14-milnertoncityofcapetownwesterncape","name":"Milnerton (14)","region":"Eskom Direct, City of Cape Town, Western Cape"},{"id":"eskde-14-milnertonridgecityofcapetownwesterncape","name":"Milnerton Ridge (14)","region":"Eskom Direct, City of Cape Town, Western Cape"},{"id":"eskde-14-milnertonspcityofcapetownwesterncape","name":"Milnerton SP (14)","region":"Eskom Direct, City of Cape Town, Western Cape"},{"id":"eskde-14-milnertonsp1cityofcapetownwesterncape","name":"Milnerton SP 1 (14)","region":"Eskom Direct, City of Cape Town, Western Cape"}]}"""
        # data = _call(url, self.token)
        return json.loads(data)

    def area(self, area_id: str) -> List[Dict]:
        url = f"{self.base_url}/area?id={area_id}"
        data = """{"events":[{"end":"2022-10-22T10:30:00+02:00","note":"Stage 3","start":"2022-10-22T08:00:00+02:00"},{"end":"2022-10-22T18:30:00+02:00","note":"Stage 3","start":"2022-10-22T16:00:00+02:00"}],"info":{"name":"Milnerton (14)","region":"Eskom Direct, City of Cape Town, Western Cape"},"schedule":{"days":[{"date":"2022-10-21","name":"Friday","stages":[["16:00-18:30"],["08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-20:30"],["00:00-02:30","08:00-12:30","16:00-20:30"],["00:00-04:30","08:00-12:30","16:00-20:30"],["00:00-04:30","08:00-12:30","16:00-20:30"]]},{"date":"2022-10-22","name":"Saturday","stages":[[],["16:00-18:30"],["08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-20:30"],["00:00-02:30","08:00-12:30","16:00-20:30"],["00:00-04:30","08:00-12:30","16:00-20:30"]]},{"date":"2022-10-23","name":"Sunday","stages":[["00:00-02:30"],["00:00-02:30"],["00:00-02:30","16:00-18:30"],["00:00-02:30","08:00-10:30","16:00-18:30"],["00:00-04:30","08:00-10:30","16:00-18:30"],["00:00-04:30","08:00-10:30","16:00-18:30"],["00:00-04:30","08:00-10:30","16:00-20:30"],["00:00-04:30","08:00-12:30","16:00-20:30"]]},{"date":"2022-10-24","name":"Monday","stages":[["08:00-10:30"],["00:00-02:30","08:00-10:30"],["00:00-02:30","08:00-10:30"],["00:00-02:30","08:00-10:30","16:00-18:30"],["00:00-02:30","08:00-12:30","16:00-18:30"],["00:00-04:30","08:00-12:30","16:00-18:30"],["00:00-04:30","08:00-12:30","16:00-18:30"],["00:00-04:30","08:00-12:30","16:00-20:30"]]},{"date":"2022-10-25","name":"Tuesday","stages":[["14:00-16:30"],["06:00-08:30","14:00-16:30"],["06:00-08:30","14:00-16:30"],["06:00-08:30","14:00-16:30","22:00-00:30"],["06:00-08:30","14:00-18:30","22:00-00:30"],["06:00-10:30","14:00-18:30","22:00-00:30"],["06:00-10:30","14:00-18:30","22:00-00:30"],["06:00-10:30","14:00-18:30","22:00-00:30"]]},{"date":"2022-10-26","name":"Wednesday","stages":[["22:00-00:30"],["14:00-16:30","22:00-00:30"],["06:00-08:30","14:00-16:30","22:00-00:30"],["06:00-08:30","14:00-16:30","22:00-00:30"],["06:00-08:30","14:00-16:30","22:00-00:30"],["06:00-08:30","14:00-18:30","22:00-00:30"],["06:00-10:30","14:00-18:30","22:00-00:30"],["00:00-02:30","06:00-10:30","14:00-18:30","22:00-00:30"]]},{"date":"2022-10-27","name":"Thursday","stages":[[],["22:00-00:30"],["14:00-16:30","22:00-00:30"],["06:00-08:30","14:00-16:30","22:00-00:30"],["00:00-02:30","06:00-08:30","14:00-16:30","22:00-00:30"],["00:00-02:30","06:00-08:30","14:00-16:30","22:00-00:30"],["00:00-02:30","06:00-08:30","14:00-18:30","22:00-00:30"],["00:00-02:30","06:00-10:30","14:00-18:30","22:00-00:30"]]}],"source":"https://loadshedding.eskom.co.za/"}}"""
        # data = _call(url, self.token)
        return json.loads(data)

    def check_allowance(self) -> Dict:
        url = f"{self.base_url}/api_allowance"
        data = _call(url, self.token)
        return json.loads(data)

    def status(self) -> int:
        url = f"{self.base_url}/status"
        data = """{"status":{"capetown":{"name":"Cape Town","next_stages":[{"stage":"1","stage_start_timestamp":"2022-10-22T06:00:00+02:00"},{"stage":"3","stage_start_timestamp":"2022-10-22T14:00:00+02:00"}],"stage":"3","stage_updated":"2022-10-21T22:00:25.203469+02:00"},"eskom":{"name":"South Africa","next_stages":[],"stage":"3","stage_updated":"2022-10-20T05:51:45.328049+02:00"}}}"""
        # data = _call(url, self.token)
        return json.loads(data)


def _call(url: str, token: str) -> Any:
    try:
        with urllib3.PoolManager(
            retries=urllib3.Retry(total=3), ca_certs=certifi.where()
        ) as conn:
            headers = {"Token": token}
            r = conn.request("GET", url, headers=headers)
            if r.status != 200:
                raise urllib3.response.HTTPError(r.status, r.reason)
            return r.data
    except Exception as e:
        error = json.loads(r.data).get("error")
        raise SePushError(error, r.status, r.reason) from e
