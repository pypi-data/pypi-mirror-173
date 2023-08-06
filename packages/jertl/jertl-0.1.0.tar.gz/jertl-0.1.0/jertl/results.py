from jertl.engine.construct import construct

class Bindings:
    """Base class for jertl processing results"""
    def __init__(self, bindings):
        self._bindings = bindings

    @property
    def bindings(self):
        """
        bindings A dictionary mapping variable identifiers to their bindings

        Returns:
            Dict[str, list | dict | str | Number]: dictionary
                containing a set of variable bindings
        """
        return {k: v for k, v in self._bindings.items() if not k.startswith('$')}


class Match(Bindings):
    """Output of a matcher"""
    def __init__(self, matched, bindings):
        self._matched = matched
        super().__init__(bindings)

    @property
    def matched(self):
        """
        matched The result of filling the structure pattern with the variables bound during the match process

        Returns:
            list | dict | str | Number: Result of a fill using the structure pattern and variable bindings
        """
        return construct(self._matched, self._bindings)


class Transformation(Bindings):
    """Class describing a tranform result"""
    def __init__(self, matched, filled, bindings):
        self._matched = matched
        self._filled  = filled
        super().__init__(bindings)

    @property
    def matched(self):
        """
        matched matching structure with variables replace with their bindings

        Returns:
            list | dict | str | Number: Result of a fill using the matching structure pattern and variable bindings
        """
        return construct(self._matched, self._bindings)

    @property
    def filled(self):
        """
        filled transformed structure

        Returns:
            list | dict | str | Number: Result of a fill using the target structure pattern and variable bindings
        """
        return construct(self._filled, self._bindings)


class Collation(Bindings):
    """Output of a collator"""
    def __init__(self, matchers, bindings):
        self._matchers = matchers
        super().__init__(bindings)

    @property
    def matches(self):
        """
        matches The result of filling the targetted match structures with the variables bound during the match process

        Returns:
            Dict[str, list | dict | str | Number]: Mapping of target identifiers to filled matching structures
        """
        return {v: construct(t, self._bindings) for v, t in self._matchers.items()}


class Inference(Bindings):
    """Result yielded by an Inferencer"""
    def __init__(self, matchers, fillers, bindings):
        self._matchers = matchers
        self._fillers  = fillers
        super().__init__(bindings)

    @property
    def matches(self):
        """
        result The result of filling the targetted match structures with the variables bound during the match process

        Returns:
            Dict[str, list | dict | str | Number]: Mapping of variable identifiers to structures
        """
        return {v: construct(t, self._bindings) for v, t in self._matchers.items()}

    @property
    def fills(self):
        """
        result The result of filling the targetting fill structures with the variables bound during the match process

        Returns:
            Dict[str, list | dict | str | Number]: Mapping of variable identifiers to structures
        """
        return {v: construct(t, self._bindings) for v, t in self._fillers.items()}
