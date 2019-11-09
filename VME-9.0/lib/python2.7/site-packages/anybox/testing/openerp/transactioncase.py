import sys
from .assertions import OpenErpAssertions
from openerp.tests.common import TransactionCase as OpenErpTransactionCase


class TransactionCase(OpenErpAssertions, OpenErpTransactionCase):

    _transaction_case_teared_down = False

    def setUp(self):
        if sys.version_info >= (2, 7):
            # handling same risks as in sharedsetup
            self.addCleanup(self.forceTearDown)
        super(TransactionCase, self).setUp()

    def forceTearDown(self):
        if not self._transaction_case_teared_down:
            self.tearDown()

    def tearDown(self):
        super(TransactionCase, self).tearDown()
        self._transaction_case_teared_down = True
