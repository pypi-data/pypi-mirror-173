# Copyright 2022 Tiger Miao
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Tracker"""
from pysnooper.tracer import Tracer
from pysnooper.tracer import get_path_and_source_from_frame


class Tracker(Tracer):
    """
    Framework Code Execution Tracking
    Args:
        ms (bool): Framework type
        filter (dict): Tracking filtering
        *args: Tracer args
        **kwargs: Tracer args
    """

    def __init__(self, *args, **kwargs):
        # filter={"path_whitelist": [], "func_whitelist": []},
        # tracking_filter=None, ms=True
        super(Tracker, self).__init__(*args, **kwargs)
        tracking_filter = kwargs.get('tracking_filter')

        if tracking_filter:
            self.func_whitelist = tracking_filter.get('func_whitelist') or []
            self.path_whitelist = tracking_filter.get('path_whitelist') or []

        self.ms = kwargs.get('ms')
        self.root_file = ""
        self.func_whitelist += ["tracking_wrapper", "deco"]

    def _frame_filter(self, frame):
        if self.ms:
            return self._frame_filter_ms(frame)
        return True

    def _frame_filter_ms(self, frame):
        """
        Filter the frame information of
        Args:
            frame: The python frame
            event: Reserved Fields
            arg: Reserved Fields

        Returns (bool): frame information
        """
        result = True
        # line_no = frame.f_lineno
        func_name = frame.f_code.co_name
        # source_path, source = get_path_and_source_from_frame(frame)
        source_path = get_path_and_source_from_frame(frame)
        source_path = source_path if not self.normalize else os.path.basename(source_path)

        if self.root_file == "":
            self.root_file = source_path
            self.root_func = func_name
            return result

        # for windows path.
        if self.root_file.rfind(".\\") == 0:
            self.root_file = self.root_file[2:]

        # debug function only for current file or path whitelist
        if (self.root_file not in source_path) and (self.root_file not in self.path_whitelist):
            return False

        # debug current function
        if func_name != self.root_func and (func_name not in self.func_whitelist):
            return False
        return result

    def trace(self, frame, event, arg):
        if not self._frame_filter(frame):
            return None
        return super(Tracker, self).trace(frame, event, arg)
