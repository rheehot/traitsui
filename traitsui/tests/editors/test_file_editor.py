#  Copyright (c) 2005-2020, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!

import unittest

from traits.api import Directory, Event, File, HasTraits
from traitsui.api import FileEditor, Item, View
from traitsui.tests._tools import (
    create_ui,
    skip_if_not_qt4,
    store_exceptions_on_all_threads,
)


class FileModel(HasTraits):

    filepath = File()

    reload_event = Event()


# Run this against wx too when enthought/traitsui#752 is also fixed.
@skip_if_not_qt4
class TestFileEditor(unittest.TestCase):
    """ Test FileEditor. """

    def check_init_and_dispose(self, style):
        # Test init and dispose by opening and closing the UI
        view = View(Item("filepath", editor=FileEditor(), style=style))
        obj = FileModel()
        with store_exceptions_on_all_threads(), \
                create_ui(obj, dict(view=view)):
            pass

    def test_simple_editor_init_and_dispose(self):
        # This may fail if run against wx, see enthought/traitsui#889
        self.check_init_and_dispose("simple")

    def test_custom_editor_init_and_dispose(self):
        self.check_init_and_dispose("custom")

    def test_custom_editor_reload_changed_after_dispose(self):
        # Test firing reload event on the model after the UI is disposed.
        view = View(
            Item(
                "filepath",
                editor=FileEditor(reload_name="reload_event"),
                style="custom",
            ),
        )
        obj = FileModel()
        with store_exceptions_on_all_threads():
            with create_ui(obj, dict(view=view)):
                pass
            # should not fail.
            obj.reload_event = True
