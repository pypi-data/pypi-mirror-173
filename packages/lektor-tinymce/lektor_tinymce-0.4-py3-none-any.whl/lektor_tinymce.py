# -*- coding: utf-8 -*-
from flask import render_template_string
from lektor.admin.modules import dash
from lektor.pluginsystem import Plugin


KEY = ''
TINYMCE_SETTINGS = ''
TEMPLATE = '''
{% extends "dash.html" %}
{% block scripts %}
  {{ super() }}
  <script src="https://cdn.tiny.cloud/1/{{tinymce_api_key}}/tinymce/4/tinymce.min.js" referrerpolicy="origin"></script>
  <script>
    var valueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
    var inputEvent = new Event('input', { bubbles: true });
    inputEvent.simulated = true;
    (new MutationObserver(function() {
        [...document.getElementsByTagName('textarea')].forEach(txt_elem => {
            if (txt_elem.classList.contains('form-control')) {
                txt_elem.classList.add('tinymce-attached');
                tinymce.init({
                    target: txt_elem,
                    setup: function(editor) {
                        editor.on('Change', function(e) {
                            valueSetter.call(txt_elem, editor.getContent());
                            txt_elem.dispatchEvent(inputEvent);
                        });
                    },
                    {{ tinymce_settings|safe }}
                });
            };
        });
    })).observe(
        document.getElementsByTagName('body')[0],
        {
            subtree: true,
            childList: true
        },
    );
  </script>
{% endblock %}
'''


def patched_endpoint(*args, **kwargs):
    return render_template_string(
        TEMPLATE,
        tinymce_settings=TINYMCE_SETTINGS,
        tinymce_api_key=KEY,
    )


def url_rule_wrapper(rule, *args, **kwargs):
    local_rule = rule
    return lambda s: s.add_url_rule(local_rule, *args, **kwargs)


class TinyMCEPlugin(Plugin):
    name = 'lektor-tinymce'
    description = u'Lektor Plugin for TinyMCE Text Editor use.'

    def on_setup_env(self, *args, **kwargs):
        global KEY
        global TINYMCE_SETTINGS
        config = self.get_config()
        KEY = config.get('licence.api-key', 'no-api-key')
        TINYMCE_SETTINGS = config.get('config.settings', '')

    def on_server_spawn(self, *args, **kwargs):
        # look through deferred_functions in dash blueprint, find the one with
        # route rule for admin views and replace it with patched function
        for idx, item in enumerate(dash.bp.deferred_functions):
            if 'rule' in item.__code__.co_freevars:
                rule_idx = item.__code__.co_freevars.index('rule')
                rule = item.__closure__[rule_idx].cell_contents
                if rule != '/':
                    dash.bp.deferred_functions[idx] = url_rule_wrapper(
                        rule,
                        endpoint='app',
                        view_func=patched_endpoint,
                    )
