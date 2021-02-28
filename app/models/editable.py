from .. import db


class EditableHTML(db.Model):
    """ CKEditor instances """
    id = db.Column(db.Integer, primary_key=True)
    locale = db.Column(db.Integer, db.ForeignKey('locales.id', ondelete='CASCADE'))
    editor_name = db.Column(db.String(100), unique=True)
    page_name = db.Column(db.String(100), unique=True)
    value = db.Column(db.Text)

    @staticmethod
    def get_editable_html(editor_name):
        editable_html_obj = EditableHTML.query.filter_by(
            editor_name=editor_name
        ).first()

        if editable_html_obj is None:
            return False
        return editable_html_obj

    @staticmethod
    def get_editable_html_by_page_name(page_name):
        editable_html_obj = EditableHTML.query.filter_by(
            page_name=page_name
        ).first()

        if editable_html_obj is None:
            return False
        return editable_html_obj
