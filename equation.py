import sqlite3
#spec name array
electric_spec_name = []
chemical_spec_name = []

# Global variable
def initialized():
    conn = sqlite3.connect('dataset.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object

    cursor.execute('PRAGMA table_info(electric)')
    electric_spec = cursor.fetchall()

    #column name electric
    global electric_spec_name
    for column in electric_spec:
        electric_spec_name.append(column[1])

    #remove strings (database specific, could have had added a variable-type filter but it is unecessary in this context)
    electric_spec_name.remove(electric_spec_name[0])
    electric_spec_name.remove(electric_spec_name[4])
    
    print(electric_spec_name)

    cursor.execute('PRAGMA table_info(chemical)')
    chemical_spec = cursor.fetchall()

    global chemical_spec_name 
    for column in chemical_spec:
        chemical_spec_name.append(column[1])

    #remove strings (database specific, could have had added a variable-type filter but it is unecessary in this context)
    chemical_spec_name.remove(chemical_spec_name[0])
    chemical_spec_name.remove(chemical_spec_name[3])

    print(chemical_spec_name)
    
    # Close the connection
    conn.close()
initialized()

def get_row_count(table):
    conn = sqlite3.connect('dataset.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    result = cursor.fetchone()
    
    conn.close()
    
    return float(result[0])

def find_extrema_in_column(table, spec, extrema):
    conn = sqlite3.connect("dataset.db")
    cursor = conn.cursor()
    
    if extrema == "max":
        query = f"SELECT MAX({spec}) FROM {table}"
    elif extrema == "min":
        query = f"SELECT MIN({spec}) FROM {table}"
    else:
        conn.close()
        raise ValueError("extrema must be either 'max' or 'min'")
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return (float(result[0]))   

def find_d_n(table, propulsion_type, spec):
    conn = sqlite3.connect('dataset.db')
    cursor = conn.cursor()
    
    query = f'SELECT {spec} FROM {table} WHERE concept = ?'
    cursor.execute(query, (propulsion_type,))
    result = cursor.fetchone()
    
    conn.close()
    
    return float(result[0]) if result else None

def find_delta_d(table, propulsion_type, spec):
    return find_d_n(table, propulsion_type, spec) - find_extrema_in_column(table, spec, "min")

def find_unit_delta(table, spec):
    return (find_extrema_in_column(table, spec, "max") - find_extrema_in_column(table, spec, "min")) / get_row_count(table)

#delta_d_dataset initialize
unit_delta_data = {
    "electric":{},
    "chemical":{},
}
#calculate delta d dataset
def calculate_delta_d_data():
    global electric_spec_name
    global chemical_spec_name
    # Calculate delta_d_data
    for spec in electric_spec_name:
        unit_delta_data["electric"][spec] = find_unit_delta("electric", spec)
        print(find_unit_delta("electric", spec))
    for row in chemical_spec_name:
        unit_delta_data["chemical"][row] = find_unit_delta("chemical", row)
        print(find_unit_delta("chemical", row))
calculate_delta_d_data()
#find an value
def find_an(table, propulsion_type, spec):
    return find_delta_d(table, propulsion_type, spec) / unit_delta_data[table][spec]


#find an * cn
def find_ancn(table, propulsion_type, spec):
    global weight_data
    return find_an(table, propulsion_type, spec) * weight_data[spec]

#get propulsion system name
def get_propulsion_system_name(table):
    conn = sqlite3.connect("dataset.db")
    cursor = conn.cursor()
    
    query = f"SELECT concept FROM {table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    values = [row[0] for row in rows]
    
    return values

#weight data
weight_data = {
    #electric
    "specific_impulse_electric": 1.5,
    "input_power_electric": 1.5,
    "thrust_to_power_electric": 1.5,
    "thrust_electric": 1.5,
    "specific_mass_electric": 1.5,
    
    #chemical
    "thrust_chemical": 1.5,
    "specific_impulse_chemical": 1.5,
    "operational_life": 15,
    "engine_mass_chemical": 1.5,
    
    #combined
    "multimode_specific_impulse": 1.5,
    "propulsion_system_mass": 1.5,
    "thrust_time": 1.5,
    "system_mass": 1.5,   
}

#list of possible combinations
combination_index = 1
combination_list = {}
def get_list_of_possible_combinations():
    global combination_index
    global combination_list
    for electric_system in  get_propulsion_system_name("electric"):
        for chemical_system in get_propulsion_system_name("chemical"):
            combination_list[combination_index] = [electric_system, chemical_system]
            combination_index += 1
get_list_of_possible_combinations() 
print(combination_list)

#create a dictionary for the sum of an * cn
sum_ancn_data = {}
def find_sum_ancn_data():
    global sum_ancn_data
    for index, value in combination_list.items():
        electric_system, chemical_system = value
        sum_ancn_data[index] = 0
        for spec in electric_spec_name:
            sum_ancn_data[index] += find_ancn("electric", electric_system, spec)
        for spec in chemical_spec_name:
            sum_ancn_data[index] += find_ancn("chemical", chemical_system, spec)
find_sum_ancn_data()


sum_weight = 0
#calculate weight sum
def calculate_sum_weight():
    global sum_weight
    for weight in weight_data.values():
        sum_weight += weight
calculate_sum_weight() 

# Step 1: Create the Database and Table
def create_database_and_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('a_value_data.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create the a_value table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS a_value_table (
        index_id INTEGER PRIMARY KEY,
        a_value REAL,
        electric_type TEXT,
        chemical_type TEXT
    )
    ''')

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
create_database_and_table()
# Step 2: Calculate `a_value` and Store in the Database
def find_A_value_data():
    global combination_list, sum_ancn_data, sum_weight, a_value

    # Initialize a_value dictionary
    a_value = {}

    # Connect to the SQLite database
    conn = sqlite3.connect('a_value_data.db')
    cursor = conn.cursor()

    # Iterate over the combination_list keys and calculate a_value
    for index in combination_list.keys():
        a_value[index] = sum_ancn_data[index] / sum_weight
        chemical_type = combination_list[index][1]
        electric_type = combination_list[index][0]

        # Insert or replace the a_value and chemical_type into the database
        cursor.execute('''
        INSERT OR REPLACE INTO a_value_table (index_id, a_value, electric_type, chemical_type)
        VALUES (?, ?, ?, ?)
        ''', (index, a_value[index], electric_type, chemical_type))

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Step 3: Fetch and Sort Data by `a_value`
def fetch_sorted_a_value_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('a_value_data.db')
    cursor = conn.cursor()

    # Fetch data from the a_value_table sorted by a_value
    cursor.execute('''
    SELECT * FROM a_value_table ORDER BY a_value
    ''')

    sorted_data = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return sorted_data

find_A_value_data()
print(a_value)



    

