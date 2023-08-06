# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from attr import define
from datetime import (
    datetime,
    time as dt_time,
    timedelta,
)
import logging
from typing import (
    Optional,
)

from gitlab import Gitlab as GitLabAPI

logger = logging.getLogger(__name__)

# Running hour of GitLab token expiry daily worker
TWO_AM_UTC = dt_time(hour=2)


class GitLabUserError(RuntimeError):
    """Base exception class for cases when an user cannot be leveraged.

    :attr:`args` is a singleton, made of the "username"
    """


class GitLabUserNotFound(GitLabUserError):
    """Raised when search is possible, but user was not found."""


class GitLabUserUnknown(GitLabUserError):
    """Raised when user is not known and search cannot be performed.

    Typically for cases where and admin token is not available.
    """


class GitLabUserNoToken(GitLabUserError):
    """Raised when no token is available for the user.

    Implicitely does not apply to implementations that are able to
    create tokens or to use the `sudo` feature of the GitLab API
    """


@define
class GitLab:
    url: str
    admin_api: Optional[GitLabAPI] = None
    admin_id: Optional[int] = None
    admin_username: Optional[str] = None

    def init_admin(self, token):
        api = self.admin_api = GitLabAPI(self.url, token)
        api.auth()
        self.admin_username = api.user.username
        self.admin_id = api.user.id
        logger.info("GitLab admin API connection checked (username=%r)",
                    self.admin_username)


class GitLabMultipleAPI:
    """Provide API access for GitLab users.

    Abstract base class to clarify the expected methods.

    Depending on implementation, the :attr:`users` attribute is used
    to authenticate or not (perhaps loaded from a file). In any case,
    it is used to carry interesting information about the user and can
    be used by downstream code to store their own interesting information.
    """

    def __init__(self, gitlab, users=None):
        self.gitlab = gitlab
        self.users = {} if users is None else users

    def user_api(self, username, utc_now=None):
        """Return an API connector authenticated as the given user.

        :param username: the "username" in the sens of GitLab, hence the
           login name / nickname, not the full name.
        :param utc_now: useful for tests of concrete classes if token
           expiration is to be taken into account.
        :return: a :class:`GitlabAPI` instance, and the extra parameters to
           pass when using it)
        :raises: GitLabUserError if impossible to act as the given user.
        """
        raise NotImplementedError  # pragma no cover

    def user_id(self, username):
        """Return the numeric id of the given user.

        We may in the future make it the handle used throughout by
        Heptapod API Import, in which case we'll probably have a ``username``
        method instead.
        """
        raise NotImplementedError  # pragma no cover


class GitLabPersonalTokensAPI(GitLabMultipleAPI):
    """Provide API access for GitLab users using Personal Tokens

    The personal tokens are expected to be found in the :attr:`users`
    attribute.

    Warnings can be issued in cases of close token expiration.
    """

    token_renewal_margin = timedelta(days=1)

    def user_api(self, username, utc_now=None):
        """See :meth:`GitlabMultipleAPI.user_api`
        """
        info = self.users.get(username)
        if info is None:
            raise GitLabUserUnknown(username)

        if utc_now is None:
            utc_now = datetime.utcnow()

        auth = info.get('auth')
        if auth is None:
            raise GitLabUserNoToken(username)

        exp = auth.get('token_expiration_date')
        # expiration can be unknown. This is the case of personal tokens.
        # TODO retrieve personal token information, but this can be
        # tricky (need the token name)
        if exp is not None and (exp - utc_now) < self.token_renewal_margin:
            logger.warning(
                "Access token for user %r will expire "
                "soon (in %d minutes).",
                username,
                (auth['token_expiration_date'] - utc_now
                 ).total_seconds() / 60,
            )

        api = info.get('api')
        if api is not None:
            return api, {}

        token = auth.get('token')
        if token is None:
            raise GitLabUserNoToken(username)

        auth['type'] = 'personal-token'
        api = info['api'] = GitLabAPI(self.gitlab.url, token)
        info['id'] = self.gl_current_user_id(api)
        return api, {}

    def user_id(self, username):
        self.user_api(username)
        return self.users[username]['id']

    def gl_current_user_id(self, api):
        """Wrapper method for easy monkey-patching in unit tests."""
        api.auth()
        return api.user.id


class GitLabSudoAPI(GitLabMultipleAPI):
    """Perform actions using the `sudo` feature of the GitLab API.

    The :attr:`gitlab` attribute is expected to be initialized with
    an admin API before any attempt at retrieving a regular user API.
    """

    @property
    def admin_api(self):
        return self.gitlab.admin_api

    def user_api(self, username):
        """Return API object and additional kwargs.

        The additional kwargs have to be used in API calls.
        """
        self.check_load_user(username)
        return self.gitlab.admin_api, dict(sudo=username)

    def user_id(self, username):
        return self.check_load_user(username)['id']

    def check_load_user(self, username):
        info = self.users.get(username)
        if info is not None:
            return info
        return self.load_user(username)

    def load_user(self, username):
        found = self.admin_api.users.list(username=username)
        if not found:
            raise GitLabUserNotFound(username)

        user = found[0]
        user_info = dict(id=user.id, auth=dict(type='sudo'))
        self.users[username] = user_info
        return user_info
