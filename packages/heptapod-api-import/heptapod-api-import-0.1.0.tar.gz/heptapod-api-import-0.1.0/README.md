# Heptapod API Import

This project is a Python library to perform advanced project import tasks,
leveraging the standard GitLab API.

The goal is to provide the means to keep the appropriate authorship and dates.
This toolbox is not meant to perform the necessary user mappings ; instead
it expects application code to provide them.

Example use cases:

- Importing issues from foreign issue trackers
- Importing a project from a full instance backup

In all cases it will need either an administrator private access token,
or a set of tokens for all relevant users.

Some of the most common applications will be provided with the library.
This is especially the case for those that involve only GitLab, as they
allow for easy testing within heptapod/heptapod-tests>.