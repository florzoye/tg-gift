
def get_info_table_sql(name: str) -> str:
    return f"""
    CREATE TABLE IF NOT EXISTS {name} (
        NameGift TEXT NOT NULL,
        GiftID TEXT PRIMARY KEY,
        FloorPrice REAL,
    )
    """


def get_create_table_sql(table_name: str) -> str:
    return f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id TEXT,
        source TEXT,  -- 🆕 Добавили
        NameColl TEXT NOT NULL,
        PricePortal REAL NOT NULL,
        PriceMRKT REAL NOT NULL,
        SpreadMRKTtoPORTAL REAL,
        SpreadPORTALtoMRKT REAL,
        SpreadDiffTON REAL,
        SpreadDiffPercent REAL,
        TotalProfit REAL
    )
    """


def get_insert_spread_sql(table_name: str) -> str:
    return f"""
    INSERT INTO {table_name} (
        id, source, NameColl, PricePortal, PriceMRKT, 
        SpreadMRKTtoPORTAL, SpreadPORTALtoMRKT,
        SpreadDiffTON, SpreadDiffPercent, TotalProfit
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """


def get_select_all_sql(table_name: str) -> str:
    return f"SELECT * FROM {table_name}"

def get_select_max_profit_sql(table_name: str) -> str:
    return f"SELECT * FROM {table_name} ORDER BY SpreadDiffPercent DESC LIMIT 1"


def get_info_table_sql(table_name: str) -> str:
    return f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id TEXT NOT NULL,
        name TEXT NOT NULL,
        FloorPrice REAL NOT NULL
    )
    """

def get_select_id_by_floor_price_sql(table_name: str) -> str:
    return f"SELECT id FROM {table_name} WHERE FloorPrice = ?"

def get_update_info_sql(table_name: str) -> str:
    return f"""
    UPDATE {table_name} 
    SET id = :id, name = :name
    WHERE FloorPrice = :FloorPrice
    """

def get_insert_info_sql(table_name: str) -> str:
    return f"""
    INSERT INTO {table_name} (id, name, FloorPrice)
    VALUES (:id, :name, :FloorPrice)
    """

def get_select_column_sql(table_name: str, column_name: str) -> str:
    return f"SELECT {column_name} FROM {table_name}"

