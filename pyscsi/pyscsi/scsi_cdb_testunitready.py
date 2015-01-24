# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE

#
# SCSI TestUnitReady command
#


class TestUnitReady(SCSICommand):
    """
    A class to hold information from a testunitready command to a scsi device
    """
    def __init__(self, scsi):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        """
        SCSICommand.__init__(self, scsi, 0, 0)
        self.cdb = self.build_cdb()
        self.execute()

    def build_cdb(self):
        """
        Build a TestUnitReady CDB

        :return: a byte array representing a code descriptor block
        """
        cdb = self.init_cdb(self.scsi.device.opcodes.TEST_UNIT_READY)
        return cdb
