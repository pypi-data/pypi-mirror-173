# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from datetime import (  # noqa: F401 some are used in doctests only
    datetime,
    timezone,
    timedelta,
)


def dt_to_api(dt: datetime):
    """Convert an incoming datetime object to the string format of the API.

    The expected format is just iso-8601. This helper function makes sure
    that timezone information is present by resolving "naive" class:`datetime`
    objects as being UTC.

    As GitLab API often provides ISO-8601 with the `Z` token to mean UTC,
    we do the same.

    TODO consider as an alternative to raise ValueError from the onset.
    could be especially useful when we give importers a dry-run mode.

    >>> dt_to_api(datetime(2002, 4, 7, 11, 20, 0))
    '2002-04-07T11:20:00Z'
    >>> dt_to_api(datetime(2002, 4, 7, 11, 20, 0,
    ...     tzinfo=timezone(timedelta(hours=2))))
    '2002-04-07T11:20:00+02:00'
    """
    if dt.tzinfo is None:
        return dt.isoformat() + 'Z'
    return dt.isoformat()


def api_to_dt(iso: str):
    """Convert, understanding the 'Z' token of ISO 8601.

    >>> api_to_dt('2003-04-07T11:20:00Z')
    datetime.datetime(2003, 4, 7, 11, 20, tzinfo=datetime.timezone.utc)
    """
    if iso.endswith('Z'):
        iso = iso[:-1] + '+00:00'
    return datetime.fromisoformat(iso)
