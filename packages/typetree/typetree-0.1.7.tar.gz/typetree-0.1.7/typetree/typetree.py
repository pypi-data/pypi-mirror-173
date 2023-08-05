# -*- coding: utf-8 -*-
"""Object type tree analyzer. The GUI is handled by a separate module."""

import dataclasses
import enum
import functools
import json
import re

from collections.abc import Callable
from typing import Any, Type

try:
    from viewer import tree_viewer
except (ModuleNotFoundError, ImportError):
    from .viewer import tree_viewer

_DEFAULT_MAX_LINES = 1000
_DEFAULT_MAX_SEARCH = 100_000
_DEFAULT_MAX_DEPTH = 20
_DEFAULT_MAX_BRANCHES = float('inf')

# Pre-compiled format for _KeyType.INDEX and _KeyType.SLICE
_RANGE_REGEX = re.compile(r'^\[(\d+)(?::(\d+))?]$')


@functools.total_ordering
class KeyType(enum.Enum):
    """Node key types.

    Each key will be displayed differently based on their type.
    """

    NONE = 0, 'None'
    """For the root node, which has no key."""

    ATTR = 1, 'Attribute'
    """For object attributes (starts with a dot).

    Examples: .attr, ._protected, .__special__.
    """

    MAP = 2, 'Mapping'
    """For dict-like Mapping keys.

    Examples: ['key'], [datetime.date(1970, 1, 1)].
    """

    INDEX = 3, 'Sequence'
    """For array-like Sequence indices or slices.

    The indices must be consecutive integers.
    Examples: [2], [4:7], [:3], [:].
    """

    SET = 4, 'Collection'
    """For set-like Collections, which have item counters, but no key.

    Example: (×3).
    The path to the item will be set to .copy().pop() for convenience,
    even though not all Collections accept these methods.
    """

    @classmethod
    def path(cls, key_type: 'KeyType', value: Any = None) -> str:
        """Key path from the parent object to the current one."""
        match key_type, value:
            case cls.NONE, None:
                return ''
            case cls.NONE, str(x):
                return x
            case cls.ATTR, _:
                return f'.{value!s}'
            case cls.MAP, _:
                return f'[{value!r}]'
            case cls.SET, int():
                return '.copy().pop()'
            case cls.INDEX, int(x):
                return f'[{x}]'
            case cls.INDEX, None:
                return '[:]'
            case cls.INDEX, (int(x), int(y)):
                if x + 1 == y:
                    return f'[{x}]'
                if x == 0:
                    return f'[:{y}]'
                return f'[{x}:{y}]'
        raise TypeError(f"Invalid key type '{key_type}' or value '{value}'")

    @classmethod
    def str(cls, key_type: 'KeyType', value: Any = None) -> str:
        """Key label to be displayed in the tree view."""
        match key_type, value:
            case cls.NONE, None:
                return ''
            case cls.SET, int(x):
                return '(×{:d}) '.format(x)
            case _:
                return f'{cls.path(key_type, value)}: '

    def __lt__(self, other: 'KeyType'):
        """For sorting. Respect the declaration order."""
        if not isinstance(other, type(self)):
            return TypeError
        return self.value < other.value


@functools.total_ordering
class _NodeKey:
    """Node key for string representation and for sorting."""

    def __init__(self, key_type: KeyType, value: Any = None):
        self._str: str = KeyType.str(key_type, value)
        self._path: str = KeyType.path(key_type, value)
        self._type: KeyType = key_type
        self._counter: int = 1
        if key_type == KeyType.SET:
            if not isinstance(value, int):
                raise TypeError
            self._counter = value
        self._slice: tuple[int, int] | None = None
        if key_type == KeyType.INDEX:
            if isinstance(value, int):
                self._slice = value, value + 1
            else:
                self._slice = value
        # Hash is unique for Sets
        self._hash: int = hash((
            type(self),
            self._type,
            self._slice,
            id(self)*(self._type == KeyType.SET)
        ))

    @property
    def path(self) -> str:
        return self._path

    @property
    def type(self) -> KeyType:
        return self._type

    @property
    def counter(self) -> int:
        return self._counter

    @property
    def slice(self) -> tuple[int, int] | None:
        return self._slice

    def reset_counter(self):
        self._counter = 1
        self._str = KeyType.str(self.type, self._counter)

    def increment_counter(self):
        self._counter += 1
        self._str = KeyType.str(self.type, self._counter)

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        if self._type == other._type == KeyType.SET:
            return False
        return self._str == other._str

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        if self._str == other._str:
            return False
        if self._slice is not None:
            if other._slice is None:
                return self._type < other._type
            return self._slice < other._slice
        if self._type == other._type:
            if self._type == KeyType.SET:
                if self._counter != other._counter:
                    return self._counter < other._counter
                return self._hash < other._hash
            return self._str < other._str
        return self._type < other._type

    def __hash__(self) -> int:
        return self._hash


def get_itself(var: Any) -> Any:
    """Do nothing, return itself."""
    return var


def get_type_name(var: Any) -> str:
    """Return the input's type name."""
    return str(type(var).__name__)


def getattr_maker(attr: str) -> Callable[[Any], Any]:
    """Build a partial `getattr` for a fixed attribute."""
    def attr_get(var: Any, attr_copy: str = attr) -> Any:
        return getattr(var, attr_copy)
    return attr_get


@dataclasses.dataclass(slots=True, frozen=True)
class Template:
    """Default template for configuration properties of :class:`Tree`."""

    items_lookup: Callable[[Any], Any] = get_itself
    type_name_lookup: Callable[[Any], str] = get_type_name
    value_lookup: Callable[[Any], Any] = get_itself
    sort_keys: bool = True
    show_lengths: bool = True
    include_attributes: bool = True
    include_dir: bool = False
    include_protected: bool = False
    include_special: bool = False
    max_search: float = _DEFAULT_MAX_SEARCH
    max_depth: float = _DEFAULT_MAX_DEPTH
    max_branches: float = _DEFAULT_MAX_BRANCHES


@dataclasses.dataclass(slots=True, frozen=True)
class DOM(Template):
    """Template for generating a tree view of DOM etree objects."""

    items_lookup: Callable[[Any], Any] = getattr_maker('childNodes')
    type_name_lookup: Callable[[Any], str] = getattr_maker('nodeName')
    value_lookup: Callable[[Any], Any] = getattr_maker('text')


@dataclasses.dataclass(slots=True, frozen=True)
class HTML(Template):
    """Template for generating a tree view of HTML etree objects."""

    type_name_lookup: Callable[[Any], str] = getattr_maker('tag')
    value_lookup: Callable[[Any], Any] = getattr_maker('text')


@dataclasses.dataclass(slots=True, frozen=True)
class XML(Template):
    """Template for generating a tree view of XML etree objects."""

    type_name_lookup: Callable[[Any], str] = getattr_maker('tag')
    value_lookup: Callable[[Any], Any] = getattr_maker('text')


class _MaxSearchError(Exception):
    """Reached maximum number of nodes to be searched."""

    pass


class _NodeInfo:
    """Non-recursive tree node info."""

    def __init__(self, obj: Any, node_key: _NodeKey, config: Template,
                 nodes_searched: int, ancestors_ids: set[int], depth: int):

        self.key: _NodeKey = node_key
        self.path: str = node_key.path
        self.config: Template = config
        self.nodes_searched: int = nodes_searched
        self.maxed_search: bool = False
        # For displaying an ellipsis indicating possible inner content
        self.maxed_depth: bool = depth >= config.max_depth
        is_infinite_recursion: bool = id(obj) in ancestors_ids

        self.type_name: str
        try:
            self.type_name = self.config.type_name_lookup(obj)
        except AttributeError:
            self.type_name = '?'
        original_var: Any = obj
        obj = self.config.items_lookup(obj)

        # These refer to the contents of Maps or Sequences
        self.items_key_type: KeyType = KeyType.NONE
        self.items_len: int | None = None
        self.update_items_info(obj, original_var)

        self.branches: dict[_NodeKey, Any] = {}
        if not is_infinite_recursion:
            try:
                self.add_branches(obj)
            except _MaxSearchError:
                pass

        self.var_repr: str = f'<{self.type_name}>'
        if is_infinite_recursion:
            self.var_repr = f'<...> {self.var_repr}'
        if self.config.show_lengths and self.items_len is not None:
            self.var_repr = f'{self.var_repr}[{self.items_len}]'

    def update_items_info(self, var: Any, original_var: Any):
        """Check which kind of iterable var is, if any, and update.

        Update `self.items_key_type` and `self.items_len` if needed.
        """
        # Check for Collections
        try:
            var, size = self.get_var_len(var, original_var)
        # If TypeError, var is not a Collection of items
        # Also ignore possible attribute lookup error
        except (TypeError, AttributeError):
            return

        # Check for Mappings
        if self.is_mapping(var):
            self.items_key_type = KeyType.MAP
            self.items_len = size
            return

        # Check for Sequences
        if self.is_sequence(var):
            self.items_key_type = KeyType.INDEX
            self.items_len = size
            return

        # Check for set-like Collections
        if self.is_collection(var):
            self.items_key_type = KeyType.SET
            self.items_len = size

    def get_var_len(self, var: Any, original_var: Any) -> tuple[Any, int]:
        """Check for contents in `var`.

        If no content is found, use the value lookup for tree leaves.
        Return the value and the number of items it contains.
        Raise :exc:`TypeError` if not a Collection.
        """
        size: int = len(var)  # Raises TypeError if not a Collection
        if not size:
            var = self.config.value_lookup(original_var)
            # value_lookup might return itself and var might be empty
            size = len(var)
        if isinstance(var, str | bytes | bytearray):
            raise TypeError
        return var, size

    @staticmethod
    def is_mapping(var: Any) -> bool:
        try:
            # Since Maps are usually also Sequences, the priority is
            # to access the Map items. But if the keys do not match
            # their Sequence values, the priority inverts.
            if (all(key1 == key2 for key1, key2 in zip(var, var.keys()))
                    and all(var[key] == value for key, value in var.items())
                    and len(var) == len(var.keys()) == len(var.items())):
                return True
        except (AttributeError, TypeError, KeyError):
            pass
        return False

    @staticmethod
    def is_sequence(var: Any) -> bool:
        try:
            if all(var[index] == value for index, value in enumerate(var)):
                return True
        except (KeyError, TypeError):
            pass
        return False

    @staticmethod
    def is_collection(var: Any) -> bool:
        try:
            next(iter(var))
        # Unknown type: has len, but is not an iterable. Ignore contents.
        except (TypeError, KeyError):
            return False
        # Is an empty Collection
        except StopIteration:
            pass
        return True

    def add_branches(self, var: Any):
        if self.config.include_attributes and hasattr(var, '__dict__'):
            for key, value in vars(var).items():
                if self.include_attr(key):
                    self.add_branch(KeyType.ATTR, key, value)
        if self.config.include_dir:
            for key in dir(var):
                if self.include_attr(key):
                    try:
                        value = getattr(var, key)
                    except AttributeError:
                        continue
                    self.add_branch(KeyType.ATTR, key, value)
        match self.items_key_type:
            case KeyType.MAP:
                for key, value in var.items():
                    self.add_branch(KeyType.MAP, key, value)
            case KeyType.INDEX:
                for index, value in enumerate(var):
                    self.add_branch(KeyType.INDEX, index, value)
            case KeyType.SET:
                for value in var:
                    self.add_branch(KeyType.SET, 1, value)
        # Success -- do not display ellipsis indicating max depth exceeded
        self.maxed_depth = False

    def add_branch(self, key_type: KeyType, key: Any, value: Any):
        if self.nodes_searched >= self.config.max_search:
            self.maxed_search = True
            if not self.branches:  # empty
                # For displaying an ellipsis indicating possible inner content
                self.maxed_depth = True
            raise _MaxSearchError
        if self.maxed_depth:
            raise _MaxSearchError
        node_key = _NodeKey(key_type, key)
        self.branches[node_key] = value
        self.nodes_searched += 1

    def include_attr(self, key: str) -> bool:
        if key.startswith('__') and key.endswith('__'):
            return self.config.include_special
        if key.startswith('_'):
            return self.config.include_protected
        return True

    def __lt__(self, other):
        if self.key.type == other.key.type == KeyType.SET:
            if self.key.counter != other.key.counter:
                return self.key.counter < other.key.counter
            return self.path < other.path
        return self.key < other.key

    def __str__(self) -> str:
        return f'{self.key}{self.var_repr}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self})'


class _InfoTree:
    """A recursive tree builder of :class:`_NodeInfo`."""

    def __init__(self, obj: Any, node_key: _NodeKey, config: Template,
                 nodes_searched: int, ancestors_ids: set[int], depth: int = 0):
        self.config: Template = config
        self.ancestors_ids: set[int] = ancestors_ids.copy()
        self.depth: int = depth
        self.node_info: _NodeInfo = _NodeInfo(
            obj, node_key, config, nodes_searched, ancestors_ids, self.depth
        )
        self.nodes_searched: int = self.node_info.nodes_searched
        self.ancestors_ids.add(id(obj))
        self.is_complete: bool = not self.node_info.branches
        self.maxed_depth: bool = (bool(self.depth >= config.max_depth
                                       and self.node_info.branches)
                                  or self.node_info.maxed_depth)
        self.has_maxed_depth: bool = self.maxed_depth
        self.branches: list[_InfoTree] = []
        self.updated: bool = False

    def update(self):
        """Recursively call to update the deepest :class:`_InfoTree`."""
        if self.is_complete:
            return
        elif self.updated:
            for info_tree in self.branches:
                info_tree.nodes_searched = self.nodes_searched
                info_tree.update()
                self._update_info_tree(info_tree)
        else:
            self.updated = True
            for key, var in self.node_info.branches.items():
                info_tree: _InfoTree = _InfoTree(
                    var, key, self.config, self.nodes_searched,
                    self.ancestors_ids, self.depth + 1,
                )
                self.branches.append(info_tree)
                self._update_info_tree(info_tree)
        self.is_complete = all(info_tree.is_complete
                               for info_tree in self.branches)

    def _update_info_tree(self, info_tree: '_InfoTree'):
        if info_tree.has_maxed_depth:
            self.has_maxed_depth = True
        if self.nodes_searched == info_tree.nodes_searched:
            info_tree.is_complete = True
        self.nodes_searched = info_tree.nodes_searched


class _SubtreeCreator:
    """Create a :class:`Subtree` instance.

    Used for pre-computing and analysing the branches.
    Needed because Subtree inherits from tuple, which is immutable, and
    the creation process is too complex to be done inside
    :meth:`_SubtreeCreator.__new__`.
    """

    def __init__(self, cls: Type['Subtree'], info_tree: _InfoTree):
        self.config: Template = info_tree.config
        info: _NodeInfo = info_tree.node_info
        node_key: _NodeKey = info.key
        self.all_branches: tuple[Subtree, ...] = tuple(
            Subtree(sub_info_tree) for sub_info_tree in info_tree.branches
        )
        self.group_branches()
        max_branches: int = int(min(float(len(self.all_branches)),
                                    self.config.max_branches))
        overflowed: bool = info.maxed_search or (len(self.all_branches)
                                                 > self.config.max_branches)
        self.subtree: Subtree = tuple.__new__(
            cls, self.all_branches[:max_branches]
        )
        self.subtree._node_key = node_key
        self.subtree._config = self.config
        self.subtree._info = info
        self.subtree._label = str(info)
        self.subtree._overflowed = overflowed
        self.subtree._maxed_depth = info.maxed_depth

    @staticmethod
    def group_to_map(v: list[set[int]]) -> dict[tuple[int, int], int]:
        """Convert groups of index mappings to consecutive range maps.

        Argument `v` is a list of indices grouped in sets that map to
        the same structure in a Sequence tree. Their positions indicate
        where they map to. Example:
            `branches = [A, B, A, A, C, A, B]`
            `unique_branches = [A, B, C]`
            `v = [{0, 2, 3, 5}, {1, 6}, {4}]`
        means that `A` shows in indices `v[0] = {0, 2, 3, 5}`, `B` shows
        in indices `v[1] = {1, 6}`, and `C` shows in `v[2] = {4}`.

        The return value is a dict of sequential ranges of indices
        as keys and their mapping to unique_branches. In the previous
        case it will return `{(0, 1): 0, (1, 2): 1, (2, 4): 0,
        (4, 5): 2, (5, 6): 0, (6, 7): 1}`.
        """
        if not v:
            return {}
        u: dict[tuple[int, int], int] = {}
        for k, s in enumerate(v):
            if not s:
                continue
            sv: list[int] = list(sorted(s))
            su: list[tuple[int, int]] = [(sv[0], sv[0] + 1)]
            for x in sv[1:]:  # type: int
                if x == su[-1][1]:
                    su[-1] = (su[-1][0], x + 1)
                else:
                    su.append((x, x + 1))
            for t in su:  # type: tuple[int, int]
                u[t] = k
        # noinspection PyTypeChecker
        return dict(sorted(u.items()))

    # noinspection PyProtectedMember
    def group_branches(self):
        """Group equivalent branches (with the same type structure)."""
        if not self.all_branches:
            return
        # Group unique consecutive Sequence branches and
        # unique Collection branches
        unique_index_branches: list[Subtree] = []
        index_branch_groups: list[list[Subtree]] = []
        index_key_groups: list[set[int]] = []
        unique_set_branches: list[Subtree] = []
        added_branches: list[Subtree] = []
        for branch in self.all_branches:
            # Process Sequences
            if branch._node_key.type == KeyType.INDEX:
                range_key = range(*branch._node_key.slice)
                try:
                    index = unique_index_branches.index(branch)
                except ValueError:
                    unique_index_branches.append(branch)
                    index_branch_groups.append([branch])
                    index_key_groups.append(set(range_key))
                else:
                    index_branch_groups[index].append(branch)
                    index_key_groups[index].update(range_key)
            # Process Collections
            elif branch._node_key.type == KeyType.SET:
                try:
                    index = unique_set_branches.index(branch)
                except ValueError:
                    branch._node_key.reset_counter()
                    unique_set_branches.append(branch)
                else:
                    unique_set_branches[index]._node_key.increment_counter()
            # Do not group other types
            else:
                added_branches.append(branch)

        # Update node keys
        unique_index_branches = self.update_index_keys(index_branch_groups,
                                                       index_key_groups)
        for branch in unique_set_branches:
            branch._update_key(branch._node_key)

        # Join and sort
        self.all_branches = tuple(
            added_branches + unique_index_branches + unique_set_branches
        )
        self.sort_branches()

    # noinspection PyProtectedMember
    def update_index_keys(self, branch_groups: list[list['Subtree']],
                          key_groups: list[set[int]]) -> list['Subtree']:
        updated_branches: list[Subtree] = []
        for _range, index in self.group_to_map(key_groups).items():
            branch = branch_groups[index].pop()
            if self.config.show_lengths:
                branch._update_key(_NodeKey(KeyType.INDEX, _range))
            else:
                branch._update_key(_NodeKey(KeyType.INDEX, None))
            updated_branches.append(branch)
        return list(sorted(updated_branches, key=lambda x: x.key))

    # noinspection PyProtectedMember
    def sort_branches(self):
        self.all_branches = tuple(sorted(
            self.all_branches,
            key=((lambda x: x._info) if self.config.sort_keys
                 else lambda x: x._node_key._type)
        ))


@functools.total_ordering
class Subtree(tuple):
    """A recursive object tree structure."""

    # Initialized by _SubtreeCreator
    _node_key: _NodeKey
    _config: Template
    _info: _NodeInfo
    _label: str
    _overflowed: bool
    _maxed_depth: bool
    # Initialized by __init__
    _nodes: int
    _hash: int
    _path: str
    _is_expandable: bool

    def __new__(cls, info_tree: _InfoTree):
        """Create an immutable nested subtree."""
        return _SubtreeCreator(cls, info_tree).subtree

    def __init__(self, *_args, **_kwargs):
        """Initialize the remaining subtree attributes."""
        self._update_paths()
        node: Subtree
        self._nodes = len(self) + sum(node._nodes for node in self)
        # Hash is unique if overflowed or max depth reached because
        # the tree is incomplete and equality between incomplete trees
        # cannot be established.
        self._hash = hash((
            self._info.var_repr,
            self._info.key.type,
            id(self)*(self._overflowed or self._maxed_depth),
            tuple(map(hash, self)),
        ))
        self._path = self._node_key.path
        self._update_paths()
        self._is_expandable = bool(self or self._overflowed
                                   or self._maxed_depth)

    @property
    def key(self) -> str:
        """Key path from previous node to the current one."""
        return self._node_key.path

    @property
    def key_type(self) -> KeyType:
        """Return the key type used.

        Can be a Sequence index, a Mapping key, an attribute, a Set
        (empty key), or none (also empty).
        """
        return self._node_key.type

    @property
    def path(self) -> str:
        """Return the key path from the root node to the current one."""
        return self._path

    @property
    def type(self) -> str:
        """Return the type name of the object the node corresponds to."""
        return self._info.type_name

    @property
    def label(self) -> str:
        """Return the full text displayed for the node."""
        return self._label

    @property
    def nodes(self) -> int:
        """Return the number of inner nodes indexed."""
        return self._nodes

    @property
    def config(self) -> Template:
        """Return the settings used for generating the tree."""
        return self._config

    @property
    def is_expandable(self) -> bool:
        """Return a flag for whether the node has inner content.

        If true, the node will show as expandable in the tree view.
        """
        return self._is_expandable

    @property
    def maxed_depth(self) -> bool:
        """Return a flag for maximum depth reached.

        Only evaluate to `True` if the object the node refers to has
        inner content that was not indexed.
        """
        return self._maxed_depth

    @property
    def overflowed(self) -> bool:
        """Return a flag for maximum branch exceeded.

        If `True`, the node has more branches than indexed.
        Might be from reaching either `max_search` or `max_branches`.
        """
        return self._overflowed

    def _update_key(self, new_key: _NodeKey):
        self._node_key = new_key
        self._info.key = new_key
        self._label = str(self._info)
        self._update_paths()

    def _update_paths(self, parent_path: str = ''):
        if self._node_key.type == KeyType.SET:
            self._path = f'{parent_path}.copy().pop()'
        else:
            self._path = f'{parent_path}{self._node_key.path}'
        for branch in self:  # type: Subtree
            branch._update_paths(self._path)

    def _get_tree_lines(self, max_lines: float,
                        root_pad: str = '',
                        branch_pad: str = '') -> list[str]:
        lines: list[str] = [f'{root_pad}{self._label}']
        if self._maxed_depth and self._is_expandable:
            lines.append(f'{branch_pad}└── ...')
            return lines
        if not self:  # empty
            return lines

        end: int = len(self)
        if not self._overflowed:
            end -= 1
        for branch in self[:end]:  # type: Subtree
            lines.extend(branch._get_tree_lines(
                max_lines=max_lines,
                root_pad=f'{branch_pad}├── ',
                branch_pad=f'{branch_pad}│   ',
            ))
        if self._overflowed:
            lines.append(f'{branch_pad}...')
        else:
            last_branch: Subtree = self[-1]
            lines.extend(last_branch._get_tree_lines(
                max_lines=max_lines,
                root_pad=f'{branch_pad}└── ',
                branch_pad=f'{branch_pad}    ',
            ))
        if len(lines) > max_lines:
            del lines[int(max_lines) - 1:]
            lines.append(' ...')
        return lines

    def to_dict(self, max_lines: float) -> str | dict[str, str | dict]:
        """Create a nested dict representing the type tree structure."""
        if not self:  # empty
            return str(self._info)
        branch: Subtree
        return {
            str(branch._info): branch.to_dict(max_lines)
            for branch in self
        }

    def __eq__(self, other: object) -> bool:
        """Compare two subtrees.

        Subtrees containing the same type structure are equivalent,
        except for set-like nodes.
        """
        if not isinstance(other, type(self)):
            raise NotImplementedError
        if self._hash != other._hash:
            return False
        if self._info.var_repr != other._info.var_repr:
            return False
        if self._info.key.type != other._info.key.type:
            return False
        if self._overflowed or self._maxed_depth:
            return False
        return super().__eq__(other)

    def __lt__(self, other: object) -> bool:
        """Compare two subtrees for sorting."""
        if not isinstance(other, type(self)):
            raise NotImplementedError
        if self == other:
            return False
        if self._info.key.type != other._info.key.type:
            if self._info.key.type is None:
                return True
            if other._info.key.type is None:
                return False
            return self._info.key.type < other._info.key.type
        if self._info.var_repr != other._info.var_repr:
            return self._info.var_repr < other._info.var_repr
        if len(self) != len(other):
            return len(self) < len(other)
        for x, y in zip(self, other):
            if x != y:
                return x < y
        return self._hash < other._hash

    def __str__(self) -> str:
        """Return the string representation of the subtree."""
        return f'{self._info!s}{{...}}'

    def __repr__(self) -> str:
        """Return the repr of the subtree."""
        return f'{type(self).__name__}({self!s})'

    def __hash__(self) -> int:
        """Return the hash of the subtree.

        Equivalent (equal) subtrees always evaluate to the same hash.
        """
        return self._hash


class Tree(Subtree):
    """Root node of the type tree representation of a Python object.

    Root-only (:class:`Tree`) attributes:

    :param depth: Maximum depth reached
    :type depth: int
    :param searches: Total number of nodes searches
    :type searches: int

    Inherited (:class:`Subtree`) attributes:

    :param key: Key path from previous node to the current one
    :type key: str
    :param key_type: The key type used. Type `help(KeyType)` for more
        info
    :type key_type: KeyType
    :param path: The key path from the root node to the current one
    :type path: str
    :param type: The type name of the object the node corresponds to
    :type type: str
    :param label: The full text displayed for the node
    :type label: str
    :param nodes: The number of inner nodes indexed
    :type nodes: int
    :param config: The settings used for generating the tree
    :type config: Template
    :param is_expandable: Flag for whether the node has inner content.
        If `True`, the node will show as expandable in the tree view
    :type is_expandable: bool
    :param maxed_depth: Flag for maximum depth reached. If `True`, the
        object the node refers to has inner content that was not indexed
    :type maxed_depth: bool
    :param overflowed: Flag indicating maximum branch exceeded. If
        `True`, the node has more branches than indexed. Might be from
        reaching either `max_search` or `max_branches`
    :type overflowed: bool
    """

    _depth: int
    _searches: int
    max_lines: float

    def __new__(cls, obj: Any, *, key_text: str | None = None,
                max_lines: float = _DEFAULT_MAX_LINES,
                template: Type[Template] = Template, **kwargs):
        """Use breadth-first search to construct a new instance."""
        # Since Tree inherits from tuple, which is immutable, the
        # instance size must be pre-computed before the instance
        # initialization. This process is done recursively with a
        # breadth-first algorithm.

        # noinspection PyArgumentList
        config: Template = template(**kwargs)
        info_tree: _InfoTree = _InfoTree(
            obj, _NodeKey(KeyType.NONE, key_text), config,
            nodes_searched=0, ancestors_ids=set(), depth=0
        )
        depth: int = 0
        while not info_tree.is_complete:
            info_tree.update()
            depth += 1
        tree: Tree = super().__new__(cls, info_tree)
        tree._depth = depth
        tree._searches = info_tree.nodes_searched
        tree.max_lines = max_lines
        return tree

    def __init__(self, obj: Any, **kwargs):
        """Build a recursive object tree structure.

        :param obj: Any Python object to be analysed
        :type obj: Any
        :param key_text: Placeholder text for the root key node.
            Defaults to None
        :type key_text: str, optional
        :param template: A configuration template for common object
            types. Currently supported: `Template` (default), `DOM`,
            `HTML`, and `XML`
        :param items_lookup: Function used to access the node's content.
            Defaults to `lambda var: var`
        :type items_lookup: Callable[[Any], Any], optional
        :param type_name_lookup: Function used to get the type name.
            Defaults to `lambda var: type(var).__name__`
        :type type_name_lookup: Callable[[Any], Any], optional
        :param value_lookup: Function used to get the value when the
            node's content is empty (tree leaves). Defaults to
            `lambda var: var`
        :type value_lookup: Callable[[Any], Any], optional
        :param sort_keys: Flag for sorting keys alphabetically. Defaults
            to `True`
        :type sort_keys: bool, optional
        :param show_lengths: Flag for displaying sizes of iterables.
            This affects how subtrees are grouped together, since
            Sequences of different sizes but same content types are
            considered equivalent. Defaults to `True`
        :type show_lengths: bool, optional
        :param include_attributes: Flag for including the mutable
            attributes returned by `vars()`. Defaults to `True`
        :type include_attributes: bool, optional
        :param include_dir: Flag for including the attributes returned
            by `dir()`, except the protected (`_protected`) and special
            (`__special__`) ones. Defaults to `False`
        :type include_dir: bool, optional
        :param include_protected: Flag for including the protected
            (`_protected`) attributes.  Defaults to `False`
        :type include_protected: bool, optional
        :param include_special`: Flag for including the special
            (`__special__`) attributes.  Defaults to `False`
        :type include_special: bool, optional
        :param max_lines: Maximum number of lines to be printed For the
            GUI, it is the maximum number of rows to be displayed, not
            including the extra ellipsis at the end. Can be disabled by
            setting it to infinity (`float('inf')` or `math.inf`).
            Defaults to 1000
        :type max_lines: float, optional
        :param max_search: Maximum number of nodes searched. Defaults to
            100,000
        :type max_search: float, optional
        :param max_depth: Maximum search depth. Defaults to 20
        :type max_depth: float, optional
        :param max_branches: Maximum number of branches displayed on
            each node. This only applies after grouping. Defaults to
            infinity
        :type max_branches: float, optional
        """
        super().__init__(obj, **kwargs)

    @property
    def depth(self) -> int:
        """Maximum depth reached."""
        return self._depth

    @property
    def searches(self) -> int:
        """Total number of nodes searched."""
        return self._searches

    def to_dict(self, max_lines: float | None = None
                ) -> str | dict[str, str | dict]:
        """Return a nested `dict` representation of the type tree."""
        if max_lines is None:
            max_lines = self.max_lines
        return super().to_dict(max_lines)

    def to_json(self, *args, max_lines: float | None = None, **kwargs) -> str:
        """Return a JSON representation of the type tree."""
        if max_lines is None:
            max_lines = self.max_lines
        return json.dumps(self.to_dict(max_lines), *args, **kwargs)

    def save_as_json(self, file_path: str, *args,
                     max_lines: float | None = None,
                     encoding: str = 'utf-8',
                     ensure_ascii: bool = False,
                     indent: int = 4,
                     **kwargs):
        """Save a JSON representation of the type tree to a file."""
        if max_lines is None:
            max_lines = self.max_lines
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(self.to_dict(max_lines), file, *args,
                      ensure_ascii=ensure_ascii,
                      indent=indent,
                      **kwargs)

    def save_as_text(self, file_path: str, encoding: str = 'utf-8', **kwargs):
        """Save the tree view as a text file."""
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(self.to_string(**kwargs))

    def to_string(self, max_lines: float | None = None,
                  verbose: bool = False) -> str:
        """Get a tree view of the object's type structure as a string.

        :param max_lines: Maximum number of lines to be printed. Can be
            disabled by setting it to infinity
        :type max_lines: float, optional
        :param verbose: Flag for printing extra information before
            printing the tree view. Defaults to False
        :type verbose: bool, optional
        """
        lines: list[str] = []
        if verbose:
            lines.append('Nodes (indexed/searched): '
                         f'{self.nodes}/{self.searches}')
            lines.append(f'Maximum depth: {self.depth}')
        if max_lines is None:
            max_lines = self.max_lines
        lines.extend(self._get_tree_lines(max_lines, ' ', ' '))
        return '\n'.join(lines)

    def print(self, max_lines: float | None = None, verbose: bool = False):
        """Print a tree view of the object's type structure.

        :param max_lines: Maximum number of lines to be printed. Can be
            disabled by setting it to infinity
        :type max_lines: float, optional
        :param verbose: Flag for printing extra information before
            printing the tree view. Defaults to False
        :type verbose: bool, optional
        """
        print(self.to_string(max_lines=max_lines, verbose=verbose))

    def view(self, spawn_thread: bool = True, spawn_process: bool = False,
             max_lines: float | None = None):
        """Show a tree view of the object's type structure in a GUI.

        :param spawn_thread: Run the GUI in a separate thread
        :type spawn_thread: bool
        :param spawn_process: Run the GUI in a separate process
        :type spawn_process: bool
        :param max_lines: Maximum number of rows to be displayed, not
            including the extra ellipsis at the end. Can be disabled by
            setting it to infinity
        """
        if max_lines is None:
            max_lines = self.max_lines
        tree_viewer(self, max_lines,
                    spawn_thread=spawn_thread,
                    spawn_process=spawn_process)


def print_tree(obj: Any, *, max_lines: float | None = None,
               verbose: bool = False, **kwargs):
    """Print a tree view of the object's type structure.

    :param obj: Any Python object to be analysed
    :type obj: Any
    :param max_lines: Maximum number of lines to be printed. Can be
        disabled by setting it to infinity
    :type max_lines: float, optional
    :param verbose: Flag for printing extra information before printing
        the tree view. Defaults to False
    :type verbose: bool, optional
    :param kwargs: Same as :class:`Tree`. Type `help(Tree.__init__)` for
        the full list
    """
    Tree(obj, **kwargs).print(max_lines=max_lines, verbose=verbose)


def view_tree(obj: Any, *,
              spawn_thread: bool = True,
              spawn_process: bool = False,
              **kwargs):
    """Show a tree view of the object's type structure in a GUI.

    :param obj: Any Python object to be analysed
    :type obj: Any
    :param spawn_thread: Run the GUI in a separate thread
    :type spawn_thread: bool
    :param spawn_process: Run the GUI in a separate process
    :type spawn_process: bool
    :param kwargs: Same as :class:`Tree`. Type `help(Tree.__init__)` for
        the full list
    """
    Tree(obj, **kwargs).view(spawn_thread=spawn_thread,
                             spawn_process=spawn_process)
