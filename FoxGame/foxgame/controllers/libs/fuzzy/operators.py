

def hedge(modifier):
    """
    Hedges are devices commonly used to weaken or strengthen
    the impact of a statement.
    """

    @wraps(hedge)
    def modify(set):
        return FuzzySet(set.parent, '%s_%s' %(modifier.func_name, set.name),
                        set.range, mfunct=lambda x : modifier(set.mfunct(x)))
    return modify


