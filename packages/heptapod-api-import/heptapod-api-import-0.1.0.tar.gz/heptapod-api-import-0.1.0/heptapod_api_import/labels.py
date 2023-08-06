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


class LabelsImporter(BaseImporter):
    """Takes care of Project and Group labels."""

    def create_object_label(self, username, obj_handle, data):
        self.ensure_role(username, AccessLevel.REPORTER, obj_handle)
        api, extra = self.gitlab_user_api(username)
        return obj_handle.traverse(api).labels.create(
            self.normalize_payload(data),
            **extra
        )

    def create_project_label(self, username, project_id, data):
        return self.create_object_label(
            username,
            GitLabObjectHandle('project', project_id),
            data)

    def create_group_label(self, username, group_id, data):
        return self.create_object_label(username,
                                        GitLabObjectHandle('group', group_id),
                                        data)

    def ensure_object_labels(self, query_username, obj_handle, labels):
        """Create only missing project labels.

        :param query_username: the GitLab username of the user doing the
          query to list existing label.
        :param labels: a list of :class:`dict` suitable for
          :meth:`create_project_label` with an extra `username` value.
        """
        existing = set(self.gl_iterate_label_names(query_username, obj_handle))
        for label_data in labels:
            label_name = label_data['name']
            if label_name in existing:
                continue
            self.create_object_label(label_data.pop('username'),
                                     obj_handle,
                                     label_data)
            existing.add(label_name)

    def ensure_group_labels(self, query_username, group_id, labels):
        return self.ensure_object_labels(
            query_username, GitLabObjectHandle('group', group_id), labels)

    def ensure_project_labels(self, query_username, project_id, labels):
        return self.ensure_object_labels(
            query_username, GitLabObjectHandle('project', project_id), labels)

    def gl_iterate_label_names(self, username, obj_handle):
        api, extra = self.gitlab_user_api(username)
        # TODO in case of project, does this include group labels?
        manager = obj_handle.traverse(api).labels
        return (lab.name for lab in manager.list(iterator=True, **extra))
