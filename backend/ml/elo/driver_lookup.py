from dataclasses import dataclass

@dataclass(frozen=True)
class DriverInfo:
    driver_name: str
    display_number: str
    canonical_driver_number: str

PERMANENT_DRIVER_LOOKUP = {
    "2": DriverInfo(driver_name="Logan Sargeant", display_number="2", canonical_driver_number="2"),
    "3": DriverInfo(driver_name="Daniel Ricciardo", display_number="3", canonical_driver_number="3"),
    "4": DriverInfo(driver_name="Lando Norris", display_number="4", canonical_driver_number="4"),
    "5": DriverInfo(driver_name="Sebastian Vettel", display_number="5", canonical_driver_number="5"),
    "6": DriverInfo(driver_name="Nicholas Latifi", display_number="6", canonical_driver_number="6"),
    "7": DriverInfo(driver_name="Kimi Räikkönen", display_number="7", canonical_driver_number="7"),
    "8": DriverInfo(driver_name="Romain Grosjean", display_number="8", canonical_driver_number="8"),
    "9": DriverInfo(driver_name="Nikita Mazepin", display_number="9", canonical_driver_number="9"),
    "10": DriverInfo(driver_name="Pierre Gasly", display_number="10", canonical_driver_number="10"),
    "11": DriverInfo(driver_name="Sergio Pérez", display_number="11", canonical_driver_number="11"),
    "14": DriverInfo(driver_name="Fernando Alonso", display_number="14", canonical_driver_number="14"),
    "16": DriverInfo(driver_name="Charles Leclerc", display_number="16", canonical_driver_number="16"),
    "18": DriverInfo(driver_name="Lance Stroll", display_number="18", canonical_driver_number="18"),
    "20": DriverInfo(driver_name="Kevin Magnussen", display_number="20", canonical_driver_number="20"),
    "21": DriverInfo(driver_name="Nyck de Vries", display_number="21", canonical_driver_number="21"),
    "22": DriverInfo(driver_name="Yuki Tsunoda", display_number="22", canonical_driver_number="22"),
    "23": DriverInfo(driver_name="Alexander Albon", display_number="23", canonical_driver_number="23"),
    "24": DriverInfo(driver_name="Guanyu Zhou", display_number="24", canonical_driver_number="24"),
    "26": DriverInfo(driver_name="Daniil Kvyat", display_number="26", canonical_driver_number="26"),
    "27": DriverInfo(driver_name="Nico Hülkenberg", display_number="27", canonical_driver_number="27"),
    "28": DriverInfo(driver_name="Brendon Hartley", display_number="28", canonical_driver_number="28"),
    "30": DriverInfo(driver_name="Liam Lawson", display_number="30", canonical_driver_number="30"),
    "31": DriverInfo(driver_name="Esteban Ocon", display_number="31", canonical_driver_number="31"),
    "33": DriverInfo(driver_name="Max Verstappen", display_number="33", canonical_driver_number="33"),
    "35": DriverInfo(driver_name="Sergey Sirotkin", display_number="35", canonical_driver_number="35"),
    "43": DriverInfo(driver_name="Franco Colapinto", display_number="43", canonical_driver_number="43"),
    "44": DriverInfo(driver_name="Lewis Hamilton", display_number="44", canonical_driver_number="44"),
    "47": DriverInfo(driver_name="Mick Schumacher", display_number="47", canonical_driver_number="47"),
    "55": DriverInfo(driver_name="Carlos Sainz", display_number="55", canonical_driver_number="55"),
    "63": DriverInfo(driver_name="George Russell", display_number="63", canonical_driver_number="63"),
    "77": DriverInfo(driver_name="Valtteri Bottas", display_number="77", canonical_driver_number="77"),
    "81": DriverInfo(driver_name="Oscar Piastri", display_number="81", canonical_driver_number="81"),
    "87": DriverInfo(driver_name="Oliver Bearman", display_number="87", canonical_driver_number="87"),
    "88": DriverInfo(driver_name="Robert Kubica", display_number="88", canonical_driver_number="88"),
    "99": DriverInfo(driver_name="Antonio Giovinazzi", display_number="99", canonical_driver_number="99"),
}

TEMPORARY_DRIVER_LOOKUP = {
    # Championship Number Assignments
    (2022, "1"): DriverInfo(driver_name="Max Verstappen", display_number="1", canonical_driver_number="33"),
    (2023, "1"): DriverInfo(driver_name="Max Verstappen", display_number="1", canonical_driver_number="33"),
    (2024, "1"): DriverInfo(driver_name="Max Verstappen", display_number="1", canonical_driver_number="33"),
    
    # Reserve/Stand-in Number Assignments
    (2024, "38"): DriverInfo(driver_name="Oliver Bearman", display_number="38", canonical_driver_number="87"), # Ferrari reserve
    (2024, "50"): DriverInfo(driver_name="Oliver Bearman", display_number="50", canonical_driver_number="87"), # Haas reserve
    (2023, "40"): DriverInfo(driver_name="Liam Lawson", display_number="40", canonical_driver_number="30"), # AlphaTauri reserve
    (2022, "45"): DriverInfo(driver_name="Nyck de Vries", display_number="45", canonical_driver_number="21"), # Williams reserve
    (2020, "51"): DriverInfo(driver_name="Pietro Fittipaldi", display_number="51", canonical_driver_number="51"), # Haas reserve
    (2020, "89"): DriverInfo(driver_name="Jack Aitken", display_number="89", canonical_driver_number="89"), # Williams reserve
    (2024, "61"): DriverInfo(driver_name="Jack Doohan", display_number="61", canonical_driver_number="7"), # Alpine practice/reserve
}
def get_driver_info(
    season: int,
    driver_number: str,
) -> DriverInfo:

    key = (
        int(season),
        str(driver_number),
    )

    if key in TEMPORARY_DRIVER_LOOKUP:

        return TEMPORARY_DRIVER_LOOKUP[
            key
        ]

    if str(driver_number) in PERMANENT_DRIVER_LOOKUP:

        return PERMANENT_DRIVER_LOOKUP[
            str(driver_number)
        ]

    raise KeyError(
        f"Unknown driver number "
        f"{driver_number} "
        f"for season {season}"
    )