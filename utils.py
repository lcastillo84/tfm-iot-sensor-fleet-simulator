from datetime import datetime


def get_timestamp() -> str:
    "Función utilitaria. Genera una cadena de texto con marca temporal actual"
    return datetime.now().isoformat(timespec='milliseconds')


def read_sequence(filename: str) -> int:
    "Lee archivo de secuencia y devuelve el valor numérico"
    with open(filename) as f:
        current_seq_value = f.readline()
    return int(current_seq_value)


def update_sequence(
        filename: str,
        current_seq_value: int,
        max_seq_nbr: int) -> None:
    "Actualiza el archivo de secuencia"
    with open(filename, 'w') as f:
        new_seq_value = current_seq_value + 1
        if new_seq_value > max_seq_nbr:
            new_seq_value = 0
        f.write(str(new_seq_value))
