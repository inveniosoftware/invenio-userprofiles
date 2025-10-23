..
    This file is part of Invenio.
    Copyright (C) 2015-2025 CERN.
    Copyright (C) 2024-2025 Graz University of Technology.
    Copyright (C) 2025 KTH Royal Institute of Technology.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version v4.1.1 (released 2025-10-23)

- i18n: pulled translations

Version v4.1.0 (released 2025-07-17)

- i18n: pulled translations
- i18n: push translations
- fix: setuptools require underscores instead of dashes
- i18n: Removed obsolete languages
- i18n: unified gettext formatting
- fix: 404 issue when pressing cancel

Version 4.0.0 (released 2024-12-04)

- tests: apply changes for sqlalchemy>=2.0
- setup: bump major dependencies

Version 3.0.1 (release 2024-11-30)

- setup: change to reusable workflows
- setup: pin dependencies
- i18n:push translations
- tests: check existing username case-insensitive

Version 3.0.0 (released 2024-03-22)

- breaking change: remove breadcrumbs usage
- global: migrate to (api) finalize_app
  (remove deprecation for `before_first_request`)

Version 2.3.1 (released 2023-10-20)

- email: case-insensitive comparison of user email

Version 2.3.0 (released 2023-07-31)

- settings profile: Update buttons with labeled styling and a11y fixes
- alembic: fix recipe based on latest sqlalchemy-continuum
- pull translations

Version 2.2.1 (released 2023-05-26)

- fix styling for locale preferences field

Version 2.2.0 (released 2023-04-25)

- add locale to user profile preferences

Version 2.1.0 (released 2023-03-02)

- remove deprecated flask_babelex imports
- install invenio_i18n explicitly

Version 2.0.5 (released 2022-12-14)

- forms: add helper for preferences form

Version 2.0.4 (released 2022-11-21)

- add translations

Version 2.0.3 (released 2022-07-08)

- add redirection on user profile form submit
- allow updating preferences for read only profiles

Version 2.0.2 (released 2022-07-01)

- Style radio buttons and remove dotted bullet points in settings page.

Version 2.0.1 (released 2022-06-10)

- Fixes the Alembic recipe dependency for removing the userprofiles table.

Version 2.0.0 (released 2022-05-23)

- Changes the profile backend to use the new Invenio-Accounts 2.0 profile
  field instead of a separate database table.

- Adds support for allowing users to change their visibility settings.

Version 1.2.4 (released 2021-10-18)

- Unpin Flask 2

Version 1.2.3 (released 2021-07-12)

- Adds german translations

Version 1.2.2 (released 2021-05-17)

- Add config option to make user profiles form read-only

Version 1.2.1 (released 2020-12-17)

- Add theme dependent icons.

Version 1.2.0 (released 2020-12-09)

- Marked strings for translation
- Added Turkish translation
- Changes `cancel` button's color
- Integrates Semantic-UI templates
- Removes example app

Version 1.1.1 (released 2020-05-11)

- Minimum version of Invenio-Accounts bumped to v1.2.1 due WTForms moving the
  email validation to an optional dependency

Version 1.1.0 (released 2020-03-11)

- Change Flask dependency management to invenio-base
- drop Python 2.7 support

Version 1.0.1 (released 2018-05-25)

- Flask v1.0 support.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
