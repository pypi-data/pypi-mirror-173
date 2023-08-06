# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from attr import (
    define,
    Factory,
)
from datetime import datetime
import logging
from typing import (
    Any,
    Callable,
)

from gitlab.const import AccessLevel
from gitlab.exceptions import GitlabGetError

from .api import (
    GitLabMultipleAPI,
)
from .datetime import dt_to_api
from .objects import GitLabObjectHandle
logger = logging.getLogger(__name__)


ACCESS_LEVELS_BY_VALUE = {level.value: name
                          for name, level in AccessLevel.__members__.items()}


@define(slots=False)
class BaseImporter:
    """Abstract class taking care of common concerns

    It encapsulates the :class:`GitLabMultipleAPI` class to manage
    API connections for the relevant GitLab users.

    Concrete importers (issues, merge requests) are supposed to
    subclass this base class, but export/import applicative code is
    supposed to instantiate concrete importers rather than subclass again.

    All applicative notions (users, roles, objects) handled by this class
    and its subclasses supplied in `heptapod_api_import` are relevant to
    GitLab or Heptapod. They have no representation nor awaraness of the
    original system corresponding notions (notably users).
    """

    gitlab_multiple_api: GitLabMultipleAPI
    """Provides GitLab API access as the appropriate users."""

    roles_manager: Callable
    """A function providing the GitLab user for role management of an object.

    It must take a unique argument (a :class:`GitLabObjectHandler` and return
    a username.
    """

    roles_cache: dict = Factory(dict)
    """Used to remember access levels of users

    This spares lots of API calls.

    Keys are :class:`GitLabObjectHandle` instances, values are dicts
    whose keys are usernames and AccessLevel values.

    TODO If memory becomes an issue, we can replace this with an LRU cache.
    """

    comma_lists: Any = ('labels, ')
    """Control payload lists ro serialize as comma-separated strings.

    See :meth:`normalize_payload`.
    """

    @property
    def admin_api(self):
        return self.gitlab_multiple_api.gitlab.admin_api

    def gitlab_user_api(self, *args, **kwargs):
        """See :meth:`GitLabApiManager.user_api`."""
        return self.gitlab_multiple_api.user_api(*args, **kwargs)

    def get_role(self, username, obj: GitLabObjectHandle):
        """Get the role of username on the given Group or Project.

        Inheritance is taken into account.
        """
        cache = self.roles_cache.setdefault(obj, {})
        try:
            return cache[username]
        except KeyError:
            pass

        as_member = self.gl_user_as_member(username, obj)
        role = None if as_member is None else as_member.access_level
        cache[username] = role
        return role

    def gl_user_as_member(self, username, objh: GitLabObjectHandle):
        api, extra = self.gitlab_user_api(self.roles_manager(objh))
        user_id = self.gitlab_multiple_api.user_id(username)

        obj = objh.traverse(api, **extra)
        try:
            # Using `members_all` means that inherited members are included,
            # see, e.g., https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html  # noqa: E501
            as_member = self.gl_members_get(obj.members_all, user_id, **extra)
            return as_member
        except GitlabGetError as exc:
            if exc.response_code != 404:
                raise
            return None

    def gl_members_get(self, obj_members, user_id, **extra):
        """Singled out for testing convenience."""
        return obj_members.get(user_id, **extra)

    def ensure_role(self, username, role, objh: GitLabObjectHandle):
        cache = self.roles_cache.setdefault(objh, {})
        existing_role = cache.get(username)
        if existing_role is not None and existing_role >= role:
            return

        as_member = self.gl_user_as_member(username, objh)
        if as_member is not None and as_member.access_level >= role:
            return

        api, extra = self.gitlab_user_api(self.roles_manager(objh))
        user_id = self.gitlab_multiple_api.user_id(username)
        obj = objh.traverse(api, **extra)
        if as_member is None:
            logger.info("Adding user %s to direct members of %s with "
                        "%s access level", username, objh, role.name)
            obj.members.create(dict(user_id=user_id, access_level=role),
                               **extra)
        else:
            logger.info("Bumping access level of user %r on %s "
                        "from %s to %s", username, objh,
                        ACCESS_LEVELS_BY_VALUE[as_member.access_level],
                        role.name)
            as_direct_member = obj.members.get(user_id, **extra)
            as_direct_member.access_level = role
            as_direct_member.save(**extra)

        cache[username] = role

    def normalize_payload(self, data):
        """Apply frequent conversions.

        - all datetime objects are converted to the expected ISO 8601 format
        - some lists (or tuples) are converted to comma-separated values,
          according to the :attr:`comma_lists` attribute.
        """
        normalized = {}
        for k, v in data.items():
            if isinstance(v, datetime):
                normalized[k] = dt_to_api(v)
            elif k in self.comma_lists:
                # in case of labels, that seem to be already handled by
                # python-gitlab
                normalized[k] = ','.join(v)
            else:
                normalized[k] = v
        return normalized
