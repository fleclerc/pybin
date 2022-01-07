from stats.StatsCompute import StatsCompute
import datetime
import unittest

entry1 = {"minPrc" : 46010, "volume" : 0.5}
entry2 = {"minPrc" : 46011, "volume" : 0.5}
entry3 = {"minPrc" : 46009, "volume" : 0.5}
entrybase = {
    '_id': {'date': {'year': 2021, 'month': 12, 'day': 15, 'hour': 0, 'minute': 56},
            'symbol': 'BTCUSDT'
            },
    'minPrc': 48100.1, 'maxPrc': 48121.0, 'volume': 31.385,
    'timestamp': datetime.datetime(2021, 12, 15, 0, 56, 36, 232000)
}
    
class EntryHelper:
    def __init__(self) -> None:
        self.timestamp = entrybase["timestamp"]
    
    def entry(self, price, volume = 0.5):
        e = entrybase.copy()
        e["minPrc"] = price
        e["volume"] = volume
        e["timestamp"] = self.timestamp
        self.timestamp += datetime.timedelta(seconds=1)
        return e

class test_StatsCompute(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        self.entryhelper = EntryHelper()
        super().__init__(methodName=methodName)

    def entry(self, price, volume = 0.5):
        return self.entryhelper.entry(price, volume)

    def test_init(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        self.assertEqual(len(sc.entries), 1)
        self.assertEqual(sc.nbDown, 0)

    def test_addoneup(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        sc.next(self.entry(46011))
        self.assertEqual(len(sc.entries), 2)
        self.assertEqual(sc.nbDown, 0)

    def test_addonedown(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        sc.next(self.entry(46009))
        self.assertEqual(len(sc.entries), 2)
        self.assertEqual(sc.nbDown, 1)

    def test_addonedownoneup(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        sc.next(self.entry(46009))
        sc.next(self.entry(46011))
        self.assertEqual(len(sc.entries), 3)
        self.assertEqual(sc.nbDown, 1)

    def test_add3identical(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        self.assertEqual(len(sc.entries), 3)
        self.assertEqual(sc.nbDown, 0)

    def test_add4identical(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 0)

    def test_add5identical(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        sc.next(self.entry(46010))
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 0)
        self.assertEqual(sc.volume, 2.0)

    def test_add4mixed(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010, volume=0.5))
        sc.next(self.entry(46011, volume=0.2))
        sc.next(self.entry(46010, volume=0.3))
        sc.next(self.entry(46011, volume=0.1))
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 1)
        self.assertEqual(sc.volume, 1.1)

    def test_add4mixed2(self):
        sc = StatsCompute(4)
        sc.next(self.entry(46010, volume=0.5))
        sc.next(self.entry(46009, volume=0.5))
        sc.next(self.entry(46008, volume=0.5))
        sc.next(self.entry(46019, volume=0.5))
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 2)
