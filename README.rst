pretalx Zammad plugin
==========================

This is a plugin for `pretalx`_.

This plugin allows you to link to tickets in a Zammad issue tracker.

The plugin will match the e-mail adresses of speakers and the six digit speaker and session codes from pretalx with the customer e-mail addresses and tags in Zammad and show the related Zammad ticket title, ticket state and ID on the speaker and session pages in the orga interface.

To manually link Zammad tickets to speakers or sessions in pretalx, you can simply add the six digit code of a speaker or a submission to the tags within Zammad.

Development setup
-----------------

1. Make sure that you have a working `pretalx development setup`_.

2. Clone this repository, eg to ``local/pretalx-zammad``.

3. Activate the virtual environment you use for pretalx development.

4. Run ``pip install -e .`` within this directory to register this application with pretalx's plugin registry.

5. Run ``make`` within this directory to compile translations.

6. Restart your local pretalx server. This plugin should show up in the plugin list shown on startup in the console.
   You can now use the plugin from this repository for your events by enabling it in the 'plugins' tab in the settings.

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed::

    pip install flake8 flake8-bugbear isort black

To check your plugin for rule violations, run::

    black --check .
    isort -c .
    flake8 .

You can auto-fix some of these issues by running::

    isort .
    black .


License
-------

Copyright 2025 Florian Moesch

Released under the terms of the Apache License 2.0


.. _pretalx: https://github.com/pretalx/pretalx
.. _pretalx development setup: https://docs.pretalx.org/en/latest/developer/setup.html
