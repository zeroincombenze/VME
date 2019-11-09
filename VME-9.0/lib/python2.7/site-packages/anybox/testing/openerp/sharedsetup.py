"""This module provides rollbacked tests with shared data loaded once.
"""
import os
import sys
from .assertions import OpenErpAssertions
from openerp.tests.common import SingleTransactionCase
from openerp.tools.convert import convert_xml_import


class SharedSetupTransactionCase(OpenErpAssertions, SingleTransactionCase):
    """Insulated tests with a shared data setup.

    Loads data and plays the tests within a single transaction.
    XML files listed in _data_files class attribute are loaded.
    The path is interpreted relative to the package in which the subclass sits.

    For example, for a class defined in MODULE/tests/test_spam,
    _data_files = ('data/spam.xml',)
    will load MODULE/tests/data/spam.xml

    The path separator is always / for convenience on POSIX systems.
    On operating systems with different path separators,
    an automatic conversion is done.

    A rollback to savepoint is issued after each test.
    The whole transaction is rollbacked at class teardown
    """

    _savepoint_name = None

    _data_files = ()

    _module_ns = 'tests'  # indicate in which module's namespace the loaded data should be put

    @classmethod
    def savepoint_name(cls):
        name = cls._savepoint_name
        return name if name is not None else cls.__name__

    @classmethod
    def setUpClass(cls):
        SingleTransactionCase.setUpClass()
        # Any exception from here would cause tear downs not to
        # be executed.
        # This has been witnessed to cause PG to deadlock,
        # a major developper headache and lost time
        try:
            cls.initTestData()
        except:
            cls.tearDownClass()
            raise

        cls.cr.execute('SAVEPOINT "%s"' % cls.savepoint_name())

    @classmethod
    def initTestData(cls):
        """Loads the data file before the savepoint.

        Subclasses can override this, and possibly call super() to still benefit from the data
        loading facility."""
        module = sys.modules[cls.__module__]
        base_path = os.path.dirname(module.__file__)
        for path in cls._data_files:
            path = path.split('/')
            path.insert(0, base_path)
            path = os.path.join(*path)
            convert_xml_import(cls.cr, cls._module_ns, path)  # TODO YML, CSV ?

    def tearDown(self):
        # GR: direct API for ROLLBACK TO SAVEPOINT on cnx object ?
        self.cr.execute('ROLLBACK TO SAVEPOINT "%s"' % self.savepoint_name())

    @classmethod
    def tearDownClass(cls):
        cls.registry('ir.model.data').clear_caches()
        super(SharedSetupTransactionCase, cls).tearDownClass()
