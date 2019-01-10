import codecs
import csv
from app import db


class Settings(db.Model):
    __tablename__ = 'app_settings'
    id = db.Column(db.Unicode(256), db.Sequence('app_settings_id_seq'), primary_key=True)
    value = db.Column(db.Unicode(256))

    @staticmethod
    def insert_settings(csv_path):
        with codecs.open(csv_path, 'r', 'utf-8') as settings_file:
            settings = csv.reader(settings_file)
            for s in settings:
                setting = Settings.query.filter_by(id=s[0]).first()
                if setting is None:
                    setting = Settings(
                        id=s[0],
                        value=s[1]
                    )
                    db.session.add(setting)
                db.session.commit()

    def __repr__(self):
        return '<Settings %r>' % self.id
