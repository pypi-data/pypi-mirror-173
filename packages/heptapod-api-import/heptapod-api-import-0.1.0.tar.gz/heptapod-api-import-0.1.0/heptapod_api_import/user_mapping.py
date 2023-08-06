# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import attr
import logging
import re

from typing import (
    Optional,
    Callable,
)
from gitlab.const import SearchScope
from gitlab.exceptions import (
    GitlabCreateError,
)
from .api import GitLabAPI
from .datetime import dt_to_api

logger = logging.getLogger(__name__)


class IdentityMapping:

    def get(self, k):
        return k


GITLAB_USERNAME_BASE_RX = re.compile(r'^\w+$')
GITLAB_USERNAME_FORBIDDEN_SUFFIXES = ('.', '.git', '.atom')
# hyphen in Python regexps character sets need no escaping if first or last:
GITLAB_USERNAME_FORBIDDEN_CHARS_RX = re.compile(r'[^a-zA-Z0-9_.-]')
EMAIL_AT_AND_FOLLOWING_RX = re.compile(r'@.*$')
LEADING_HYPHENS_RX = re.compile(r'^-+')
DECIMAL_NUMBER_RX = re.compile(r'^\d+')


def is_valid_username(username):
    """Tell wheteher the username respects GitLab standards.

    # From warnings emitted by GitLab API:
    # 'username': ["can contain only letters, digits, '_', '-' and '.'.
    # Cannot start with '-' or end in '.', '.git' or '.atom'."]}

    >>> is_valid_username('someone@something')
    False
    >>> is_valid_username('-foo')
    False
    >>> is_valid_username('some-foo_bar')
    True
    >>> is_valid_username('gitlab.git')
    False
    """
    return (GITLAB_USERNAME_FORBIDDEN_CHARS_RX.search(username) is None
            and not username.startswith('-')
            and not any(username.endswith(suffix)
                        for suffix in GITLAB_USERNAME_FORBIDDEN_SUFFIXES
                        )
            )


def sanitize_username(name):
    r"""Return a valid GitLab username derived from the provided one.

    If the provided one is valid, it is of course unchanged. Otherwise,
    the rules that GitLab applies in SSO signup are applied.

    From ``app/models/namespace.rb`` in GitLab 14.10.1, called from
    ``Gitlab::Auth::OAuth::User#user_attributes``::

      def clean_path(path)
        path = path.dup
        # Get the email username by removing everything after an `@` sign.
        path.gsub!(/@.*\z/,                "")
        # Remove everything that's not in the list of allowed characters.
        path.gsub!(/[^a-zA-Z0-9_\-\.]/,    "")
        # Remove trailing violations ('.atom', '.git', or '.')
        loop do
          orig = path
          PATH_TRAILING_VIOLATIONS.each { |ext| path = path.chomp(ext) }
          break if orig == path
        end

        # Remove leading violations ('-')
        path.gsub!(/\A\-+/, "")

        # Users with the great usernames of "." or ".." would end up with
        # a blank username.
        # Work around that by setting their username to "blank", followed by
        # a counter.
        path = "blank" if path.blank?

        uniquify = Uniquify.new
        uniquify.string(path) { |s| Namespace.find_by_path_or_name(s) }
      end

    This function does the same, expcept for the unicity counter at the end,
    which will require round-trips to the GitLab instance.


    Doctests inspired by `spec/models/namespace_spec.rb` at GitLab 14.10.1::

      >>> sanitize_username("-john+gitlab-ETC%.git@gmail.com")
      'johngitlab-ETC'
      >>> sanitize_username("--%+--valid_*&%name=.git.%.atom.atom.@email.com")
      'valid_name'

    More tests::

      >>> sanitize_username('.git')
      'blank'

    Numeric usernames are problematic with the APU, especially when using
    the ``sudo`` feature, because they are interpreted as user ids. Hence we
    change them:

       >>> sanitize_username('1234567')
       '1234567_'

    """
    # Handling multiple lines: it is very unlikely that the system we're
    # exporting users from would accept line breaks in nicknames.
    # Still, let's guard against it.
    name = name.splitlines()[0]
    # (If supplied username looks like an email address),
    # get the email username by removing everything after an `@` sign.
    # (including the `@`)
    name = EMAIL_AT_AND_FOLLOWING_RX.sub('', name)

    # Remove everything that's not in the list of allowed characters.
    name = GITLAB_USERNAME_FORBIDDEN_CHARS_RX.sub('', name)
    while True:
        orig = name
        for suffix in GITLAB_USERNAME_FORBIDDEN_SUFFIXES:
            if name.endswith(suffix):
                name = orig[:-len(suffix)]
        if name == orig:
            break

    # Remove leading violations ('-')
    name = LEADING_HYPHENS_RX.sub('', name)

    # Users with the great usernames of "." or ".." would end up with a
    # blank username.
    # Work around that by setting their username to "blank", followed by a
    # counter.
    # (the counter part is left to the caller)
    if not name:
        name = "blank"

    # Pure numeric usernames are problematic with the API, because
    # the `sudo` feature interprets them as ids, not usernames
    if DECIMAL_NUMBER_RX.match(name):
        name += '_'

    return name


@attr.define
class EmailUserMapping:
    """A user mapping whose keys are email addresses, based on GitLab lookups.

    Relies on the admin connection provided by :attr:`admin_api`.
    """
    admin_api: GitLabAPI
    mapping: dict = attr.field(factory=dict)

    create_missing: bool = False
    """If ``True`` missing users will be automatically created.

    For the creation to work, the  :attr:`src_user_exporter` attribute
    must also be set.
    """

    src_user_exporter: Optional[Callable] = None
    """Callback to extract the necessary data to create missing GitLab users.

    The callback takes a unique :class:`str` argument (the user email)

    Callback return
    ~~~~~~~~~~~~~~~

    The returned value must be a :class:`dict`.

    Required values:

    - `nickname`: the user short handle, usable in login or in `@` mentions.
       Example: 'gracinet'
    - `fullname`: the complete name, e.g., 'Georges Racinet'

    Default values

    - `force_random_password`: set to `True` if `password` and `reset_password`
      are missing. The create user will have to use the reset facility at
      first login.
    - `confirmed_at`: if not set, the current time is automatically used.

    Ignored values:

    - `email`: the input email will be used as primary email. This can change
      in the future if there are use cases for secondary emails.

    Unsettable values:

    - `confirmed_at`, `created_at`: ignored by GitLab itself. Applications
      are advised to use the ``note`` or ``bio`` text attributes to record
      the original date of creation for lack of better solution.

    Other key/value pairs will be passed as-is to the
    `GitLab API <https://docs.gitlab.com/ce/api/users.html#user-creation>`_

    Note: the returned :class:`dict` will be converted in-place, hence
    after-the-fact inspection is possible.
    """

    testing_mode: bool = False
    """Put created addresses under the :attr:`testing_address_domain` domain.

    If ``True``, automatic user creation will be made by postfixing the
    address with the value of :addr:`testing_address_domain`, so that, e.g,
    ``foo@example.com`` becomes ``foo@example.com.heptapod.test``.

    This is meant for testing instances, to be 100% sure that a test run
    wont end up sending confusing emails to the actual users.

    Addresses that are found in the database are unaffected: if a user
    has the requested address, it will be found. Similarly, if
    ``foo@example.com.heptapod.test`` is present in the database, its user
    will match ``foo@example.com``, so that resuming an import that has
    performed some automatic creations works straight.
    """

    testing_address_domain: str = 'heptapod.test'
    """See :attr:`testing_mode."""

    @property
    def testing_address_suffix(self):
        return '.' + self.testing_address_domain

    def normalize_email(self, email):
        """Normalization as GitLab does.

        Excerpts from Rails app (GitLab 14.10.1) lib/api/user.rb::

            conflict!('Email has already been taken') if User
              .by_any_email(user.email.downcase)
              .any?

        and also (TODO not sure where exactly it matters, but we may need
        to implement something alike)
        app/services/users/update_canonical_email_service.rb::

            def canonicalize_email
              email = user.email

              portions = email.split('@')
              username = portions.shift
              rest = portions.join

              regex = Regexp.union(INCLUDED_DOMAINS_PATTERN)
              return unless regex.match?(rest)

              no_dots = username.tr('.', '')
              before_plus = no_dots.split('+')[0]
              "#{before_plus}@#{rest}"
            end
        """
        return email.lower()

    def get(self, email):
        gl_email = self.normalize_email(email)

        # even in testing mode, it could be that the user exists with
        # the given address (preloaded testing instance)
        username = self.simple_fetch(gl_email)
        if username is not None:
            return username

        if self.testing_mode:
            gl_email += self.testing_address_suffix
            username = self.simple_fetch(gl_email)

        if username is None and self.create_missing:
            username = self.create_user(gl_email, input_email=email)

        return username

    def simple_fetch(self, email):
        gl_username = self.mapping.get(email)
        if gl_username is not None:
            return gl_username

        gl_username = self.gl_exact_search(email)
        if gl_username is not None:
            self.mapping[email] = gl_username
        return gl_username

    def gl_exact_search(self, email):
        """Use the fuzzy GitLab search API and postfilter for exact matches.

        :returns: a :class:`User` instance or `None` if no match.

        Only *confirmed* email addresses are taken into account.

        GitLab API allows to search users by email only with the general
        search (Intended for fulltext / UI convenience) that does search on
        primary and secondary emails, but also takes unrelated
        fields into account (e.g., ``username``, or whatever will feel useful
        for humans in the future).

        This method adds a layer of check to eliminate wrong (or unconfirmed
        results).

        Whatever hops we have to take to perform this search, the results
        eventually come from the `emails` table, which map email adresses
        to users without ambiguity because:

        - it has a unicity constraint on the email address itself
        - it has a foreign key constraint towards the users table
        """
        api = self.admin_api
        fuzzy = api.search(SearchScope.USERS, email)
        for info in fuzzy:
            user = api.users.get(info['id'])
            for user_email in user.emails.list():
                if user_email.email == email:
                    # depending on GitLab version, unconfirmed emails can
                    # be returned or not, whence the pragma.
                    if user_email.confirmed_at is None:  # pragma no cover
                        return None
                    return user.username

    def create_user(self, gl_email, input_email):
        data = self.src_user_exporter(input_email)
        self.convert_user_data(gl_email, data)
        input_username = data.pop('input_username')
        attempt_username = data['username']
        count = 1
        while count < 10:
            try:
                self.gl_create_user(data)
                break
            except GitlabCreateError as exc:
                err_msg = exc.error_message.lower().strip()
                if (exc.response_code != 409
                        or err_msg != 'username has already been taken'):
                    raise
                count += 1
                data['username'] = f'{attempt_username}_{count}'

        final_username = data['username']
        self.mapping[gl_email] = final_username
        if final_username != input_username:
            logger.warning("Final username associated with email address %r "
                           "is %r instead of the exported %r, to respect "
                           "GitLab validity rules. The user can change it "
                           "afterwards if the GitLab instance configuration "
                           "allows it.",
                           input_email, final_username, input_username)
        return final_username

    def convert_user_data(self, email, data):
        """Convert user data to match GitLab schema."""
        input_username = data.pop('nickname')
        data['input_username'] = input_username
        data['username'] = sanitize_username(input_username)
        data['name'] = data.pop('fullname')
        data['email'] = email
        confirmed_at = data.pop('confirmed_at', None)
        if confirmed_at is not None:
            data['confirmed_at'] = dt_to_api(confirmed_at)
        if not data.get('password') and not data.get('reset_password'):
            data['force_random_password'] = True

        # If skip_confirmation value below changes, then the logic to match
        # users by confirmed email addressses only (necessary for security)
        # also needs to be adapted.
        data['skip_confirmation'] = True
        return data

    def gl_create_user(self, data):
        logger.info("Creating user %r", data)
        return self.admin_api.users.create(data)
