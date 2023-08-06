class Dict2Obj(object):
    # ----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

    # ----------------------------------------------------------------------

    def __repr__(self):
        """"""
        return "<Dict2Obj: %s>" % self.__dict__
