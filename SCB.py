# -*- coding: utf-8 -*-

import requests
import json

from StringIO import StringIO
from IPython.core.display import HTML

class SCB():
    """Main class for the SCB API."""
    def __init__(self, url):
        self.url = url
        self.query = {"query": [], "response": {}}

    def describe(self):
        """Display metadata for table."""
        r = requests.get(self.url)
        return self._make_table(r.json())

    def filter(self, code, kind, values):
        filter = {"code": code, "selection": {"filter": kind, "values": values}}
        self.query["query"].append(filter)
        return self

    def get(self, out="csv"):
        """Get table data."""
        self.query["response"] = {"format": out}
        self.r = requests.post(self.url, data=json.dumps(self.query))
        return StringIO(self.r.text)

    def _make_table(self, data):
        """Returns an HTML table of data for the IPython notebook."""
        table_head = """
        <table>
        <thead>
        %s
        </thead>
        """

        table_end = """
        <tbody>
        """

        headers = []
        header_row = '<tr>'
        for header in data[0]:
            headers.append(header)
            header_row += '<td>%s</td>' % header
        header_row += '</tr>'
            
        for sublevel in data:
            table_end += '<tr>'
            for prop in headers:
                table_end += '<td>%s</td>' % sublevel[prop]
            table_end += '</tr>'
            
        table_end += '</tbody></table>'

        return HTML((table_head % header_row) + table_end)

    def __repr__(self):
        return '<SCB instance: %s>' % self.url
