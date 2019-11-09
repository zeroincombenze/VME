from anybox.testing.openerp import SharedSetupTransactionCase


class TestSharedSetup(SharedSetupTransactionCase):
    """Proof that the SharedSetup class works."""

    _data_files = ('sharedsetup.xml',
                   )

    _module_ns = 'sharedtest'

    def setUp(self):
        super(TestSharedSetup, self).setUp()
        self.model = self.registry('res.partner')

    def assertRollbacked(self):
        """Proof that data load and rollback works."""
        rec = self.browse_ref('sharedtest.partner')
        self.assertEquals(rec.name, 'Tests')
        return rec.id

    def test_one(self):
        rec_id = self.assertRollbacked()
        self.model.write(self.cr, self.uid, rec_id, dict(name="spam"))
        # write has really been done
        self.assertRecord(self.model, rec_id, dict(name="spam"))

    def test_two(self):
        rec_id = self.assertRollbacked()
        self.model.write(self.cr, self.uid, rec_id, dict(name="eggs"))
        # write has really been done
        self.assertRecord(self.model, rec_id, dict(name="eggs"))
