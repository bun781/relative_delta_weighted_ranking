import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('dataseet.db')

# Create a cursor object
cursor = conn.cursor()

# Create the propulsion_systems table
cursor.execute('''
CREATE TABLE IF NOT EXISTS electric (
    concept TEXT,
    specific_impulse_electric REAL,
    input_power_electric REAL,
    thrust_to_power_electric REAL,
    thrust_to_mass_electric REAL
)
''')

# Insert data into the propulsion_systems table
propulsion_data = [
    ('Resistojet', 297.5, 0.7, 824, 0.769),
    ('Arcjet (NH3)', 480, 0.85, 135, 0.329),
    ('Arcjet (N2H4)', 541, 1.985, 125.5, 0.286),
    ('Pulsed Plasma Thruster (PPT)', 800, 0.025, 113, 0.007),
    ('Hall Effect Thruster (HET)', 1760, 3, 54.77, 0.154),
    ('Ion Thruster (IT)', 3084, 0.988, 33.9, 0.048)
]

cursor.executemany('''
INSERT INTO electric (concept, specific_impulse_electric, input_power_electric, thrust_to_power_electric, thrust_to_mass_electric)
VALUES (?, ?, ?, ?, ?)
''', propulsion_data)

cursor.execute('''
CREATE TABLE IF NOT EXISTS chemical (
    concept TEXT,
    thrust_chemical REAL,
    engine_mass_chemical REAL,
    specific_impulse_chemical REAL,
    thrust_to_weight_chemical REAL
)
''')
#inverse of weight

# Data to be inserted into the table
chemical_data = [
    ('N2H4 - 1.03', 0.155, 0.15, 210, 1.03),
    ('N2H4 - 0.54', 0.38, 0.7, 302.5, 0.54),
    ('N2H4 - 15.86', 2.22, 0.14, 222.5, 15.86),
    ('N2H4 - 31.79', 4.45, 0.14, 220, 31.79),
    ('N2H4 - 64.58', 15.5, 0.24, 225, 64.58),
    ('N2H4 - 120.83', 29, 0.24, 227.5, 120.83),
    ('N2H4 - 140', 56, 0.4, 227.5, 140.00),
    ('N2H4 - 71.61', 111, 1.55, 227.5, 71.61),
    ('N2H4 - 53.20', 133, 2.5, 233.5, 53.20),
    ('N2H4 - 125', 200, 1.6, 233, 125.00),
    ('N2H4 - 276.59', 567, 2.05, 235, 276.59),
    ('N2H4 - 118.14', 1335, 11.3, 235, 118.14),
    ('N2H4 - 329.15', 2699, 8.2, 233, 329.15),
    ('N2O4/CH6N2 - 22.00', 11, 0.5, 285, 22.00),
    ('N2O4/CH6N2 - 31.43', 22, 0.7, 290, 31.43),
    ('N2O4/CH6N2 - 79.29', 111, 1.4, 300, 79.29),
    ('N2O4/CH6N2 - 108.41', 445, 4.1, 308, 108.41),
    ('N2O4/CH6N2 - 100', 450, 4.5, 305, 100.00),
    ('N2O4/CH6N2 - 97.78', 440, 4.5, 325, 97.78),
    ('N2O4/CH6N2 - 118.24', 450, 3.8, 309, 118.42),
    ('N2O4/N2H4 - 98.89', 445, 4.5, 322, 98.89),
    ('N2O4/N2H5 - 80.00', 440, 5.5, 330, 80.00),
    ('N2O4/N2H6 - 112.50', 450, 4, 317, 112.50)
]

# Insert data into the table
cursor.executemany('''
INSERT INTO chemical (concept, thrust_chemical, engine_mass_chemical, specific_impulse_chemical, thrust_to_weight_chemical)
VALUES (?, ?, ?, ?, ?)
''', chemical_data)



# Commit the transaction
conn.commit()

# Close the connection
conn.close()
