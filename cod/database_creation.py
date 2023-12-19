import psycopg2
import csv

# Connect to your postgres DB
try:
    conn = psycopg2.connect("host=localhost dbname=Olympiadas_atletas user=postgres password=843324")
except psycopg2.OperationalError:
    print("Connection failed")


cur = conn.cursor()

# Execute a query
cur.execute('''
CREATE TABLE IF NOT EXISTS athletes (
    id SERIAL PRIMARY KEY,
    id_athletes INT,
    name VARCHAR(120),
    sex VARCHAR(6),
    age INT,
    HEIGHT NUMERIC,
    WEIGHT NUMERIC
);
    
CREATE TABLE IF NOT EXISTS team (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(50),
    name_athletes VARCHAR(120),
    athletes_id INT,
    CONSTRAINT athletes_fk FOREIGN KEY(athletes_id) REFERENCES athletes(id)
);
            
CREATE TABLE IF NOT EXISTS modalities (
    id SERIAL PRIMARY KEY,
    games VARCHAR(40),
    NOC VARCHAR(5),
    year INT,
    season VARCHAR(20),
    event VARCHAR(100),
    athletes_id INT,
    CONSTRAINT athletes_fk FOREIGN KEY(athletes_id) REFERENCES athletes(id)
);
            
CREATE TABLE IF NOT EXISTS sports (
    id SERIAL PRIMARY KEY,
    sport VARCHAR(30),
    NOC VARCHAR(5),
    modalities_id INT,
    CONSTRAINT modalities_fk FOREIGN KEY(modalities_id) REFERENCES modalities(id)
    
);
            
CREATE TABLE IF NOT EXISTS medal (
    id SERIAL PRIMARY KEY,
    medal VARCHAR(30),
    NOC VARCHAR(5),
    athletes_id INT,
    modalities_id INT,
    CONSTRAINT athletes_fk FOREIGN KEY(athletes_id) REFERENCES athletes(id),
    CONSTRAINT modalities_fk FOREIGN KEY(modalities_id) REFERENCES modalities(id)
    
);
            
CREATE TABLE IF NOT EXISTS region (
    id SERIAL PRIMARY KEY,
    noc VARCHAR(5),
    region VARCHAR(50),
    notes VARCHAR(40),
    CONSTRAINT unico_noc_region UNIQUE (noc, region)
    
);
''')
conn.commit()


athletes = []
team = []
modalities = []
sports = []
medal = []
with open(file="cod/athlete_events.csv", mode="r", encoding="utf-8") as arquivo:
    data = csv.reader(arquivo, delimiter=",")
    next(data)
    data = set(map(tuple, list(data)))
    data = list(map(list, data))
    for index, row in enumerate(data):
        row = list(map(lambda x: None if x=="NA" else x, row))
        athletes.append([index, row[0], row[1], row[2], row[3], row[4], row[5]])
        team.append([row[6], row[1], index])
        modalities.append([index, row[8], row[7], row[9], row[10], row[13], index])
        sports.append([row[12], row[7], index])
        medal.append([row[14], row[7], index, index])

athletes = set(map(tuple, athletes))
athletes = list(map(list, athletes))
athletes = list(map(lambda x: [x[0], x[1].replace("\'", "\""), x[2], x[3], x[4], x[5], x[6]], athletes))

for i in athletes:
    id = i[0]
    id_athletes = i[1]
    name = i[2]
    sex = i[3]
    age = i[4]
    height = i[5]
    weight = i[6]
    cur.execute(f'''INSERT INTO athletes (id, id_athletes, name, sex, age, HEIGHT, WEIGHT) VALUES 
                (%s, %s, %s, %s, %s, %s, %s) ''', (id, id_athletes, name, sex, age, height, weight))
    conn.commit()

for i in team:
    team_name = i[0]
    name_athletes = i[1]
    id_athletes = i[2]
    cur.execute(f'INSERT INTO team (team_name, name_athletes, athletes_id) VALUES (%s, %s, %s) ', (team_name, name_athletes, id_athletes))
    conn.commit()

for i in modalities:
    id = i[0]
    games = i[1]
    noc = i[2]
    year = i[3]
    season = i[4]
    event = i[5]
    id_athletes = i[6]
    cur.execute(f'''INSERT INTO modalities (id, games, noc, year, season, event, athletes_id) VALUES 
                (%s, %s, %s, %s, %s, %s, %s) ''', (id, games, noc, year, season, event, id_athletes))
    conn.commit()

for i in sports:
    sport = i[0]
    noc = i[1]
    id_athletes = i[2]
    cur.execute(f'''INSERT INTO sports (sport, noc, modalities_id) VALUES 
                (%s, %s, %s) ''', (sport, noc, id_athletes))
    conn.commit()

for i in medal:
    medal = i[0]
    noc = i[1]
    athletes_id = i[2]
    modalities_id = i[3]
    cur.execute(f'''INSERT INTO medal (medal, noc, athletes_id, modalities_id) VALUES 
                (%s, %s, %s, %s) ''', (medal, noc, athletes_id, modalities_id))
    conn.commit()

with open(file='cod/noc_regions.csv', mode='r', encoding='utf-8') as file:
    data_region = csv.reader(file)
    next(data_region)
    for row in data_region:
        cur.execute("""
            INSERT INTO region (noc, region, notes)
            VALUES (%s, %s, %s)
            ON CONFLICT ON CONSTRAINT unico_noc_region DO NOTHING;
        """, (row[0], row[1], row[2]))
        conn.commit()
cur.close()
conn.close()