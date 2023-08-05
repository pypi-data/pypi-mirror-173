from upytl import html as h, Component


meta_data = {
    'data-web23py': '{web23py}',
    'data-app_root': '{app_root}',
    'data-app_static': {'URL("static")'},
}


NOBODY = ''


class CSSLink(Component):
    props = {
        'href': ''
    }

    template = {
        h.Link(rel="stylesheet", type="text/css", href='{href}'): '',
    }


index = {
    h.Html(): {
        h.Head(): {
            h.Meta(charset='utf-8', **meta_data): NOBODY,
            h.Link(rel="shortcut icon", type="image/x-icon", href={'URL("static", "favicon1.ico")'}): NOBODY,
            CSSLink(href={'URL("static", "fontawesome/css/all.css")'}): NOBODY,
            CSSLink(href={'URL("static", "css/v3p_bulma.css")'}): NOBODY,
            CSSLink(href={'URL("static", "css/app.css")'}): NOBODY,
            CSSLink(href={'URL("static", "js/codemirror/lib/codemirror.css")'}): NOBODY,
            CSSLink(href={'URL("static", "js/codemirror/addon/hint/show-hint.css")'}): NOBODY,
            CSSLink(href={'URL("static", "js/codemirror/addon/dialog/dialog.css")'}): NOBODY,
            h.Title(): '[[ title ]]'
        }
    },
    h.Body(): {
        h.Div(id="app"): NOBODY
    },
    h.Script(
        type='text/javascript',
        src={'URL("static", "js/rs_require.js")'},
        **{
            'data-main': {'URL("static", "js/index")'}
        }
    ): NOBODY
}
