"""High level OpenERP assertions and helpers."""


class OpenErpAssertions(object):
    """Mixin class providing assertion and helper methods to write tests.

    Some of these methods will make less sense with the new API scheduled for
    OpenERP 8, we'll provide them as simple wrappers for backwards compat then.
    """

    def _model_inst(self, model):
        return self.registry(model) if isinstance(model, basestring) else model

    def searchUnique(self, model, domain, **kw):
        """Search, assert that there's exactly one result, return its id.

        :model: can be either a string (model name) or a model instance
        :domain: domain to perform the search with
        :kw: any additional keyword (e.g., ``context``) is passed both
             to search or read.
        """
        model = self._model_inst(model)
        ids = model.search(self.cr, self.uid, domain, **kw)
        self.assertEquals(len(ids), 1,
                          msg="Domain %r on model %r should give "
                          "exactly one record "
                          "(got %d)" % (domain, model, len(ids)))
        return ids[0]

    def readUnique(self, model, domain, load='_classic_write', **kw):
        """Fetch a record by domain, assert unicity, return a read.

        :model: can be either a string (model name) or a model instance
        :load: directly passed to the underlying ``read`` call.
        :kw: any additional keyword (e.g., ``context``) is passed both
             to search or read.
        """
        model = self._model_inst(model)
        rec_id = self.searchUnique(model, domain, **kw)

        return model.read(self.cr, self.uid, rec_id, load=load, **kw)

    def assertRecord(self, model, rec_id, vals, list_to_set=False, **kw):
        """Fetch and compare a record with the provided values dict.

        This saves a LOT of typing and makes assertion much easier to read
        while avoiding a browse.

        :model: can be either a string (model name) or a model instance
        :rec_id: numeric id of the record to check
        :vals: ``dict`` of expected values. For ``many2one`` fields, just pass
               the expected numeric id.
        :list_to_set: if ``True``, all ``list`` instances in the read record
                      will be converted to ``set`` prior tocomparison
        :kw: any additional keyword arguments are passed on to the underlying
             call(s) of ``assertEqual``.

        Examples:

         - if you already have the model obj as ``users_model``::

             self.assertRecord(users_model, 1, dict(name='Administrator'))

         - in general::

             self.assertRecord('res.users', 1, dict(name='Administrator',
                                                    partner_id=1))
        """
        def normalize(v):
            if list_to_set and isinstance(v, list):
                return set(v)
            return v

        read = self._model_inst(model).read(self.cr, self.uid, rec_id,
                                            vals.keys(), load='_classic_write')
        if isinstance(read, (list, tuple)):
            # happens for some models (seen w/ ir.attachment)
            self.assertEqual(len(read), 1,
                             msg="read() returned a list whose "
                             "length is %d (should be 1)" % len(read))
            read = read[0]

        as_dict = dict((k, normalize(v))
                       for k, v in read.iteritems()
                       if k in vals)
        self.assertEqual(as_dict, vals, **kw)

    def assertUniqueWithValues(self, model, domain, values, list_to_set=False,
                               context=None, **kw):
        """Combine :meth:`searchUnique` and :meth:`assertRecord`.

        :return: id of (unique) record matching domain
        """
        rec_id = self.searchUnique(model, domain, context=context)
        self.assertRecord(model, rec_id, values, list_to_set=list_to_set, **kw)
        return rec_id

    def assertNoRecord(self, model, domain, context=None, msg=None):
        """Assert that the given domain gives 0 results on prescribed model.

        :param model: a :class:``osv.Model`` instance or a model name
        :param domain: a standard OpenERP domain
        :param context: optional OpenERP context
        :param msg: same meaning as for :meth:assertEqual
        """
        return self.assertEqual(
            len(self._model_inst(model).search(self.cr, self.uid,
                                               domain, context=context)),
            0, msg=msg)
