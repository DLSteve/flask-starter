import codecs
import csv

from app import db
from dateutil.parser import parse
from sqlalchemy import text
from chardet.universaldetector import UniversalDetector


class RoleAccountPasswordReset(db.Model):
    """An ISIM reset event for a warehouse role based account"""
    __tablename__ = 'role_account_password_resets'
    id = db.Column(db.Integer, db.Sequence('role_account_password_resets_id_seq'), primary_key=True)
    agent = db.Column(db.String(100))
    acct = db.Column(db.String(100))
    acct_location = db.Column(db.String(100))
    reset_date = db.Column(db.Date())
    reset_day = db.Column(db.String(100))
    reset_type = db.Column(db.String(100))

    @staticmethod
    def clean_duplicates():
        database = 'iam_analytics'
        table = 'role_account_password_resets'
        sql = text('DELETE FROM {db}.dbo.{tbl} WHERE id NOT IN (SELECT MIN(id)'
                   ' FROM {db}.dbo.{tbl} GROUP BY agent, acct, acct_location,'
                   ' reset_date, reset_day, reset_type);'.format(db=database, tbl=table))
        db.engine.execute(sql)

    @staticmethod
    def insert_resets(csv_path):

        # Attempt to detect file encoding
        detector = UniversalDetector()
        file = codecs.open(csv_path, 'rb')
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        file.close()
        encoding = detector.result['encoding'] if detector.result else 'utf-8'

        with codecs.open(csv_path, 'r', encoding) as role_resets_file:

            # Check if CSV file has a header row.
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(role_resets_file.read(2048))
            role_resets_file.seek(0)
            role_resets = csv.reader(role_resets_file)
            iter_resets = iter(role_resets)

            if has_header:
                next(iter_resets)

            for r in iter_resets:
                try:
                    role_password_resets = RoleAccountPasswordReset(
                        agent=r[0],
                        acct=r[1],
                        acct_location=r[2],
                        reset_date=parse(r[3], dayfirst=False, yearfirst=True, fuzzy=True, ignoretz=True),
                        reset_day=r[4],
                        reset_type=r[5]
                    )
                    db.session.add(role_password_resets)
                    db.session.commit()
                except ValueError:
                    pass

    def __repr__(self):
        return 'RoleAccountPasswordReset id: {}, account: {}, date: {}>'.format(self.id, self.acct, self.reset_date)


class NamedAccountPasswordReset(db.Model):
    """An ISIM or MCA reset event for a named based account"""
    __tablename__ = 'named_account_password_resets'
    id = db.Column(db.Integer, db.Sequence('named_account_password_resets_id_seq'), primary_key=True)
    agent = db.Column(db.String(100))
    acct = db.Column(db.String(100))
    acct_location = db.Column(db.String(100))
    reset_date = db.Column(db.Date())
    reset_day = db.Column(db.String(100))
    reset_type = db.Column(db.String(100))
    type = db.Column(db.String(100))

    @staticmethod
    def clean_duplicates():
        database = 'iam_analytics'
        table = 'named_account_password_resets'
        sql = text('DELETE FROM {db}.dbo.{tbl} WHERE id NOT IN (SELECT MIN(id)'
                   ' FROM {db}.dbo.{tbl} GROUP BY agent, acct, acct_location,'
                   ' reset_date, reset_day, reset_type);'.format(db=database, tbl=table))
        db.engine.execute(sql)

    @staticmethod
    def insert_resets(csv_path):

        # Attempt to detect file encoding
        detector = UniversalDetector()
        file = codecs.open(csv_path, 'rb')
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        file.close()
        encoding = detector.result['encoding'] if detector.result else 'utf-8'

        with codecs.open(csv_path, 'r', encoding) as named_resets_file:

            # Check if CSV file has a header row.
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(named_resets_file.read(2048))
            named_resets_file.seek(0)
            named_resets = csv.reader(named_resets_file)
            iter_resets = iter(named_resets)

            if has_header:
                next(iter_resets)

            for r in iter_resets:
                if r[6] not in ['aux-support', 'aux-testUser']:
                    try:
                        named_password_resets = NamedAccountPasswordReset(
                            agent=r[0],
                            acct=r[1],
                            acct_location=r[2] if r[2] else '00099',
                            reset_date=parse(r[3], dayfirst=False, yearfirst=True, fuzzy=True, ignoretz=True),
                            reset_day=r[4],
                            reset_type=r[5],
                            type=r[6] if r[6] else 'Unknown'
                        )
                        db.session.add(named_password_resets)
                        db.session.commit()
                    except ValueError:
                        pass

    def __repr__(self):
        return 'NamedAccountPasswordReset id: {}, account: {}, date: {}>'.format(self.id, self.acct, self.reset_date)
