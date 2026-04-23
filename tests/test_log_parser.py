# Android GA Tracking Debugger
# Copyright (c) 2025 Alejandro Reinoso
#
# This software is licensed under the Custom Shared-Profit License (CSPL) v1.0.
# See the LICENSE.txt file for details.

import pytest

from src.log_parser import (
    parse_consent_line,
    parse_logging_event_line,
    parse_user_property_line,
)

# Log line prefix: 18 chars, same convention as logcat (MM-DD HH:MM:SS.mmm)
_LOG_PREFIX = "01-15 10:30:45.123"


def test_parse_logging_event_line_extracts_name_and_params():
    line = (
        f"{_LOG_PREFIX}  1234  5678 I FA: Logging event (FE): "
        "name=view_item, params=Bundle[{item_id=sku1, value=1}]"
    )

    result = parse_logging_event_line(line)
    assert result is not None
    assert result["datetime"] == _LOG_PREFIX
    assert result["name"] == "view_item"
    assert result["params"] == {"item_id": "sku1", "value": "1"}


def test_parse_logging_event_line_returns_none_when_malformed():
    assert parse_logging_event_line("not a real analytics line") is None


def test_parse_user_property_line_standard():
    line = f"{_LOG_PREFIX}  I FA: Setting user property: user_tier, premium"
    result = parse_user_property_line(line)
    assert result is not None
    assert result["name"] == "user_tier"
    assert result["value"] == "premium"


def test_parse_user_property_line_firebase_fe_variant():
    line = f"{_LOG_PREFIX}  I FA: Setting user property (FE): cohort, 2024_q1"
    result = parse_user_property_line(line)
    assert result is not None
    assert result["name"] == "cohort"
    assert result["value"] == "2024_q1"


def test_parse_consent_line_extracts_flags():
    line = (
        f"{_LOG_PREFIX}  I FA:  "
        "Setting storage consent, ad_storage=granted, "
        "analytics_storage=granted, ad_user_data=denied"
    )
    result = parse_consent_line(line)
    assert result is not None
    assert result["ad_storage"] == "granted"
    assert result["analytics_storage"] == "granted"
    assert result["ad_user_data"] == "denied"


def test_parse_consent_line_returns_none_without_storage_keys():
    line = f"{_LOG_PREFIX}  I FA: unrelated message with no=consent"
    assert parse_consent_line(line) is None
