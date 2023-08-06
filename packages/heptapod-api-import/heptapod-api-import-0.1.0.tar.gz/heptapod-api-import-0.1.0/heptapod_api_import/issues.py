# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import logging

from gitlab.const import AccessLevel

from .base import BaseImporter
from .objects import GitLabObjectHandle

logger = logging.getLogger(__name__)


class IssuesImporter(BaseImporter):
    """Takes care of issues and associated objects.

    Applicative code should only need to use the :methd:`import_issues`
    method.
    """

    def __init__(self, *a, **kw):
        super(IssuesImporter, self).__init__(*a, **kw)
        self.saved_attrs = {}

    def start(self, project_id):
        """TODO make this a context manager?"""
        api, extra = self.gitlab_user_api('root')  # TODO object_owner
        project = api.projects.get(project_id, **extra)
        self.saved_attrs[GitLabObjectHandle('project', project_id)] = dict(
            emails_disabled=project.emails_disabled)
        project.heptapod_api_import = 'heptapod_api'
        project.emails_disabled = True
        project.save(**extra)

    def end(self, project_id):
        api, extra = self.gitlab_user_api('root')  # TODO object_owner
        project = api.projects.get(project_id, **extra)
        project.heptapod_api_import = 'heptapod_api_done'
        saved = self.saved_attrs[GitLabObjectHandle('project', project_id)]
        project.emails_disabled = saved['emails_disabled']
        project.save(**extra)

    def project_api(self, username, project_id):
        """Shortcut for readability."""
        api, extra = self.gitlab_user_api(username)
        return api.projects.get(project_id, lazy=True), extra

    def issues_api(self, username, project_id):
        """Shortcut for readability."""
        project, extra = self.project_api(username, project_id)
        return project.issues, extra

    def create_issue(self, data):
        """Create just the issue itself."""
        project_id = data.pop('project_id')
        username = data.pop('username')
        data = self.normalize_payload(data)

        title = data['title']
        if len(title) > 255:
            data['title'] = title[:200] + '...'
            descr = data.get('description', '').strip()
            if descr:
                data['description'] = title + '\n\n' + descr
            else:
                data['description'] = title

        if not data.get('description'):
            # GitLab does not accept empty issue descriptions
            data['description'] = '(empty description)'

        return self.gl_create_issue(project_id, username, data)

    def gl_create_issue(self, project_id, username, data):

        issues, extra = self.issues_api(username, project_id)
        # TODO need the admin_issue permission for some operations
        # and the `set_issue_metadata` for labels, milestones etc.
        # cf app/policies/issue_policy.rb
        return issues.create(data, **extra)

    def ensure_user_can_file(self, username, project_id):
        """Give the minimal permissions so that user can file issue, comment.
        """
        # TODO unless project is public
        self.ensure_role(username, AccessLevel.REPORTER,
                         GitLabObjectHandle('project', project_id)
                         )

    def create_note(self, issue, data):
        username = data.pop('username')
        self.ensure_user_can_file(username, issue.project_id)
        # TODO unless project is public
        data = self.normalize_payload(data)
        if not data.get('body'):
            # GitLab does not accept empty body:
            #     400 Bad request - Note {:note=>["can't be blank"]}
            data['body'] = '(empty message)'
        return self.gl_create_note(username, issue, data)

    def gl_create_note(self, username, issue, data):
        issues, extra = self.issues_api(username, issue.project_id)
        return issues.get(issue.iid).notes.create(data, **extra)

    def usernames_to_ids(self, data, key, target_key):
        """Update data[key] in place to put ids instead of usernames.
        """
        value = data.pop(key, None)
        if value is None:
            return

        data[target_key] = tuple(self.gitlab_multiple_api.user_id(v)
                                 for v in value)

    def change_labels(self, issue, data):
        username = data.pop('username')
        issues, extra = self.issues_api(username, issue.project_id)
        as_user = issues.get(issue.iid, **extra)
        data = self.normalize_payload(data)
        as_user.add_labels = data['add_labels']
        as_user.remove_labels = data['remove_labels']
        dt = data.get('datetime')
        state_change = data.get('state_change')
        if state_change is not None:
            as_user.state_event = state_change
        if dt is not None:
            as_user.updated_at = dt
        assignee_ids = data.get('assignee_ids')
        if assignee_ids is not None:
            as_user.assignee_ids = assignee_ids

        as_user.save(**extra)

    def create_project_file(self, project_id, data):
        username = data.pop('creator')
        project, extra = self.project_api(username, project_id)
        return project.upload(data['file_name'], filepath=data['path'],
                              **extra)

    def import_issue(self, data, attachments_header='\n\n'):
        """Import an issue and its timeline of events.

        The events can be a new comment, changing labels, closing, reopening
        etc.

        Data dictionaries are as in the GitLab API PUT or POST body,
        with the following exceptions:

        - ``events`` (issue itself only): list of dict-like objects with:
          + ``type``: one of the implemented event types (see below)
          + ``data``: actual data associated to the event. They are
           subject to the rules explained here.
        - ``project_id`` (issue itself only): numeric ID (:class:`int`)
           of the project. Not part of the API body, because it is passed
          in the URL.
        - ``username`` (issue itself and all its events): used by the
          importer to act as the proper GitLab user. Not part of API body
          (derived from token headers).
        - all date/time values: have to be given in UTC as a
          :class:`datetime` instance without time zone.
        - ``labels`` (issue itself and all its events): iterable of label
          names
        - ``attachments``: list of dict-like objects with:
          + ``creator``: username of the attachment creator
          + ``path``: path on the local filesystem to data (TODO support also
            opended file-like object)
          + ``file_name``: name of the attached file
          + ``download_renderer``: template to use to render the attachment
            in issue description, will be given the projects file return
            dict, with ``url`` and ``markdown`` keys, see
              https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#file-uploads
            Together with ``attachments_header``, can be used, e.g., to
            build up a table.

        Events and their specificites:

        - ``comment``: an Issue Note is added to the issue
        - ``change_labels``: an update of the issue is made to add labels.
          This event has specific data fields: `add_labels`, `remove_labels`
          (both iterables of label names) and `datetime`.

        Note: the "event" terminology is specific to Heptapod API Importer.

        GitLab API References:

        - Issues: https://docs.gitlab.com/ce/api/issues.html
        - Notes (comments): https://docs.gitlab.com/ce/api/notes.html
        """
        # TODO decide whether we want to grant or use the owner API
        # to add the labels
        project_id = data['project_id']
        self.ensure_user_can_file(data['username'], project_id)
        events = data.pop('events')
        attachments = data.pop('attachments', ())
        if attachments:
            data['description'] += attachments_header
        for att in attachments:
            self.ensure_user_can_file(att['creator'], project_id)
            render_args = self.create_project_file(data['project_id'], att)
            data['description'] += att['download_renderer'].format(
                **render_args)
        self.usernames_to_ids(data, 'assignees', 'assignee_ids')

        issue = self.create_issue(data)

        for event in events:
            event_data = event['data']
            self.usernames_to_ids(event_data, 'assignees', 'assignee_ids')
            if event['type'] == 'comment':
                self.create_note(issue, event_data)
            elif event['type'] == 'change_labels':
                self.change_labels(issue, event_data)
