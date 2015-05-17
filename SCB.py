# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd

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
        self.content = r.json()
        if type(self.content) == list:
            return self._make_table(r.json())
        else:
            return self._make_filter_table(self.content['variables'])

    def go(self, fragment):
        fragment = fragment.strip()
        if self.url.endswith('/'):
            if fragment.startswith('/'):
                fragment = fragment[1:]
        else:
            if not fragment.startswith('/'):
                fragment = '/%s' % fragment
        self.url += fragment
        return self.describe()

    def filter(self, code, kind, values):
        """Creates a new filter for the current table"""
        new_filter = {"code": code, "selection": {"filter": kind, "values": values}}
        try:
            ix = next(i for (i, d) in enumerate(self.query['query']) if d['code'] == code)
            self.query['query'][ix] = new_filter
        except StopIteration:
            self.query["query"].append(new_filter)
        return self

    def get(self, out="csv"):
        """Get table data."""
        self.query["response"] = {"format": out}
        self.r = requests.post(self.url, data=json.dumps(self.query))
        return pd.read_csv(StringIO(self.r.text))

    def flush(self):
        del self.query['query'][:]
        return self

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
            header_row += '<th>%s</th>' % header
        header_row += '</tr>'
            
        for sublevel in data:
            table_end += '<tr>'
            for prop in headers:
                table_end += '<td>%s</td>' % sublevel[prop]
            table_end += '</tr>'
            
        table_end += '</tbody></table>'

        return HTML((table_head % header_row) + table_end)

    def _make_filter_table(self, data):
        """Returns an HTML table of possible filters for a table."""
        table_head = """
        <table>
        <thead>
        <tr><th>code</th><th>text</th><th>values</th></tr>
        </thead>
        """

        table_end = """
        <tbody>
        """
            
        for code in data:
            if len(code['values']) > 10:
                values = ', '.join(map(str, code['values'][:5])) + ' [...] ' +\
                         ', '.join(map(str, code['values'][-5:]))
            else: 
                values = ', '.join(map(str, code['values']))
            table_end += '<tr>'
            table_end += '<td>%s</td><td>%s</td><td>%s</td>' % (code['code'], code['text'], values)
            table_end += '</tr>'
            
        table_end += '</tbody></table>'

        return HTML(table_head + table_end)

    def __repr__(self):
        return '<SCB instance: %s>' % self.url
