##
#    Copyright (c) 2012-2013 Cyrus Daboo. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##

from cStringIO import StringIO
from pycalendar.icalendar.calendar import Calendar
from pycalendar.tests.utils import TestPyCalendar
from pycalendar.timezonedb import TimezoneDatabase
import os
import tempfile

StandardTZs = (
    """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//calendarserver.org//Zonal//EN
BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:STANDARD
DTSTART:18831118T120358
RDATE:18831118T120358
TZNAME:EST
TZOFFSETFROM:-045602
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19180331T020000
RRULE:FREQ=YEARLY;UNTIL=19190330T070000Z;BYDAY=-1SU;BYMONTH=3
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19181027T020000
RRULE:FREQ=YEARLY;UNTIL=19191026T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:STANDARD
DTSTART:19200101T000000
RDATE:19200101T000000
RDATE:19420101T000000
RDATE:19460101T000000
RDATE:19670101T000000
TZNAME:EST
TZOFFSETFROM:-0500
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19200328T020000
RDATE:19200328T020000
RDATE:19740106T020000
RDATE:19750223T020000
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19201031T020000
RDATE:19201031T020000
RDATE:19450930T020000
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19210424T020000
RRULE:FREQ=YEARLY;UNTIL=19410427T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19210925T020000
RRULE:FREQ=YEARLY;UNTIL=19410928T060000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19420209T020000
RDATE:19420209T020000
TZNAME:EWT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19450814T190000
RDATE:19450814T190000
TZNAME:EPT
TZOFFSETFROM:-0400
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19460428T020000
RRULE:FREQ=YEARLY;UNTIL=19660424T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19460929T020000
RRULE:FREQ=YEARLY;UNTIL=19540926T060000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:STANDARD
DTSTART:19551030T020000
RRULE:FREQ=YEARLY;UNTIL=19661030T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19670430T020000
RRULE:FREQ=YEARLY;UNTIL=19730429T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19671029T020000
RRULE:FREQ=YEARLY;UNTIL=20061029T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19760425T020000
RRULE:FREQ=YEARLY;UNTIL=19860427T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19870405T020000
RRULE:FREQ=YEARLY;UNTIL=20060402T070000Z;BYDAY=1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:20070311T020000
RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20071104T020000
RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
END:VTIMEZONE
END:VCALENDAR
""",
    """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//calendarserver.org//Zonal//EN
BEGIN:VTIMEZONE
TZID:America/Los_Angeles
X-LIC-LOCATION:America/Los_Angeles
BEGIN:STANDARD
DTSTART:18831118T120702
RDATE:18831118T120702
TZNAME:PST
TZOFFSETFROM:-075258
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19180331T020000
RRULE:FREQ=YEARLY;UNTIL=19190330T100000Z;BYDAY=-1SU;BYMONTH=3
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19181027T020000
RRULE:FREQ=YEARLY;UNTIL=19191026T090000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19420209T020000
RDATE:19420209T020000
TZNAME:PWT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19450814T160000
RDATE:19450814T160000
TZNAME:PPT
TZOFFSETFROM:-0700
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19450930T020000
RDATE:19450930T020000
RDATE:19490101T020000
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:STANDARD
DTSTART:19460101T000000
RDATE:19460101T000000
RDATE:19670101T000000
TZNAME:PST
TZOFFSETFROM:-0800
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19480314T020000
RDATE:19480314T020000
RDATE:19740106T020000
RDATE:19750223T020000
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19500430T020000
RRULE:FREQ=YEARLY;UNTIL=19660424T100000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19500924T020000
RRULE:FREQ=YEARLY;UNTIL=19610924T090000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:STANDARD
DTSTART:19621028T020000
RRULE:FREQ=YEARLY;UNTIL=19661030T090000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19670430T020000
RRULE:FREQ=YEARLY;UNTIL=19730429T100000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19671029T020000
RRULE:FREQ=YEARLY;UNTIL=20061029T090000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19760425T020000
RRULE:FREQ=YEARLY;UNTIL=19860427T100000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19870405T020000
RRULE:FREQ=YEARLY;UNTIL=20060402T100000Z;BYDAY=1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:20070311T020000
RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20071104T020000
RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
END:VTIMEZONE
END:VCALENDAR
""",
)

NonStandardTZs = (
    """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//calendarserver.org//Zonal//EN
BEGIN:VTIMEZONE
TZID:America/Cupertino
X-LIC-LOCATION:America/Cupertino
BEGIN:DAYLIGHT
DTSTART:20070311T020000
RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20071104T020000
RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
END:VTIMEZONE
END:VCALENDAR
""",
)


class TestTimezoneDB(TestPyCalendar):

    def setUp(self):
        super(TestTimezoneDB, self).setUp()

        # Standard components explicitly added
        for vtz in StandardTZs:
            cal = Calendar()
            TimezoneDatabase.getTimezoneDatabase()._addStandardTimezone(cal.parseComponent(StringIO(vtz)))

        # Just parsing will add as non-standard
        for vtz in NonStandardTZs:
            Calendar.parseData(vtz)

    def test_getTimezone(self):
        """
        L{TimezoneDatabase.getTimezone} returns correct result.
        """

        data = (
            ("America/New_York", True),
            ("America/Los_Angeles", True),
            ("America/Cupertino", True),
            ("America/FooBar", False),
        )

        for tzid, result in data:
            tz = TimezoneDatabase.getTimezone(tzid)
            if result:
                self.assertTrue(tz is not None)
                self.assertEqual(tz.getID(), tzid)
            else:
                self.assertTrue(tz is None)

    def test_getTimezoneInCalendar(self):
        """
        L{TimezoneDatabase.getTimezoneInCalendar} returns correct result.
        """

        data = (
            ("America/New_York", True),
            ("America/Los_Angeles", True),
            ("America/Cupertino", True),
            ("America/FooBar", False),
        )

        for tzid, result in data:
            cal = TimezoneDatabase.getTimezoneInCalendar(tzid)
            if result:
                self.assertTrue(cal is not None)
                self.assertEqual(cal.getComponents()[0].getID(), tzid)
            else:
                self.assertTrue(cal is None)

    def test_isStandardTimezone(self):
        """
        L{TimezoneDatabase.isStandardTimezone} returns correct result.
        """

        data = (
            ("America/New_York", True),
            ("America/Los_Angeles", True),
            ("America/Cupertino", False),
            ("America/FooBar", False),
        )

        for tzid, result in data:
            self.assertEqual(TimezoneDatabase.isStandardTimezone(tzid), result, "Failed {}".format(tzid))


class TestTimezoneDBCache(TestPyCalendar):

    def setUp(self):
        super(TestTimezoneDBCache, self).setUp()

        # Use temp dbpath
        tmpdir = tempfile.mkdtemp()
        TimezoneDatabase.createTimezoneDatabase(tmpdir)

        # Save standard components to temp directory
        for vtz in StandardTZs:
            cal = Calendar()
            tz = cal.parseComponent(StringIO(vtz))
            tzid_parts = tz.getID().split("/")
            if not os.path.exists(os.path.join(tmpdir, tzid_parts[0])):
                os.makedirs(os.path.join(tmpdir, tzid_parts[0]))
            with open(os.path.join(tmpdir, "{}.ics".format(tz.getID())), "w") as f:
                f.write(vtz)

    def test_isStandardTimezone(self):
        """
        L{TimezoneDatabase.isStandardTimezone} returns correct result when the database
        cache is initially empty.
        """

        data = (
            ("America/New_York", True),
            ("America/Los_Angeles", True),
            ("America/Cupertino", False),
            ("America/FooBar", False),
        )

        TimezoneDatabase.getTimezoneDatabase().clear()

        # Do twice to excersise the cache
        for _ in range(2):
            for tzid, result in data:
                self.assertEqual(TimezoneDatabase.isStandardTimezone(tzid), result, "Failed {}".format(tzid))

        self.assertTrue("America/New_York" in TimezoneDatabase.getTimezoneDatabase().stdtzcache)
        self.assertTrue("America/Los_Angeles" in TimezoneDatabase.getTimezoneDatabase().stdtzcache)
        self.assertFalse("America/Cupertino" in TimezoneDatabase.getTimezoneDatabase().stdtzcache)
        self.assertFalse("America/FooBar" in TimezoneDatabase.getTimezoneDatabase().stdtzcache)

        self.assertFalse("America/New_York" in TimezoneDatabase.getTimezoneDatabase().notstdtzcache)
        self.assertFalse("America/Los_Angeles" in TimezoneDatabase.getTimezoneDatabase().notstdtzcache)
        self.assertTrue("America/Cupertino" in TimezoneDatabase.getTimezoneDatabase().notstdtzcache)
        self.assertTrue("America/FooBar" in TimezoneDatabase.getTimezoneDatabase().notstdtzcache)
