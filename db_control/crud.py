from sqlalchemy.orm import sessionmaker
from db_control.connect import engine
from db_control.mymodels import Reflection

Session = sessionmaker(bind=engine)
session = Session()

def add_reflection(feeling, event, emotion, values):
    try:
        new_reflection = Reflection(
            feeling=feeling,
            event=event,
            emotion=emotion,
            values=values
        )
        session.add(new_reflection)
        session.commit()
        print("Reflection added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error adding reflection: {e}")
    finally:
        session.close()

def update_reflection(refleid, assess, awareness):
    try:
        reflection = session.query(Reflection).filter_by(id=refleid).first()
        if reflection:
            reflection.assess = assess
            reflection.awareness = awareness
            session.commit()
            print("Reflection updated successfully.")
        else:
            print("Reflection not found.")
    except Exception as e:
        session.rollback()
        print(f"Error updating reflection: {e}")
    finally:
        session.close()
