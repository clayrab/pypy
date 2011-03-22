from pypy.objspace.std.listobject import W_ListObject, EmptyListStrategy, ObjectListStrategy, IntegerListStrategy, StringListStrategy, RangeListStrategy, make_range_list
from pypy.objspace.std.test.test_listobject import TestW_ListObject

class TestW_ListStrategies(TestW_ListObject):

    def test_check_strategy(self):
        assert isinstance(W_ListObject(self.space, []).strategy, EmptyListStrategy)
        assert isinstance(W_ListObject(self.space, [self.space.wrap(1),self.space.wrap('a')]).strategy, ObjectListStrategy)
        assert isinstance(W_ListObject(self.space, [self.space.wrap(1),self.space.wrap(2),self.space.wrap(3)]).strategy, IntegerListStrategy)
        assert isinstance(W_ListObject(self.space, [self.space.wrap('a'), self.space.wrap('b')]).strategy, StringListStrategy)

    def test_empty_to_any(self):
        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.append(self.space.wrap(1.))
        assert isinstance(l.strategy, ObjectListStrategy)

        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.append(self.space.wrap(1))
        assert isinstance(l.strategy, IntegerListStrategy)

        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.append(self.space.wrap('a'))
        assert isinstance(l.strategy, StringListStrategy)

    def test_int_to_any(self):
        l = W_ListObject(self.space, [self.space.wrap(1),self.space.wrap(2),self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.append(self.space.wrap(4))
        assert isinstance(l.strategy, IntegerListStrategy)
        l.append(self.space.wrap('a'))
        assert isinstance(l.strategy, ObjectListStrategy)

    def test_string_to_any(self):
        l = W_ListObject(self.space, [self.space.wrap('a'),self.space.wrap('b'),self.space.wrap('c')])
        assert isinstance(l.strategy, StringListStrategy)
        l.append(self.space.wrap('d'))
        assert isinstance(l.strategy, StringListStrategy)
        l.append(self.space.wrap(3))
        assert isinstance(l.strategy, ObjectListStrategy)

    def test_setitem(self):
        # This should work if test_listobject.py passes
        l = W_ListObject(self.space, [self.space.wrap('a'),self.space.wrap('b'),self.space.wrap('c')])
        assert self.space.eq_w(l.getitem(0), self.space.wrap('a'))
        l.setitem(0, self.space.wrap('d'))
        assert self.space.eq_w(l.getitem(0), self.space.wrap('d'))

        assert isinstance(l.strategy, StringListStrategy)

        # IntStrategy to ObjectStrategy
        l = W_ListObject(self.space, [self.space.wrap(1),self.space.wrap(2),self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.setitem(0, self.space.wrap('d'))
        assert isinstance(l.strategy, ObjectListStrategy)

        # StringStrategy to ObjectStrategy
        l = W_ListObject(self.space, [self.space.wrap('a'),self.space.wrap('b'),self.space.wrap('c')])
        assert isinstance(l.strategy, StringListStrategy)
        l.setitem(0, self.space.wrap(2))
        assert isinstance(l.strategy, ObjectListStrategy)

    def test_insert(self):
        # no change
        l = W_ListObject(self.space, [self.space.wrap(1),self.space.wrap(2),self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.insert(3, self.space.wrap(4))
        assert isinstance(l.strategy, IntegerListStrategy)

        # StringStrategy
        l = W_ListObject(self.space, [self.space.wrap('a'),self.space.wrap('b'),self.space.wrap('c')])
        assert isinstance(l.strategy, StringListStrategy)
        l.insert(3, self.space.wrap(2))
        assert isinstance(l.strategy, ObjectListStrategy)

        # IntegerStrategy
        l = W_ListObject(self.space, [self.space.wrap(1),self.space.wrap(2),self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.insert(3, self.space.wrap('d'))
        assert isinstance(l.strategy, ObjectListStrategy)

        # EmptyStrategy
        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.insert(0, self.space.wrap('a'))
        assert isinstance(l.strategy, StringListStrategy)

        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.insert(0, self.space.wrap(2))
        assert isinstance(l.strategy, IntegerListStrategy)

    def test_list_empty_after_delete(self):
        l = W_ListObject(self.space, [self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.deleteitem(0)
        assert isinstance(l.strategy, EmptyListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1), self.space.wrap(2)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.deleteslice(0, 1, 2)
        assert isinstance(l.strategy, EmptyListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.pop(-1)
        assert isinstance(l.strategy, EmptyListStrategy)

    def test_setslice(self):
        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.setslice(0, 1, 2, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.setslice(0, 1, 2, [self.space.wrap(4), self.space.wrap(5), self.space.wrap(6)])
        assert isinstance(l.strategy, IntegerListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1), self.space.wrap('b'), self.space.wrap(3)])
        assert isinstance(l.strategy, ObjectListStrategy)
        l.setslice(0, 1, 2, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, ObjectListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.setslice(0, 1, 2, [self.space.wrap('a'), self.space.wrap('b'), self.space.wrap('c')])
        assert isinstance(l.strategy, ObjectListStrategy)

    def test_extend(self):
        l = W_ListObject(self.space, [])
        assert isinstance(l.strategy, EmptyListStrategy)
        l.extend(W_ListObject(self.space, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)]))
        assert isinstance(l.strategy, IntegerListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.extend(W_ListObject(self.space, [self.space.wrap('a'), self.space.wrap('b'), self.space.wrap('c')]))
        assert isinstance(l.strategy, ObjectListStrategy)

        l = W_ListObject(self.space, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)
        l.extend(W_ListObject(self.space, [self.space.wrap(4), self.space.wrap(5), self.space.wrap(6)]))
        assert isinstance(l.strategy, IntegerListStrategy)

    def test_rangelist(self):
        l = make_range_list(self.space, 1,3,7)
        assert isinstance(l.strategy, RangeListStrategy)
        v = l.pop(5)
        assert self.space.eq_w(v, self.space.wrap(16))
        assert isinstance(l.strategy, IntegerListStrategy)

        l = make_range_list(self.space, 1,3,7)
        assert isinstance(l.strategy, RangeListStrategy)
        l.append(self.space.wrap("string"))
        assert isinstance(l.strategy, ObjectListStrategy)

        l = make_range_list(self.space, 1,1,5)
        assert isinstance(l.strategy, RangeListStrategy)
        l.append(self.space.wrap(19))
        assert isinstance(l.strategy, IntegerListStrategy)

    def test_keep_range(self):
        # simple list
        l = make_range_list(self.space, 1,1,5)
        assert isinstance(l.strategy, RangeListStrategy)
        x = l.pop(0)
        assert self.space.eq_w(x, self.space.wrap(1))
        assert isinstance(l.strategy, RangeListStrategy)
        l.pop(-1)
        assert isinstance(l.strategy, RangeListStrategy)
        l.append(self.space.wrap(5))
        assert isinstance(l.strategy, RangeListStrategy)

        # complex list
        l = make_range_list(self.space, 1,3,5)
        assert isinstance(l.strategy, RangeListStrategy)
        l.append(self.space.wrap(16))
        assert isinstance(l.strategy, RangeListStrategy)

    def test_empty_range(self):
        l = make_range_list(self.space, 0, 0, 0)
        assert isinstance(l.strategy, EmptyListStrategy)

        l = make_range_list(self.space, 1, 1, 10)
        print l.getitems()
        for i in l.getitems():
            assert isinstance(l.strategy, RangeListStrategy)
            l.pop(-1)

        assert isinstance(l.strategy, EmptyListStrategy)

    def test_range_setslice(self):
        l = make_range_list(self.space, 1, 3, 5)
        assert isinstance(l.strategy, RangeListStrategy)
        l.setslice(0, 1, 3, [self.space.wrap(1), self.space.wrap(2), self.space.wrap(3)])
        assert isinstance(l.strategy, IntegerListStrategy)