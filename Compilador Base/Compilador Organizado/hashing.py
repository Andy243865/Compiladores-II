import hashlib
from lexer import hash_table

def generate_hash(value):
    """Genera un hash SHA-256 para un valor dado."""
    return hashlib.sha256(str(value).encode()).hexdigest()

def update_variable_hash(var_name, value):
    """Actualiza el hash de una variable cuando se le asigna un valor."""
    if value != 'undefined':
        if var_name not in hash_table:
            hash_table[var_name] = []
        
        hash_value = generate_hash(value)
        hash_table[var_name].append({'value': value, 'hash': hash_value})
    else:
        hash_table.pop(var_name, None)
