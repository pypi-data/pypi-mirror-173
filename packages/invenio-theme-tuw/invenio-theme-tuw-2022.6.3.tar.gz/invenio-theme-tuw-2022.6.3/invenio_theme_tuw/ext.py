# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing the theme for TU Wien."""

from flask.config import Config

from . import config
from .views import create_blueprint


class TUWConfig(Config):
    """Override for the Flask config that evaluates the SITE_{API,UI}_URL proxies."""

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if key in ("SITE_UI_URL", "SITE_API_URL"):
            value = str(value)

        return value


class InvenioThemeTUW:
    """Invenio-Theme-TUW extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-theme-tuw"] = self

        blueprint = create_blueprint(app)
        app.register_blueprint(blueprint)

        @app.before_first_request
        def patch_config():
            # replace the app's config with our own override that evaluates
            # the LocalProxy objects set for SITE_{API,UI}_URL by casting them
            # into strings (which is their expected type)
            app.config = TUWConfig(app.config.root_path, app.config)

        @app.before_first_request
        def register_bp_first():
            # since invenio-app-rdm currently (april 2021) doesn't offer an easy way of
            # overriding the provided jinja templates, we have to perform a workaround:
            # the first blueprint that has a definition for a template (per name) gets
            # selected by 'render_template'
            # thus, we just have to make sure that our blueprint is inserted before the
            # 'invenio_app_rdm' blueprints
            # note: the below code requires Flask 2.0.2+ and Python 3.7+
            bps = {
                name: bp
                for name, bp in app.blueprints.items()
                if name != "invenio_theme_tuw"
            }
            app.blueprints = {"invenio_theme_tuw": blueprint, **bps}

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            app.config.setdefault(k, getattr(config, k))
