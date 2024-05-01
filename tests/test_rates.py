"""Description

Test module for the rates applying functions of the lib_optimization library."""

# flake8: noqa: F811, F401

import os
import sys
import copy
import numpy as np
import pulp as pulp

from BatchMonitor import Batch

from BatchMonitor.lib_optimization import (
    _apply_rates,
    _customs_duty,
    _exchange_rate,
    _taxe_rate,
    _transport_fee,
)

from .fixture_optimization import Batch_list_fixture

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_exchange_rate(Batch_list_fixture):
    """Test of the _exchange_rate function"""
    Batch_list_fixture_float = copy.deepcopy(Batch_list_fixture)
    waited = [
        Batch.from_str("batch 1:12; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:20; 6xapple, 7xbanana, 7xorange"),
    ]

    batch_list = _exchange_rate(Batch_list_fixture, rate=np.array([1.2, 2, 1]))

    assert np.all(batch_list == waited)

    waited_float = [
        Batch.from_str("batch 1:20; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:40; 6xapple, 7xbanana, 7xorange"),
    ]
    batch_list_float = _exchange_rate(Batch_list_fixture_float, rate=2)

    assert np.all(batch_list_float == waited_float)


def test_taxe_rate(Batch_list_fixture):
    """Test of the _taxe_rate function"""
    Batch_list_fixture_float = copy.deepcopy(Batch_list_fixture)
    waited = [
        Batch.from_str("batch 1:12; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:20; 6xapple, 7xbanana, 7xorange"),
    ]

    batch_list = _taxe_rate(Batch_list_fixture, rate=np.array([0.2, 1, 0]))

    assert np.all(batch_list == waited)

    waited_float = [
        Batch.from_str("batch 1:20; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:40; 6xapple, 7xbanana, 7xorange"),
    ]
    batch_list_float = _taxe_rate(Batch_list_fixture_float, rate=1)

    assert np.all(batch_list_float == waited_float)


def test_customs_duty(Batch_list_fixture):
    """Test of the _customs_duty function"""
    Batch_list_fixture_float = copy.deepcopy(Batch_list_fixture)
    waited = [
        Batch.from_str("batch 1:12; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:20; 6xapple, 7xbanana, 7xorange"),
    ]

    batch_list = _customs_duty(Batch_list_fixture, rate=np.array([0.2, 1, 0]))

    assert np.all(batch_list == waited)

    waited_float = [
        Batch.from_str("batch 1:20; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:40; 6xapple, 7xbanana, 7xorange"),
    ]
    batch_list_float = _customs_duty(Batch_list_fixture_float, rate=1)

    assert np.all(batch_list_float == waited_float)


def test_transport_fee(Batch_list_fixture):
    """Test of the _transport_fee function"""
    Batch_list_fixture_float = copy.deepcopy(Batch_list_fixture)
    waited = [
        Batch.from_str("batch 1:12; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:20; 6xapple, 7xbanana, 7xorange"),
    ]

    batch_list = _transport_fee(Batch_list_fixture, rate=np.array([0.2, 1, 0]))

    assert np.all(batch_list == waited)

    waited_float = [
        Batch.from_str("batch 1:20; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:30; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:40; 6xapple, 7xbanana, 7xorange"),
    ]
    batch_list_float = _transport_fee(Batch_list_fixture_float, rate=1)

    assert np.all(batch_list_float == waited_float)


def test_apply_rates(Batch_list_fixture):
    """Test of the _apply_rates function"""
    Batch_list_fixture_float = copy.deepcopy(Batch_list_fixture)
    waited = [
        Batch.from_str("batch 1:20.735999999999997; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:240; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:20.0; 6xapple, 7xbanana, 7xorange"),
    ]

    batch_list = _apply_rates(
        Batch_list_fixture,
        customs_duty=np.array([0.2, 1, 0]),
        exchange_rate=np.array([1.2, 2, 1]),
        tax_rate=np.array([0.2, 1, 0]),
        transport_fee=np.array([0.2, 1, 0]),
    )

    assert np.all(batch_list == waited)

    waited_float = [
        Batch.from_str("batch 1:160; 3xapple, 2xbanana, 4xorange"),
        Batch.from_str("batch 2:240; 5xapple, 5xbanana, 5xorange"),
        Batch.from_str("batch 3:320; 6xapple, 7xbanana, 7xorange"),
    ]

    batch_list_float = _apply_rates(
        Batch_list_fixture_float,
        customs_duty=1,
        exchange_rate=2,
        tax_rate=1,
        transport_fee=1,
    )

    assert np.all(batch_list_float == waited_float)
