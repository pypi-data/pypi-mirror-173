import jertl.ast.emitter as jae
import jertl.ast.builder as jab

from jertl.engine.interpreter import Interpreter
from jertl.engine.construct   import construct

from jertl.results import Match, Transformation, Collation, Inference

class Matcher:
    """Class which compares data to a structure and returns all Matches"""
    def __init__(self, structure):
        """
        Args:
            structure (str): pattern describing structure to be identified
        """
        self._ast          = jab.ast_for_string(structure, 'structure')
        self._instructions = list(jae.emit_match(self._ast))

    def match_all(self, data):
        """match_all Generate all Matches of a structure to data.

        Args:
            data ((Sequence | Mapping | Number)): Python data structure
                to examine

        Yields:
            :obj:`~.Match`: All possible Matches

        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(data):
            yield Match(self._ast, bindings)

    def match(self, data):
        """match Matches a structure to data.

        Args:
            data ((Sequence | Mapping | Number)): Python data structure to match

        Returns:
            Optional(:obj:`~.Match`): (Sequence | Mapping | Number)
        """
        for m in self.match_all(data):
            return m


class Filler:
    """Class which performs fills"""
    def __init__(self, structure):
        """
        Args:
            structure (str): pattern describing structure to be used for creating new data
        """
        self._ast = jab.ast_for_string(structure, 'structure')

    def fill(self, **bindings):
        """fill Fills structure and returns data with structure variables replaced with their bindings

        Args:
            **bindings (Dict[str, list | dict | str | Number]): Initial variable bindings

        Returns:
            (list | dict | str | Number): data
        """
        return construct(self._ast, bindings)


class Transformer:
    """A transformer with compile structure"""
    def __init__(self, transform):
        """
        Args:
            transform (str): pattern describing a transform
        """
        self._ast = jab.ast_for_string(transform, 'transform')
        self._source = self._ast.input
        self._target = self._ast.output
        self._instructions = list(jae.emit_match(self._source))

    def transform_all(self, data):
        """transform_all finds all possible transforms of data

        Args:
            data ((list | dict | str | Number)): Data structure to be
                transformed

        Yields:
            :obj:`~.Transformation`:  All possible transforms of the sources

        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(data):
            yield Transformation(self._source, self._target, bindings)

    def transform(self, data):
        """transform Finds a transform of data

        Args:
            data ((list | dict | str | Number)): Data structure to be
                transformed

        Returns:
            Optional(:obj:`~.Transformer`):: A Transformation if one was found

        """
        for m in self.transform_all(data):
            return m


class Collator:
    """Class which performs collations"""
    def __init__(self, collation):
        """
        Args:
            collation (str): pattern describing a collation

        """
        self._ast = jab.ast_for_string(collation, 'collation')
        self._toplevel = {m.variable.identifier for m in self._ast}
        self._instructions = list(jae.emit_collation(self._ast, self._toplevel))

    def collate_all(self, **bindings):
        """collate_all Yield all possible collations of data

        Args:
            **bindings (Dict[str, list | dict | str | Number]): Initial variable bindings

        Yields:
            :obj:`~.Collation`: All possible collations

        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(None, bindings):
            structures = {m.variable.identifier: m.structure for m in self._ast}
            yield Collation(structures, bindings)

    def collate(self, **bindings):
        """collate Find a collation if any

        Args:
            **bindings (Dict[str, list | dict | str | Number]): Initial variable bindings

        Returns:
            Optional(:obj:`Collation`): A Collation

        """
        for m in self.collate_all(**bindings):
            return m


class Rule:
    """Class which finds inferences of a production rule"""
    def __init__(self, rule):
        """
        Args:
            rule (str): pattern describing an inference rule
        """
        self._ast = jab.ast_for_string(rule, 'rule_')
        self._toplevel = {m.variable.identifier for m in self._ast.matchers}
        self._instructions = list(jae.emit_collation(self._ast.matchers, self._toplevel))

    def infer_all(self, **bindings):
        """infer_all Yield all possible inferences of rule applied to data

        Args:
            **bindings (Dict[str, list | dict | str | Number]): Initial variable bindings

        Yields:
            :obj:`~.Inference`: All possible inferences

        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(None, bindings):
            inputs  = {m.variable.identifier: m.structure for m in self._ast.matchers}
            outputs = {a.variable.identifier: a.structure for a in self._ast.setters}
            yield Inference(inputs, outputs, bindings)

    def infer(self, **bindings):
        """infer Finds an inference of rule applied to data (if any)

        Args:
            **bindings (Dict[str, list | dict | str | Number]): Initial variable bindings

        Returns:
            Optional(:obj:`~.Inference`): An inference

        """
        for m in self.infer_all(**bindings):
            return m


__all__ = ['Matcher', 'Filler', 'Transformer', 'Collator', 'Rule']
