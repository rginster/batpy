# -*- coding: UTF-8 -*-
"""Module, which implements formula engine for batpy

    Implementation of batpy's formula evaluator written on top of Python's AST
    package. Idea is based on https://blog.oyam.dev/python-formulas/

    """

import ast
import operator

MAX_FORMULA_LENGTH = 255


def byte_offset_to_char_offset(source: str, byte_offset: int) -> int:
    """Convert byte offset to char offset

    Cuts out all bytes before byte_offset mark and then attempts to count the
    characters in the cut out part.

    Parameters
    ----------
    source : str
        Input string from which a part is to be cut out
    byte_offset : int
        Byte offset marker to cut out all previous bytes

    Returns
    -------
    int
        Counted characters
    """
    while True:
        try:
            pre_source = source.encode()[:byte_offset].decode()
            break
        except UnicodeDecodeError:
            byte_offset -= 1
            continue
    return len(pre_source)


class FormulaError(Exception):
    """Base class for formula engine errors

    Parameters
    ----------
    Exception
        Common base class for all non-exit exceptions.
    """


class FormulaSyntaxError(FormulaError):
    """Class for formula engine errors regarding syntax

    Parameters
    ----------
    FormulaError
        Base class for formula engine errors
    """

    def __init__(self, msg: str, lineno: int, offset: int):
        """Initialize object

        Parameters
        ----------
        msg : str
            Error message
        lineno : int
            Line number in which the error occurs
        offset : int
            Column / character at which the error occurs
        """
        self.msg = msg
        self.lineno = lineno
        self.offset = offset

    @classmethod
    def from_ast_node(
        cls, source: str, node: ast.AST, msg: str
    ) -> "FormulaSyntaxError":
        """Convert AST node's position and use it in the error object

        Parameters
        ----------
        source : str
            Formula to evaluate
        node : ast.AST
            Ast node
        msg : str
            Error message

        Returns
        -------
        FormulaSyntaxError
            Error message whith line number and offset
        """
        lineno = node.lineno
        col_offset = node.col_offset
        offset = byte_offset_to_char_offset(source, col_offset)
        return cls(msg=msg, lineno=lineno, offset=offset + 1)

    @classmethod
    def from_syntax_error(
        cls, error: SyntaxError, msg: str
    ) -> "FormulaSyntaxError":
        """Python's parser errors

        Parameters
        ----------
        error : SyntaxError
            Error type
        msg : str
            Error message

        Returns
        -------
        FormulaSyntaxError
             Error message whith line number and offset
        """
        return cls(
            msg=f"{msg}: {error.msg}", lineno=error.lineno, offset=error.offset
        )

    def __str__(self) -> str:
        """Error string representation

        Returns
        -------
        str
            Error as string
        """
        return f"{self.lineno}:{self.offset}: {self.msg}"


class FormulaRuntimeError(FormulaError):
    """Class for formula engine errors during runtime

    Parameters
    ----------
    FormulaError : _type_
        Base class for formula engine errors
    """


def eval_constant(
    source: str, node: ast.Constant, vars_val: dict[str, any]
) -> float:
    """Evaluate the value of the AST constant node

    Parameters
    ----------
    source : str
        Formula to evaluate
    node : ast.Constant
        Ast node
    vars_val : dict[str, any]
        Variables and their values used to evaluate the function

    Returns
    -------
    float
        Result of the evaluated formula

    Raises
    ------
    FormulaSyntaxError.from_ast_node
        Error, if AST node's formula syntax is wrong
    """
    _ = vars_val
    if isinstance(node.value, (int, float)):
        return float(node.value)
    raise FormulaSyntaxError.from_ast_node(
        source, node, "Literals of this type are not supported"
    )


def eval_name(source: str, node: ast.Name, vars_val: dict[str, any]) -> float:
    """Evaluate the value of the variable (AST name node)

    Parameters
    ----------
    source : str
        Formula to evaluate
    node : ast.Name
        Ast node
    vars_val : dict[str, any]
        Variables and their values used to evaluate the function

    Returns
    -------
    float
        Result of the evaluated formula

    Raises
    ------
    FormulaSyntaxError.from_ast_node
        Error, if AST node's formula syntax is wrong
    """
    try:
        return float(vars_val[node.id])
    except KeyError as exc:
        raise FormulaSyntaxError.from_ast_node(
            source, node, f"Undefined variable: {node.id}"
        ) from exc


def eval_node(source: str, node: ast.AST, vars_val: dict[str, any]) -> float:
    """Evaluate supported AST node

    The eval_node function accepts supported AST nodes and passes the node to a
    more specific function.

    Parameters
    ----------
    source : str
        Formula to evaluate
    node : ast.AST
        Ast node
    vars_val : dict[str, any]
        Variables and their values used to evaluate the function

    Returns
    -------
    float
        Result of the evaluated formula

    Raises
    ------
    FormulaSyntaxError.from_ast_node
        Error, if AST node's formula syntax is wrong
    """
    supported_evaluators = {
        ast.Expression: eval_expression,
        ast.Constant: eval_constant,
        ast.Name: eval_name,
        ast.BinOp: eval_binop,
        ast.UnaryOp: eval_unaryop,
    }

    for ast_type, evaluator in supported_evaluators.items():
        if isinstance(node, ast_type):
            return evaluator(source, node, vars_val)

    raise FormulaSyntaxError.from_ast_node(
        source, node, "This syntax is not supported"
    )


def evaluate_formula(formula: str, vars_val: dict[str, any] = None) -> float:
    """Evaluate formula from string

    Parameters
    ----------
    formula : str
        Formula to evaluate
    vars_val : dict[str, any], optional
        Variables and their values used to evaluate the function,
        by default None

    Returns
    -------
    float
        Result of the evaluated formula

    Raises
    ------
    FormulaSyntaxError
        Error, if formula syntax is wrong
    FormulaSyntaxError.from_syntax_error
        Error, if formula could not be parsed
    FormulaRuntimeError
        Error, if exception occurs during runtime

    Examples
    --------
    >>> evaluate_formula("a + b * 2", {"a": 2, "b": 20})
    42
    """
    if vars_val is None:
        vars_val = {}
    if len(formula) > MAX_FORMULA_LENGTH:
        raise FormulaSyntaxError(
            f"The formula is too long: {len(formula)} > {MAX_FORMULA_LENGTH}",
            1,
            1,
        )

    try:
        node = ast.parse(formula, "<string>", mode="eval")
    except SyntaxError as error:
        raise FormulaSyntaxError.from_syntax_error(error, "Could not parse")

    try:
        return eval_node(formula, node, vars_val)
    except FormulaSyntaxError:
        raise
    except Exception as error:
        raise FormulaRuntimeError(f"Evaluation failed: {error}") from error


def eval_expression(
    source: str, node: ast.Expression, vars_val: dict[str, any]
) -> float:
    """Evaluate top level AST node

    Parameters
    ----------
    source : str
        Formula to evaluate
    node : ast.AST
        Ast node
    vars_val : dict[str, any]
        Variables and their values used to evaluate the function

    Returns
    -------
    float
        Result of the evaluated formula
    """
    return eval_node(source, node.body, vars_val)


def eval_binop(
    source: str, node: ast.BinOp, vars_val: dict[str, any]
) -> float:
    """Evaluate binary operations from AST node

    Evaluate the left and the right operands using eval_node and then apply
    the binary operation over their values.

    Parameters
    ----------
    source : str
        Formula to evaluate
    node : ast.BinOp
        Ast node
    vars_val : dict[str, any]
        Variables and their values used to evaluate the function

    Returns
    -------
    float
        Result of the evaluated formula

    Raises
    ------
    FormulaSyntaxError.from_ast_node
        Error, if AST node's formula syntax is wrong
    """
    supported_operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    left_value = eval_node(source, node.left, vars_val)
    right_value = eval_node(source, node.right, vars_val)

    try:
        apply = supported_operations[type(node.op)]
    except KeyError as exc:
        raise FormulaSyntaxError.from_ast_node(
            source, node, "Operations of this type are not supported"
        ) from exc

    return apply(left_value, right_value)


def eval_unaryop(
    source: str, node: ast.UnaryOp, vars_val: dict[str, any]
) -> float:
    """Evaluate unary operations from AST node

    Parameters
    ----------
    source : str
        Formula to evaluate
    node : ast.UnaryOp
        Ast node
    vars_val : dict[str, any]
        Variables and their values used to evaluate the function

    Returns
    -------
    float
        Result of the evaluated formula

    Raises
    ------
    FormulaSyntaxError.from_ast_node
        Error, if AST node's formula syntax is wrong
    """
    supported_operations = {
        ast.USub: operator.neg,
    }

    operand_value = eval_node(source, node.operand, vars_val)

    try:
        apply = supported_operations[type(node.op)]
    except KeyError as exc:
        raise FormulaSyntaxError.from_ast_node(
            source, node, "Operations of this type are not supported"
        ) from exc

    return apply(operand_value)
