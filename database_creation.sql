-- country table
CREATE TABLE country (
    cname VARCHAR(50) PRIMARY KEY,
    population BIGINT
);

-- users table
CREATE TABLE users (
    email VARCHAR(60) PRIMARY KEY,
    name VARCHAR(30),
    surname VARCHAR(40),
    salary INTEGER,
    phone VARCHAR(20),
    cname VARCHAR(50),
    FOREIGN KEY (cname)
        REFERENCES country(cname)
        ON DELETE CASCADE
);

-- patients table
CREATE TABLE patients (
    email VARCHAR(60) PRIMARY KEY,
    FOREIGN KEY (email)
        REFERENCES users(email)
        ON DELETE CASCADE
);

-- disease_type table
CREATE TABLE disease_type (
    id INTEGER PRIMARY KEY,
    description VARCHAR(140)
);

-- disease table
CREATE TABLE disease (
    disease_code VARCHAR(50) PRIMARY KEY,
    pathogen VARCHAR(20),
    description VARCHAR(140),
    id INTEGER,
    FOREIGN KEY (id)
        REFERENCES disease_type(id)
        ON DELETE CASCADE
);

-- discover table
CREATE TABLE discover (
    cname VARCHAR(50),
    disease_code VARCHAR(50),
    first_enc_date DATE,
    PRIMARY KEY (cname, disease_code),
    FOREIGN KEY (cname)
        REFERENCES country(cname)
        ON DELETE CASCADE,
    FOREIGN KEY (disease_code)
        REFERENCES disease(disease_code)
        ON DELETE CASCADE
);

-- doctor table
CREATE TABLE doctor (
    email VARCHAR(60) PRIMARY KEY,
    degree VARCHAR(20),
    FOREIGN KEY (email)
        REFERENCES users(email)
        ON DELETE CASCADE
);

-- specialize table
CREATE TABLE specialize (
    id INTEGER,
    email VARCHAR(60),
    PRIMARY KEY (id, email),
    FOREIGN KEY (id)
        REFERENCES disease_type(id)
        ON DELETE CASCADE,
    FOREIGN KEY (email)
        REFERENCES doctor(email)
        ON DELETE CASCADE
);

-- public_servant table
CREATE TABLE public_servant (
    email VARCHAR(60) PRIMARY KEY,
    department VARCHAR(50),
    FOREIGN KEY (email)
        REFERENCES users(email)
        ON DELETE CASCADE
);

-- record table
CREATE TABLE record (
    email VARCHAR(60),
    cname VARCHAR(50),
    disease_code VARCHAR(50),
    total_deaths INTEGER,
    total_patients INTEGER,
    PRIMARY KEY (email, cname, disease_code),
    FOREIGN KEY (email)
        REFERENCES public_servant(email)
        ON DELETE CASCADE,
    FOREIGN KEY (cname)
        REFERENCES country(cname)
        ON DELETE CASCADE,
    FOREIGN KEY (disease_code)
        REFERENCES disease(disease_code)
        ON DELETE CASCADE
);

-- patient_disease table
CREATE TABLE patient_disease (
    email VARCHAR(60),
    disease_code VARCHAR(50),
    disease_date DATE,
    PRIMARY KEY (email, disease_code),
    FOREIGN KEY (email)
        REFERENCES patients(email)
        ON DELETE CASCADE,
    FOREIGN KEY (disease_code)
        REFERENCES disease(disease_code)
        ON DELETE CASCADE
);

-- Data insertion statements

INSERT INTO Country (cname, population) VALUES
('United States', 331002651),
('Canada', 37742154),
('United Kingdom', 67886011),
('Germany', 83783942),
('France', 65273511),
('Italy', 60461826),
('Spain', 46754778),
('Australia', 25499884),
('China', 1439323776),
('Japan', 126476461),
('Democratic Republic of the Congo', 89561403),
('Nigeria', 206139589),
('India', 1380004385),
('Brazil', 212559417),
('Argentina', 45195777),
('Peru', 32971854),
('Chile', 19116201),
('Colombia', 50882891),
('Kazakhstan', 34984);

INSERT INTO DiseaseType (id, description) VALUES
(1, 'Infectious diseases'),
(2, 'Genetic diseases'),
(3, 'Deficiency diseases'),
(4, 'Physiological diseases'),
(5, 'Zoonotic diseases'),
(6, 'Viral diseases'),
(7, 'Bacterial diseases'),
(8, 'Parasitic diseases'),
(9, 'Neurological diseases'),
(10, 'Respiratory diseases'),
(11, 'Virology');

INSERT INTO Disease (disease_code, pathogen, description, id) VALUES
('COVID-19', 'virus', 'Respiratory illness caused by SARS-CoV-2', 6),
('Influenza', 'virus', 'Seasonal flu', 6),
('Tuberculosis', 'bacteria', 'Bacterial infection affecting lungs', 7),
('Ebola', 'virus', 'Severe viral hemorrhagic fever', 6),
('Malaria', 'parasite', 'Mosquito-borne infectious disease', 8),
('Diabetes', 'N/A', 'Chronic condition affecting insulin', 4),
('Alzheimer', 'N/A', 'Progressive neurological disorder', 9),
('Common Cold', 'virus', 'Upper respiratory tract infection', 6),
('Cholera', 'bacteria', 'Infectious disease causing severe diarrhea', 7),
('Lyme Disease', 'bacteria', 'Tick-borne illness', 7);

INSERT INTO Users (email, name, surname, salary, phone, cname) VALUES
('john.doe@example.com', 'John', 'Doe', 50000, '123-456-7890', 'United States'),
('jane.smith@example.com', 'Jane', 'Smith', 55000, '234-567-8901', 'Canada'),
('alex.brown@example.com', 'Alex', 'Brown', 60000, '345-678-9012', 'United Kingdom'),
('lisa.white@example.com', 'Lisa', 'White', 65000, '456-789-0123', 'Germany'),
('michael.green@example.com', 'Michael', 'Green', 70000, '567-890-1234', 'France'),
('emily.harris@example.com', 'Emily', 'Harris', 75000, '678-901-2345', 'Italy'),
('daniel.clark@example.com', 'Daniel', 'Clark', 80000, '789-012-3456', 'Spain'),
('olivia.lewis@example.com', 'Olivia', 'Lewis', 85000, '890-123-4567', 'Australia'),
('li.wei@example.com', 'Li', 'Wei', 90000, '901-234-5678', 'China'),
('sakura.tanaka@example.com', 'Sakura', 'Tanaka', 95000, '012-345-6789', 'Japan'),
('maria.garcia@hospital.es', 'Maria', 'Garcia', 120000, '600-123-456', 'Spain'),
('carlos.fernandez@clinic.es', 'Carlos', 'Fernandez', 115000, '600-234-567', 'Spain'),
('laura.martinez@medcenter.es', 'Laura', 'Martinez', 125000, '600-345-678', 'Spain'),
('giuseppe.rossi@ospedale.it', 'Giuseppe', 'Rossi', 130000, '600-123-456', 'Italy'),
('anna.bianchi@clinica.it', 'Anna', 'Bianchi', 125000, '600-234-567', 'Italy'),
('marco.verdi@centromedico.it', 'Marco', 'Verdi', 120000, '600-345-678', 'Italy'),
('joao.silva@healthdept.br', 'João', 'Silva', 55000, '600-123-456', 'Brazil'),
('mariana.souza@healthdept.br', 'Mariana', 'Souza', 52000, '600-234-567', 'Brazil'),
('pedro.almeida@epidemiology.br', 'Pedro', 'Almeida', 51000, '600-345-678', 'Brazil'),
('carla.costa@publichealth.br', 'Carla', 'Costa', 53000, '600-456-789', 'Brazil'),
('abdulbek.nur@domain.com', 'Abdulbek', 'Nur', 55000, '600-123-456', 'Kazakhstan'),
('gulnara.khan@domain.com', 'Gulnara', 'Khan', 52000, '600-234-567', 'Kazakhstan'),
('bekzhan.suleimenov@domain.com', 'Bekzhan', 'Suleimenov', 57000, '600-345-678', 'Kazakhstan'),
('gulzat.turgan@domain.com', 'Gulzat', 'Turgan', 53000, '600-456-789', 'Kazakhstan'),
('aigul.serik@domain.com', 'Aigul', 'Serik', 54000, '600-567-890', 'Kazakhstan'),
('zubek.aydar@domain.com', 'Zubek', 'Aydar', 58000, '600-678-901', 'Kazakhstan');

INSERT INTO Patients (email) VALUES
('john.doe@example.com'),
('jane.smith@example.com'),
('alex.brown@example.com'),
('lisa.white@example.com'),
('michael.green@example.com'),
('emily.harris@example.com'),
('daniel.clark@example.com'),
('olivia.lewis@example.com'),
('li.wei@example.com'),
('sakura.tanaka@example.com');

INSERT INTO Doctor (email, degree) VALUES
('john.doe@example.com', 'MD'),
('jane.smith@example.com', 'PhD'),
('alex.brown@example.com', 'MD'),
('lisa.white@example.com', 'MD'),
('michael.green@example.com', 'DO'),
('emily.harris@example.com', 'MD'),
('daniel.clark@example.com', 'PhD'),
('olivia.lewis@example.com', 'MD'),
('li.wei@example.com', 'MD'),
('sakura.tanaka@example.com', 'MD'),
('maria.garcia@hospital.es', 'MD'),
('carlos.fernandez@clinic.es', 'PhD'),
('laura.martinez@medcenter.es', 'DO'),
('giuseppe.rossi@ospedale.it', 'MD'),
('anna.bianchi@clinica.it', 'PhD'),
('marco.verdi@centromedico.it', 'DO');

INSERT INTO PublicServant (email, department) VALUES
('john.doe@example.com', 'Health Department'),
('jane.smith@example.com', 'Epidemiology'),
('alex.brown@example.com', 'Public Health'),
('lisa.white@example.com', 'Disease Control'),
('michael.green@example.com', 'Health Department'),
('emily.harris@example.com', 'Disease Control'),
('daniel.clark@example.com', 'Public Health'),
('olivia.lewis@example.com', 'Epidemiology'),
('li.wei@example.com', 'Health Department'),
('sakura.tanaka@example.com', 'Disease Control'),
('joao.silva@healthdept.br', 'Health Department'),
('mariana.souza@healthdept.br', 'Health Department'),
('pedro.almeida@epidemiology.br', 'Epidemiology'),
('carla.costa@publichealth.br', 'Public Health');

INSERT INTO Specialize (id, email) VALUES
(6, 'john.doe@example.com'),  
(7, 'jane.smith@example.com'),  
(1, 'alex.brown@example.com'),  
(6, 'lisa.white@example.com'),
(8, 'michael.green@example.com'),  
(1, 'emily.harris@example.com'),
(2, 'daniel.clark@example.com'), 
(9, 'olivia.lewis@example.com'),  
(7, 'li.wei@example.com'),
(6, 'sakura.tanaka@example.com'),
(1, 'maria.garcia@hospital.es'),  
(2, 'maria.garcia@hospital.es'),   
(3, 'maria.garcia@hospital.es'),    
(1, 'carlos.fernandez@clinic.es'), 
(4, 'carlos.fernandez@clinic.es'), 
(5, 'carlos.fernandez@clinic.es'),  
(2, 'laura.martinez@medcenter.es'), 
(3, 'laura.martinez@medcenter.es'),
(11, 'giuseppe.rossi@ospedale.it'),
(11, 'anna.bianchi@clinica.it'),
(11, 'marco.verdi@centromedico.it');

INSERT INTO PatientDisease (email, disease_code) VALUES
('john.doe@example.com', 'COVID-19'),
('jane.smith@example.com', 'Influenza'),
('alex.brown@example.com', 'Tuberculosis'),
('lisa.white@example.com', 'Ebola'),
('michael.green@example.com', 'Malaria'),
('emily.harris@example.com', 'Diabetes'),
('daniel.clark@example.com', 'Alzheimer'),
('olivia.lewis@example.com', 'Common Cold'),
('li.wei@example.com', 'Cholera'),
('sakura.tanaka@example.com', 'Lyme Disease');

INSERT INTO Discover (cname, disease_code, first_enc_date) VALUES
('China', 'COVID-19', '2019-12-01'),
('United States', 'Influenza', '1918-01-01'),
('United Kingdom', 'Tuberculosis', '1882-03-24'),
('Democratic Republic of the Congo', 'Ebola', '1976-08-01'),
('Nigeria', 'Malaria', '1880-11-06'),
('Germany', 'Diabetes', '1910-01-01'),
('United States', 'Alzheimer', '1906-11-03'),
('United Kingdom', 'Common Cold', '1950-01-01'),
('India', 'Cholera', '1817-01-01'),
('United States', 'Lyme Disease', '1975-01-01');

INSERT INTO Record (email, cname, disease_code, total_deaths, total_patients) VALUES
('john.doe@example.com', 'United States', 'COVID-19', 500000, 30000000),
('jane.smith@example.com', 'Canada', 'Influenza', 10000, 500000),
('alex.brown@example.com', 'United Kingdom', 'Tuberculosis', 2000, 30000),
('lisa.white@example.com', 'Germany', 'Ebola', 0, 1),
('michael.green@example.com', 'Nigeria', 'Malaria', 300000, 10000000),
('emily.harris@example.com', 'Italy', 'Diabetes', 5000, 300000),
('daniel.clark@example.com', 'United States', 'Alzheimer', 100000, 500000),
('olivia.lewis@example.com', 'Australia', 'Common Cold', 0, 1000000),
('li.wei@example.com', 'China', 'Cholera', 50000, 200000),
('sakura.tanaka@example.com', 'Japan', 'Lyme Disease', 5, 50),
('joao.silva@healthdept.br', 'Brazil', 'COVID-19', 100, 5000),
('joao.silva@healthdept.br', 'Argentina', 'COVID-19', 150, 5200),
('mariana.souza@healthdept.br', 'Brazil', 'COVID-19', 120, 4800),
('mariana.souza@healthdept.br', 'Peru', 'COVID-19', 110, 4600),
('pedro.almeida@epidemiology.br', 'Brazil', 'COVID-19', 130, 6000),
('pedro.almeida@epidemiology.br', 'Chile', 'COVID-19', 125, 5900),
('carla.costa@publichealth.br', 'Brazil', 'COVID-19', 90, 4700),
('carla.costa@publichealth.br', 'Colombia', 'COVID-19', 100, 4800);