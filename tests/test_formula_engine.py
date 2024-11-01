# -*- coding: UTF-8 -*-
"""Tests for module formula_engine
"""

import pytest

from batpy.formula_engine import (
    FormulaRuntimeError,
    FormulaSyntaxError,
    _byte_offset_to_char_offset,
    evaluate_formula,
)


@pytest.mark.parametrize(
    "formula_without_error, vars_without_error, expected_evaluation",
    [
        ("42", None, 42.0),
        ("-42", None, -42.0),
        ("42.0", {}, 42.0),
        ("42e-1", {}, 42e-1),
        ("1 + 2 * (3.0 / 4.0) - 0.5 + 40", {}, 42.0),
        ("a * b / c", {"a": 1274, "b": 3, "c": 91}, 42.0),
    ],
)
def test_evaluate_formula(
    formula_without_error, vars_without_error, expected_evaluation
):
    """Test evaluate_formula

    Parameters
    ----------
    formula_without_error : _type_
        Formulas to evaluate, which will result in no error
    vars_without_error : _type_
        Variables and their values, which will result in no error
    expected_evaluation : _type_
        Result of the formula evaluation
    """
    assert (
        evaluate_formula(formula_without_error, vars_without_error)
        == expected_evaluation
    )


@pytest.mark.parametrize(
    "formula_with_error, vars_with_error, expected_error",
    [
        ("''", {}, FormulaSyntaxError),
        ("1 ** 42", {}, FormulaSyntaxError),
        ("1 // 42", {}, FormulaSyntaxError),
        ("not 42", {}, FormulaSyntaxError),
        ("und", {}, FormulaSyntaxError),
        ("and and", {}, FormulaSyntaxError),
        ("f(42)", {}, FormulaSyntaxError),
        ("42" * 1025, {}, FormulaSyntaxError),
        ("lambda a:" * 4242, {}, FormulaSyntaxError),
        ("42/0", {}, FormulaRuntimeError),
    ],
)
def test_evaluate_formula_raise_error(
    formula_with_error, vars_with_error, expected_error
):
    """Test evaluate_formula, which will result in an error

    Parameters
    ----------
    formula_with_error : _type_
        Formulas to evaluate, which will result in an error
    vars_with_error : _type_
        Variables and their values, which will result in no error
    expected_error : _type_
        Expected error type
    """
    with pytest.raises(expected_error):
        assert evaluate_formula(formula_with_error, vars_with_error)


def test_formula_syntax_error_string():
    """Test FormulaSyntaxError string representation"""
    error = FormulaSyntaxError("42", 42, 42)
    assert str(error) == f"{error.lineno}:{error.offset}: {error.msg}"


def test_byte_offset_to_char_offset():
    """Test _byte_offset_to_char_offset"""
    assert _byte_offset_to_char_offset("\x81", 1) == 0
