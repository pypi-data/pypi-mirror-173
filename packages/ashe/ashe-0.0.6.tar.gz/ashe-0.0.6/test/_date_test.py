import unittest
from datetime import datetime, timedelta

from ashe import today, yesterday, get_interval_days


class DateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.today = str(datetime.today().date())
        self.yesterday = str(datetime.today().date() - timedelta(days=1))
        self.today_date = datetime.fromisoformat(self.today).date()
        self.yesterday_date = datetime.fromisoformat(self.yesterday).date()

        self.interval_days = {
            "start": "2022-10-01",
            "end": "2022-10-03",
            "interval": 3,
            "days": ["2022-10-01", "2022-10-02", "2022-10-03"],
            "latest_days": list(reversed([str(datetime.today().date() - timedelta(days=i))
                                          for i in range(3)]))
        }

    def test_date(self) -> None:
        self.assertEqual(self.today, today())
        self.assertEqual(self.today_date, today("date"))
        self.assertEqual(self.yesterday, yesterday())
        self.assertEqual(self.yesterday_date, yesterday("date"))

        self.assertEqual(
            self.interval_days["days"],
            get_interval_days(start=self.interval_days["start"], end=self.interval_days["end"])
        )
        self.assertEqual(
            self.interval_days["days"],
            get_interval_days(start=self.interval_days["start"], interval=self.interval_days["interval"])
        )
        self.assertEqual(
            self.interval_days["days"],
            get_interval_days(end=self.interval_days["end"], interval=self.interval_days["interval"])
        )
        self.assertEqual(
            self.interval_days["latest_days"],
            get_interval_days(interval=self.interval_days["interval"])
        )


if __name__ == "__main__":
    unittest.main()
