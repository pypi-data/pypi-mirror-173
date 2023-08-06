# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import attr


@attr.define(frozen=True)
class GitLabObjectHandle:
    """A lightweight object specifier.

    It is much smaller than a full python-gitlab object and is purely
    descriptive.
    """
    type: str
    """The object type.

    In general, this is the singular form, in lower case.
    Current supported types are ``project`` and ``group``.
    """
    id: int
    """The object numeric id."""

    def __str__(self):
        """Nice representation for logging etc.

        The adopted format is similar to the `repr()` of python-gitlab
        objects::

          >>> str(GitLabObjectHandle(type='project', id=87))
          '[Project id:87]'

        Square brackets instead of angled to make the difference visible.
        """
        return f'[{self.type.capitalize()} id:{self.id}]'

    def retrieve(self, api, **extra):
        """Retrieve actual python-gitlab object using the given API.
        """
        return getattr(api, self.type + 's').get(self.id, **extra)

    def traverse(self, api, **extra):
        """Perform the "lazy get of python-gitlab using the given API."""
        return self.retrieve(api, lazy=True, **extra)
