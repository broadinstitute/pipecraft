"""Node module."""

from abc import ABC
from enum import Enum
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel


class NodeType(Enum):
    """An enumeration of node types.

    The following values are supported:

    * PyFunction: a Python function node
    * InvokeShell: an invoke shell command node
    * Container: a container node
    * Scatter: a scatter node for parallel execution
    * Gather: a gather node for parallel execution

    Examples
    --------
    >>> NodeType.PyFunction
    <NodeType.PyFunction: 'PyFunction'>

    """

    PyFunction = "PyFunction"
    InvokeShell = "InvokeShell"
    Container = "Container"
    Scatter = "Scatter"
    Gather = "Gather"


class Node(ABC):
    """An abstract base class for nodes in the pipeline.

    Attributes
    ----------
    name : str
        The unique name of this node.
    node_type : NodeType
        The type of this node.
    input_paths : list[str]
        A list of paths that are used as inputs to this node.
    output_paths : list[str]
        A list of paths that are produced by this node.
    config : object
        The configuration associated with this node.

    Examples
    --------
    >>> class CustomNode(Node):
    ...     @property
    ...     def name(self) -> str:
    ...         return "CustomNode"
    ...     # ...
    >>> node = CustomNode()
    >>> node.name
    'CustomNode'

    """

    def __init__(
        self, name: str, input_paths: list[str], output_paths: list[str], config: object
    ) -> None:
        """Abstract base class for nodes in the pipeline.

        Attributes
        ----------
        name : str
            The unique name of this node.
        node_type : NodeType
            The type of this node.
        input_paths : list[str]
            A list of paths that are used as inputs to this node.
        output_paths : list[str]
            A list of paths that are produced by this node.
        config : object
            The configuration associated with this node.

        """
        self.name = name
        self.input_paths = input_paths
        self.output_paths = output_paths
        self.config = config
        self.node_type = None


class PyFunctionConfig(BaseModel):
    """Configuration for a Python function node.

    Attributes
    ----------
    py_object : object
        The Python object associated with this configuration.
    venv : Path
        The path to the virtual environment used by this configuration.

    Examples
    --------
    >>> config = PyFunctionConfig(py_object={}, venv=Path())
    >>> config.py_object
    {}

    """

    py_object: object
    venv: Path


# Generic Nodes


class PyFunction(Node):
    """Node that represents a Python function."""

    def __init__(
        self,
        name: str,
        input_paths: list[str],
        output_paths: list[str],
        config: PyFunctionConfig | None = None,
    ) -> None:
        """Node that represents a Python function.

        Attributes
        ----------
        name : str
            The unique name of this node.
        input_paths : list[str]
            A list of paths that are used as inputs to this node.
        output_paths : list[str]
            A list of paths that are produced by this node.
        config : PyFunctionConfig | None
            The configuration associated with this node.

        Examples
        --------
        >>> node = PyFunction(name="my_node", input_paths=[], output_paths=[])
        >>> node.name
        'my_node'

        """
        super().__init__(name, input_paths, output_paths, config)
        self.node_type = NodeType.PyFunction
        if config is None:
            self.config = PyFunctionConfig(py_object={}, venv=Path())

    def __repr__(self) -> str:
        """Node representation."""
        return f"{self.name}(PF)"


class InvokeShell(Node):
    """Node that represents an invoke shell command."""

    @property
    def node_type(self) -> NodeType:
        """Node type."""
        return NodeType.InvokeShell


class Container(Node):
    """Node that represents a container."""

    @property
    def node_type(self) -> NodeType:
        """Node type."""
        return NodeType.Container


# Specialized Nodes


class Scatter(Node):
    """Node that represents a scatter operation for parallel execution."""

    def __init__(
        self,
        config: PyFunctionConfig | None = None,
    ) -> None:
        """Node that represents a scatter operation for parallel execution.

        Attributes
        ----------
        name : str
            The unique name of this node.
        input_paths : list[str]
            A list of paths that are used as inputs to this node.
        output_paths : list[str]
            A list of paths that are produced by this node.
        config : PyFunctionConfig | None
            The configuration associated with this node.

        Examples
        --------
        >>> node = Scatter()
        >>> node.name
        'Scatter'

        """
        self.name = f"Scatter:{uuid4()}"
        super().__init__(self.name, [], [], config)
        self.node_type = NodeType.Scatter
        self.config = PyFunctionConfig(py_object={}, venv=Path())

    def __repr__(self) -> str:
        """Node representation."""
        return "Scatter"


class Gather(Node):
    """Node that represents a gather operation for parallel execution."""

    def __init__(
        self,
        config: PyFunctionConfig | None = None,
    ) -> None:
        """Node that represents a gather operation for parallel execution.

        Attributes
        ----------
        name : str
            The unique name of this node.
        input_paths : list[str]
            A list of paths that are used as inputs to this node.
        output_paths : list[str]
            A list of paths that are produced by this node.
        config : PyFunctionConfig | None
            The configuration associated with this node.

        Examples
        --------
        >>> node = Gather()
        >>> node.name
        'Gather'

        """
        self.name = f"Gather:{uuid4()}"
        super().__init__(self.name, [], [], config)
        if config is None:
            self.config = PyFunctionConfig(py_object={}, venv=Path())

    def __repr__(self) -> str:
        """Node representation."""
        return "Gather"