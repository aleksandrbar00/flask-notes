from note import Note
from db import db


class NoteService:
    @staticmethod
    def add_note(user_id, content):
        note = Note(
            content=content,
            user_id=user_id
        )
        db.session.add(note)
        db.session.commit()

    @staticmethod
    def get_user_notes(user_id, period):
        return db.session.query(Note).filter(
            db.sql.func.date(Note.created_at) >= period['from'],
            db.sql.func.date(Note.created_at) <= period['to'],
            Note.user_id == user_id
        ).all()
