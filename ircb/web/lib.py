# -*- coding: utf-8 -*-
import json

from aiohttp import web


class View(web.View):
    store = None
    fields = None
    excluded_fields = []

    __fields = None

    def get_fields(self):
        if self.__fields is None:
            if self.store:
                fields = set(self.store.fields())
            else:
                fields = set(self.fields or [])
            if self.fields is None:
                self.fields = fields
            else:
                fields = set(self.fields).difference(fields)
            fields = fields.difference(set(self.excluded_fields))
            self.__fields = fields
        return self.__fields

    def serialize(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(self._serialize_row(item))
        else:
            result = self._serialize_row(data)
        return json.dumps(result)

    def _serialize_row(self, row):
        d = row.to_dict(serializable=True)
        result = {}
        fields = self.get_fields()
        for field in fields:
            result[field] = d[field]
        return result
