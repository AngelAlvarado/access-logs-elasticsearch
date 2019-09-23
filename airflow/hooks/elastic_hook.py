import logging
import requests
from airflow import AirflowException
from airflow.hooks.http_hook import HttpHook
import json


class ElasticHook(HttpHook):
    def search(self, index_and_type, args):
        url = self.base_url + index_and_type + '/_search'

        req = requests.Request('GET', url, json=args)
        prep_req = session.prepare_request(req)

        resp = session.send(prep_req)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error("HTTP error: " + resp.reason)
            raise AirflowException(str(resp.status_code) + ":" + resp.reason)

        return json.loads(resp.content)


    def insert_log(self, index_and_type, args):
        try:
            url ="http://elasticsearch:9200/" + index_and_type
            req = requests.post(url, json=args)
        except requests.exceptions.HTTPError:
            logging.error("HTTP error: "+ req.status_code)
            raise AirflowException(str(req.status_code) + ":" + req.reason)

        return json.loads(req.content)      