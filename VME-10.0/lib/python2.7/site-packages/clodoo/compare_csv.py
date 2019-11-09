#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""Compare 2 file csv
"""
import sys
import csv
# import pdb

EOD = 999999


class CsvFile():

    def __init__(self):
        pass

    def get_id(self, row):
        id = row.get('id', 999999)
        id = id.split('.')
        i = len(id) - 1
        id = id[i]
        return int(id)

    def open(self, filename, dialect):
        if dialect == 'odoo':
            csv.register_dialect('odoo',
                                 delimiter=',',
                                 quotechar='\"',
                                 quoting=csv.QUOTE_MINIMAL)
        else:
            raise ValueError('Invalid Dialect')
        csv_fd = open(filename, 'rb')
        self.csv_obj = csv.DictReader(csv_fd,
                                      fieldnames=[],
                                      restkey='undef_name',
                                      dialect='odoo')
        header = self.csv_obj.next()
        self.header = header['undef_name']
        csv_fd.close()
        csv_fd = open(filename, 'rb')
        self.csv_obj = csv.DictReader(csv_fd,
                                      fieldnames=self.header,
                                      restkey='undef_name',
                                      dialect='odoo')
        self.lines = []
        self.dict = {}
        header = self.csv_obj.next()
        for row in self.csv_obj:
            id = self.get_id(row)
            if id in self.lines:
                print "Duplicate id %d" % id
            self.lines.append(id)
            self.dict[id] = row
        self.lines = sorted(self.lines)
        self.ix = 0

    def get_next_id(self):
        if self.ix < len(self.lines):
            id = self.lines[self.ix]
            self.ix += 1
            return id
        return EOD


if __name__ == "__main__":
    sts = 0
    dialect = 'odoo'
    filename_left = \
        '/opt/odoo/7.0/l10n-italy/l10n_it_base/partner/data/res.city.csv'
    left = CsvFile()
    left.open(filename_left, dialect)
    filename_right = \
        '/opt/odoo/v7/l10n-italy/l10n_it_base/partner/data/res.city.csv'
    right = CsvFile()
    right.open(filename_right, dialect)
    left_id = left.get_next_id()
    right_id = right.get_next_id()
    while left_id < EOD and right_id < EOD:
        if left_id == right_id:
            # print "Id %d Ok" % left_id
            left_id = left.get_next_id()
            right_id = right.get_next_id()
        elif left_id < right_id:
            print "Id %d only in 7.0" % left_id
            left_id = left.get_next_id()
        elif left_id > right_id:
            print "Id %d only in v7" % right_id
            right_id = right.get_next_id()
        else:
            print "GRRRRR"
            break
    sys.exit(sts)
