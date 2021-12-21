from stats.StatsCompute import StatsCompute


import unittest
entry1 = {"minPrc" : 46010, "volume" : 0.5}
entry2 = {"minPrc" : 46011, "volume" : 0.5}
entry3 = {"minPrc" : 46009, "volume" : 0.5}

class test_StatsCompute(unittest.TestCase):

    def test_init(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        self.assertEqual(len(sc.entries), 1)
        self.assertEqual(sc.nbDown, 0)

    def test_addoneup(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry2)
        self.assertEqual(len(sc.entries), 2)
        self.assertEqual(sc.nbDown, 0)

    def test_addonedown(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry3)
        self.assertEqual(len(sc.entries), 2)
        self.assertEqual(sc.nbDown, 1)

    def test_addonedownoneup(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry3)
        sc.next(entry2)
        self.assertEqual(len(sc.entries), 3)
        self.assertEqual(sc.nbDown, 1)

    def test_add3identical(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        self.assertEqual(len(sc.entries), 3)
        self.assertEqual(sc.nbDown, 0)

    def test_add4identical(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 0)

    def test_add5identical(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 0)

    def test_add5identical(self):
        sc = StatsCompute(4)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        sc.next(entry1)
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 0)
        self.assertEqual(sc.volume, 2.0)

    def test_add4mixed(self):
        sc = StatsCompute(4)
        sc.next({"minPrc" : 46010, "volume" : 0.5})
        sc.next({"minPrc" : 46011, "volume" : 0.2})
        sc.next({"minPrc" : 46010, "volume" : 0.3})
        sc.next({"minPrc" : 46011, "volume" : 0.1})
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 1)
        self.assertEqual(sc.volume, 1.1)

    def test_add4mixed2(self):
        sc = StatsCompute(4)
        sc.next({"minPrc" : 46010, "volume" : 0.5})
        sc.next({"minPrc" : 46009, "volume" : 0.5})
        sc.next({"minPrc" : 46008, "volume" : 0.5})
        sc.next({"minPrc" : 46019, "volume" : 0.5})
        self.assertEqual(len(sc.entries), 4)
        self.assertEqual(sc.nbDown, 2)
