import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('dataset.db')

# Create a cursor object
cursor = conn.cursor()

# Create the propulsion_systems table
cursor.execute('''
CREATE TABLE IF NOT EXISTS electric (
    concept TEXT,
    specific_impulse_sec REAL,
    input_power_kw REAL,
    thrust_power_mN_per_kw REAL,
    specific_mass_kg_per_kw REAL,
    propellant TEXT
)
''')

# Create the propellants table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chemical (
    propellant TEXT,
    nominal_thrust_n REAL,
    specific_impulse_sec REAL,
    operational_life_sec REAL,
    engine_mass_kg REAL
)
''')

# Insert data into the propulsion_systems table
propulsion_data = [
    ('Resistojet', 297.5, 0.7, 824, 1.3, 'N2H4'),
    ('Arcjet (NH3)', 480, 0.85, 135, 3.5, 'NH3'),
    ('Arcjet (N2H4)', 541, 1.985, 125.5, 2.8, 'N2H4'),
    ('Pulsed Plasma Thruster (PPT)', 800, 0.025, 113, 2.5, 'Teflon'),
    ('Hall Effect Thruster (HET)', 1760, 3, 54.77, 6.33, 'Xenon'),
    ('Ion Thruster (IT)', 3084, 0.988, 33.9, 20.68, 'Xenon')
]

cursor.executemany('''
INSERT INTO electric (concept, specific_impulse_sec, input_power_kw, thrust_power_mN_per_kw, specific_mass_kg_per_kw, propellant)
VALUES (?, ?, ?, ?, ?, ?)
''', propulsion_data)

# Insert data into the propellants table
propellants_data = [
    ('N2O4/N2H4', 1713.333333, 322.5, 22667, 4.513333333),
    ('N2O4/MMH', 11333.45455, 317.9, 13164, 40.40909091),
    ('N2O4/A-50', 35600, 315, 1000, 107.95),
    ('MON-3/MMH', 890, 305, 15000, 4.54),
    ('LO2/LH2', 73400, 446, 400, 138.35)
]

cursor.executemany('''
INSERT INTO chemical (propellant, nominal_thrust_n, specific_impulse_sec, operational_life_sec, engine_mass_kg)
VALUES (?, ?, ?, ?, ?)
''', propellants_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()