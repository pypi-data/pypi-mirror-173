#                                   MIT License
#
#              Copyright (c) 2022 Javier Alonso <jalonso@teldat.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#      copies of the Software, and to permit persons to whom the Software is
#            furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
#                 copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#                                    SOFTWARE.
"""Watchdog pluggable interface"""
from __future__ import annotations

import typing
import systemd.daemon as systemd

from orcha.lib.pluggable import Pluggable
from orcha.interfaces import Message, Petition

from .constants import WATCHDOG_ID
from .petition import WatchdogPetition

if typing.TYPE_CHECKING:
    from typing import Optional


class Watchdog(Pluggable):
    def on_manager_start(self):
        systemd.notify("READY=1")

    def on_manager_shutdown(self):
        systemd.notify("STOPPING=1")

    def on_message_preconvert(self, m: Message) -> Optional[Petition]:
        if m.id == WATCHDOG_ID:
            return WatchdogPetition(queue=m.extras.get("queue"))
