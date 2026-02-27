import psycopg2
import uuid
import logging

def get_connection():
    return psycopg2.connect(
        host="10.0.0.4",  
        database="resumes",
        user="postgres",
        password="password",
        port=5432
    )

def insert_candidate(data):
    conn = get_connection()
    cur = conn.cursor()

    try:
        candidate_id = str(uuid.uuid4())

        # Insert candidate
        cur.execute("""
            INSERT INTO candidates (id, full_name, summary, years_experience)
            VALUES (%s, %s, %s, %s)
        """, (
            candidate_id,
            data["candidate"]["full_name"],
            data["candidate"]["summary"],
            data["candidate"]["years_experience"]
        ))

        # Insert contacts
        contact_id = str(uuid.uuid4())
        contacts = data.get("contacts", {})
        cur.execute("""
            INSERT INTO contacts (id, candidate_id, email, phone, linkedin_url, github_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            contact_id,
            candidate_id,
            contacts.get("email"),
            contacts.get("phone"),
            contacts.get("linkedin_url"),
            contacts.get("github_url")
        ))

        # Insert skills
        for skill in data.get("skills", []):
            cur.execute("""
                INSERT INTO skills (id, candidate_id, skill_name, category)
                VALUES (%s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                candidate_id,
                skill.get("skill_name"),
                skill.get("category")
            ))

        # Insert education
        for edu in data.get("education", []):
            cur.execute("""
                INSERT INTO education (id, candidate_id, degree, institution, start_year, end_year)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                candidate_id,
                edu.get("degree"),
                edu.get("institution"),
                edu.get("start_year"),
                edu.get("end_year")
            ))

        # Insert experience
        for exp in data.get("experience", []):
            cur.execute("""
                INSERT INTO work_experience (id, candidate_id, company, role, start_date, end_date, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                candidate_id,
                exp.get("company"),
                exp.get("role"),
                exp.get("start_date"),
                exp.get("end_date"),
                exp.get("description")
            ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        logging.error(str(e))
        raise e

    finally:
        cur.close()
        conn.close()
