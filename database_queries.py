from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_user = 'myuser'
db_password = 'aibekarsen'
db_host = 'localhost'
db_port = '5432'
db_name = 'health_info_db'

DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Query 1a: List all diseases caused by "bacteria" that were discovered before 2020.
query1a = text("""
SELECT d.disease_code, d.description
FROM Disease d
JOIN Discover di ON d.disease_code = di.disease_code
WHERE d.pathogen = 'bacteria' AND di.first_enc_date < '2020-01-01';
""")

print("\nQuery 1a: Diseases caused by 'bacteria' discovered before 2020:")
result1a = session.execute(query1a).mappings()
for row in result1a:
    print(f"Disease Code: {row['disease_code']}, Description: {row['description']}")

# Query 1b: Retrieve the names and degrees of doctors who are not specialized in "infectious diseases."
query1b = text("""
SELECT u.name, u.surname, doc.degree
FROM Users u
JOIN Doctor doc ON u.email = doc.email
WHERE doc.email NOT IN (
    SELECT s.email
    FROM Specialize s
    JOIN disease_type dt ON s.id = dt.id
    WHERE dt.description = 'Infectious diseases'
);
""")

result1b = session.execute(query1b).mappings()
print("\nQuery 1b: Doctors not specialized in 'Infectious diseases':")
for row in result1b:
    print(f"Name: {row['name']} {row['surname']}, Degree: {row['degree']}")

# Query 1c: List the name, surname, and degree of doctors who are specialized in more than 2 disease types.
query1c = text("""
SELECT u.name, u.surname, doc.degree
FROM Users u
JOIN Doctor doc ON u.email = doc.email
JOIN Specialize s ON doc.email = s.email
GROUP BY u.email, u.name, u.surname, doc.degree
HAVING COUNT(s.id) > 2;
""")

result1c = session.execute(query1c).mappings()
print("\nQuery 1c: Doctors specialized in more than 2 disease types:")
for row in result1c:
    print(f"Name: {row['name']} {row['surname']}, Degree: {row['degree']}")

# Query 2a: List countries and the average salary of doctors specialized in "virology."
query2a = text("""
SELECT u.cname, ROUND(AVG(u.salary), 2) AS avg_salary
FROM Users u
JOIN Doctor doc ON u.email = doc.email
JOIN Specialize s ON doc.email = s.email
JOIN disease_type dt ON s.id = dt.id
WHERE dt.description = 'Virology'
GROUP BY u.cname;
""")

result2a = session.execute(query2a).mappings()
print("\nQuery 2a: Average salary of doctors specialized in 'Virology' by country:")
for row in result2a:
    print(f"Country: {row['cname']}, Average Salary: {row['avg_salary']}")

# Query 2b: Find departments with public servants reporting "covid-19" cases across multiple countries, counting such employees per department.
query2b = text("""
SELECT ps.department, COUNT(DISTINCT ps.email) AS employee_count
FROM public_servant ps
JOIN Record r ON ps.email = r.email
WHERE r.disease_code = 'COVID-19'
GROUP BY ps.department
HAVING COUNT(DISTINCT r.cname) > 1;
""")

result2b = session.execute(query2b).mappings()
print("\nQuery 2b: Departments with public servants reporting 'COVID-19' cases across multiple countries:")
for row in result2b:
    print(f"Department: {row['department']}, Employees: {row['employee_count']}")

# Query 3a: Double the salary of public servants who have recorded more than three “covid-19” patients.
query3a = text("""
UPDATE Users
SET salary = salary * 2
WHERE email IN (
    SELECT ps.email
    FROM public_servant ps
    JOIN Record r ON ps.email = r.email
    WHERE r.disease_code = 'COVID-19'
    GROUP BY ps.email
    HAVING SUM(r.total_patients) > 3
);
""")
session.execute(query3a)
session.commit()
print("\nQuery 3a: Salaries updated for eligible public servants.")

# Query 3b: Delete users whose name contains the substring “bek” or “gul.”
query3b = text("""
DELETE FROM Users
WHERE name ILIKE '%bek%' OR name ILIKE '%gul%';
""")
session.execute(query3b)
session.commit()
print("\nQuery 3b: Deleted users with names containing 'bek' or 'gul'.")

# Query 4a: Create a primary indexing on the “email” field in the Users table.
query4a = text("""
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                   WHERE table_name = 'users' AND constraint_type = 'PRIMARY KEY') THEN
        ALTER TABLE Users ADD PRIMARY KEY (email);
    END IF;
END $$;
""")
session.execute(query4a)
session.commit()
print("\nQuery 4a: Primary index created on 'email' field in Users table.")

# Query 4b: Create a secondary indexing on the “disease_code” field in the Disease table.
query4b = text("""
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'idx_disease_disease_code') THEN
        CREATE INDEX idx_disease_disease_code ON Disease(disease_code);
    END IF;
END $$;
""")
session.execute(query4b)
session.commit()
print("\nQuery 4b: Secondary index created on 'disease_code' field in Disease table.")


# Query 5: List the top 2 countries with the highest number of total patients recorded.
query5 = text("""
SELECT r.cname, SUM(r.total_patients) AS total_patients
FROM Record r
GROUP BY r.cname
ORDER BY total_patients DESC
LIMIT 2;
""")

result5 = session.execute(query5).mappings()
print("\nQuery 5: Top 2 countries with the highest number of total patients recorded:")
for row in result5:
    print(f"Country: {row['cname']}, Total Patients: {row['total_patients']}")

# Query 6: Calculate the total number of patients who have covid-19 disease.
query6 = text("""
SELECT SUM(r.total_patients) AS total_covid_patients
FROM Record r
WHERE r.disease_code = 'COVID-19';
""")

result6 = session.execute(query6).mappings().first()  # Use .first() to get the first row
if result6:
    print(f"\nQuery 6: Total number of patients who have COVID-19: {result6['total_covid_patients']}")
else:
    print("\nQuery 6: No results found for total number of COVID-19 patients.")

# Query 7: Create a view with all patients’ names and surnames along with their respective diseases.
query7 = text("""
CREATE OR REPLACE VIEW patient_diseases_view AS
SELECT u.name, u.surname, pd.disease_code
FROM Users u
JOIN patient_disease pd ON u.email = pd.email;
""")
session.execute(query7)
session.commit()
print("\nQuery 7: View 'patient_diseases_view' created.")

# Query 8: Retrieve a list of all patients’ full names along with the diseases they have been diagnosed with.
query8 = text("""
SELECT name, surname, disease_code
FROM patient_diseases_view;
""")

result8 = session.execute(query8).mappings()
print("\nQuery 8: Patients and their diagnosed diseases:")
for row in result8:
    print(f"Name: {row['name']} {row['surname']}, Disease: {row['disease_code']}")

# Close the session
session.close()
