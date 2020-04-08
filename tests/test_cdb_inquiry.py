# coding: utf-8
# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import unittest

from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbInquiryTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(spc)) as s:
            # cdb for standard page request
            i = s.inquiry(alloclen=128)
            cdb = i.cdb
            self.assertEqual(cdb[0], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb[1:3], bytearray(2))
            self.assertEqual(scsi_ba_to_int(cdb[3:5]), 128)
            self.assertEqual(cdb[5], 0)
            cdb = i.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb['evpd'], 0)
            self.assertEqual(cdb['page_code'], 0)
            self.assertEqual(cdb['alloc_len'], 128)

            d = Inquiry.unmarshall_cdb(Inquiry.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            # supported vpd pages
            i = s.inquiry(evpd=1, page_code=0x88, alloclen=300)
            cdb = i.cdb
            self.assertEqual(cdb[0], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb[1], 0x01)
            self.assertEqual(cdb[2], 0x88)
            self.assertEqual(scsi_ba_to_int(cdb[3:5]), 300)
            self.assertEqual(cdb[5], 0)
            cdb = i.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb['evpd'], 1)
            self.assertEqual(cdb['page_code'], 0x88)
            self.assertEqual(cdb['alloc_len'], 300)

            d = Inquiry.unmarshall_cdb(Inquiry.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
