import datetime
import unittest

from traits.api import Date, HasTraits, List
from traitsui.api import DateEditor, View, Item

from traitsui.tests._tools import skip_if_not_qt4


class Foo(HasTraits):

    dates = List(Date)

    single_date = Date()


def single_select_custom_view():
    view = View(
        Item(
            name='single_date',
            style="custom",
            editor=DateEditor(multi_select=False),
        )
    )
    return view


def multi_select_custom_view():
    view = View(
        Item(
            name='dates',
            style="custom",
            editor=DateEditor(multi_select=True),
        )
    )
    return view


@skip_if_not_qt4
class TestDateEditorCustomQt(unittest.TestCase):

    def test_single_select_qt4(self):
        foo, _, editor = self.get_custom_editor(single_select_custom_view)

        date = datetime.date(2018, 2, 3)
        self.click_date_on_editor(editor, date)
        self.assertEqual(foo.single_date, date)

    def test_multi_select_dates_on_editor(self):
        foo, ui, editor = self.get_custom_editor(multi_select_custom_view)
        dates = [
            datetime.date(2018, 2, 3), datetime.date(2018, 2, 1)
        ]
        for date in dates:
            self.click_date_on_editor(editor, date)

        for date in dates:
            self.check_select_status(editor=editor, date=date, selected=True)

        self.assertEqual(foo.dates, sorted(dates))

    def test_multi_select_qt4_styles_reset(self):
        foo, ui, editor = self.get_custom_editor(multi_select_custom_view)

        date = datetime.date(2018, 2, 1)
        self.click_date_on_editor(editor, date)
        self.check_select_status(editor=editor, date=date, selected=True)

        self.click_date_on_editor(editor, date)
        self.check_select_status(editor=editor, date=date, selected=False)

    def test_multi_select_qt4_set_model_dates(self):
        # Test setting the dates from the model object.
        foo, ui, editor = self.get_custom_editor(multi_select_custom_view)
        foo.dates = [
            datetime.date(2010, 1, 2),
            datetime.date(2010, 2, 1),
        ]

        for date in foo.dates:
            self.check_select_status(editor=editor, date=date, selected=True)

    # --------------------
    # Helper methods
    # --------------------

    def get_custom_editor(self, view_factory):
        foo = Foo()
        ui = foo.edit_traits(view=view_factory())
        editor, = ui._editors
        return foo, ui, editor

    def check_select_status(self, editor, date, selected):
        from pyface.qt import QtCore, QtGui
        qdate = QtCore.QDate(date.year, date.month, date.day)
        textformat = editor.control.dateTextFormat(qdate)
        if selected:
            self.assertEqual(
                textformat.fontWeight(),
                QtGui.QFont.Bold,
                "{!r} is not selected.".format(date))

            self.assertEqual(
                textformat.background().color().green(),
                128,
                "Expected non-zero green color value.")
        else:
            self.assertEqual(
                textformat.fontWeight(),
                QtGui.QFont.Normal,
                "{!r} is not unselected.".format(date),
            )
            self.assertEqual(
                textformat.background().style(),
                0,   # Qt.BrushStyle.NoBrush,
                "Expected brush to have been reset."
            )
            self.assertEqual(
                textformat.background().color().green(),
                0,
                "Expected color to have been reset.")

    def click_date_on_editor(self, editor, date):
        from pyface.qt import QtCore
        # QCalendarWidget.setSelectedDate modifies internal state
        # instead of triggering the click signal.
        # So we call update_object directly
        editor.update_object(
            QtCore.QDate(date.year, date.month, date.day))