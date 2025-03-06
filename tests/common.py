class Hook:
    def __init__(self, ref=None):
        self.ref = ref


HOOK_CLASS_FULLNAME = Hook.__module__ + '.' + Hook.__name__
