import py
from pypy.jit.backend.cli.test.test_zrpy_basic import CliTranslatedJitMixin
from pypy.jit.metainterp.test import test_send


class TestSend(CliTranslatedJitMixin, test_send.TestOOtype):
    # for the individual tests see
    # ====> ../../../metainterp/test/test_send.py

    def skip_loop(self):
        py.test.skip('jump across loops not implemented yet')

    def skip(self):
        py.test.skip('in-progress')

    test_three_receivers = skip_loop
    
    test_indirect_call_unknown_object_1 = skip
    test_three_cases = skip
    test_three_classes = skip
    test_recursive_call_to_portal_from_blackhole = skip
    test_residual_oosend = skip
