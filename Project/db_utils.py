# db_utils.py
def get_oracle_connection_string():
    db_username = "m"
    db_password = "00"
    db_host = "localhost"
    db_port = "1521"
    db_service_name = "XE"  # Assuming XE is the service name based on your tnsnames.ora

    return f"{db_username}/{db_password}@{db_host}:{db_port}/{db_service_name}"
