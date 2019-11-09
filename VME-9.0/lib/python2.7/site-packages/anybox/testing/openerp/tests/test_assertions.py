from anybox.testing.openerp import TransactionCase

import random


class TestAssertions(TransactionCase):
    """Proof that the high level assertions do work."""

    def setUp(self):
        super(TestAssertions, self).setUp()
        # we could do this in a SharedSetupTransactionCase, but the point here
        # is to test the helper methods in the simplest context
        model = self.model = self.registry('res.partner')
        self.rec_id = model.create(self.cr, self.uid, dict(name="Assertor"))

    def test_assertRecord_model_inst(self):
        self.assertRecord(self.model, self.rec_id, dict(name="Assertor"))
        self.assertRaises(AssertionError, self.assertRecord,
                          self.model, self.rec_id, dict(name="Assertors"))

    def test_assertRecord_model_name(self):
        self.assertRecord('res.partner', self.rec_id, dict(name="Assertor"))

    def test_assertRecord_list_to_set(self):
        model, cr, uid, rec_id = self.model, self.cr, self.uid, self.rec_id

        # doing with bank_ids, any other o2m or m2m would do. If this
        # one gets too complicated (should find another one already, but
        # good enough for now)
        model.write(cr, uid, rec_id,
                    dict(bank_ids=[(0, 0, dict(state='', acc_number=1)),
                                   (0, 0, dict(state='', acc_number=2)),
                                   (0, 0, dict(state='', acc_number=3))]))
        bk_ids = self.registry('res.partner.bank').search(
            cr, uid, [('partner_id', '=', rec_id)])
        self.assertTrue(bk_ids)

        random.shuffle(bk_ids)  # for good measure
        self.assertRecord(model, rec_id, dict(bank_ids=set(bk_ids)),
                          list_to_set=True)
        self.assertRaises(AssertionError, self.assertRecord,
                          model, rec_id, dict(bank_id=set(bk_ids[1:])),
                          list_to_set=True)

    def test_searchUnique(self):
        for model in (self.model, 'res.partner'):
            self.assertEqual(
                self.searchUnique(model, [('name', '=', 'Assertor')]),
                self.rec_id)

    def test_readUnique(self):
        for model in (self.model, 'res.partner'):
            r = self.readUnique(model, [('name', '=', 'Assertor')])
            self.assertEqual(r['id'], self.rec_id)
            self.assertEqual(r['name'], 'Assertor')
