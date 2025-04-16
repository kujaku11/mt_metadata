# ===============================================================
# imports
# ===============================================================
from loguru import logger
import numpy as np
from enum import Enum

# ===============================================================


def convert_position_float2str(position: float) -> str:
    """
    Convert position float to a string in the format of DD:MM:SS.ms

    Parameters
    ----------
    position : float
        decimal degrees of latitude or longitude

    Returns
    -------
    str
        latitude or longitude in format of DD:MM:SS.ms
    """

    assert type(position) is float, "Given value is not a float"

    deg = int(position)
    sign = 1
    if deg < 0:
        sign = -1

    deg = abs(deg)
    minutes = (abs(position) - deg) * 60.0
    # need to round seconds to 4 decimal places otherwise machine precision
    # keeps the 60 second roll over and the string is incorrect.
    sec = np.round((minutes - int(minutes)) * 60.0, 4)
    if sec >= 60.0:
        minutes += 1
        sec = 0

    if int(minutes) == 60:
        deg += 1
        minutes = 0

    position_str = f"{sign * int(deg)}:{int(minutes):02.0f}:{sec:05.2f}"
    logger.debug(f"Converted {position} to {position_str}")

    return position_str


def convert_position_str2float(position_str: str) -> float:
    """
    Convert a position string in the format of DD:MM:SS to decimal degrees

    :param position: latitude or longitude om DD:MM:SS.ms
    :type position: float

    :returns: latitude or longitude as a float

    Parameters
    ----------
    position_str : str
        latitude or longitude om DD:MM:SS.ms

    Returns
    -------
    float
        latitude or longitude as a float

    Raises
    ------
    ValueError
        If position string cannot be converted to a float or
        if the format is incorrect.
    """

    if position_str in [None, "None"]:
        return 0.0

    p_list = position_str.split(":")
    if len(p_list) != 3:
        msg = f"{position_str} not correct format, should be DD:MM:SS"
        logger.error(msg)
        raise ValueError(msg)

    deg = float(p_list[0])
    minutes = _assert_minutes(float(p_list[1]))
    sec = _assert_seconds(float(p_list[2]))

    # get the sign of the position so that when all are added together the
    # position is in the correct place
    sign = 1
    if deg < 0:
        sign = -1

    position_value = sign * (abs(deg) + minutes / 60.0 + sec / 3600.0)

    logger.debug(f"Converted {position_str} to {position_value}")

    return position_value


def _assert_minutes(minutes: float | int) -> float:
    """
    Assert minutes are between 0 and 60

    Parameters
    ----------
    minutes : float | int
        number of minutesto be checked

    Returns
    -------
    float
        number of minutes if valid
    """
    if not 0 <= minutes < 60.0:
        msg = (
            f"minutes should be 0 < > 60, currently {minutes:.0f} "
            "conversion will account for non-uniform "
            "time. Be sure to check accuracy."
        )
        logger.warning(msg)

    return minutes


def _assert_seconds(seconds: float | int) -> float:
    """
    Assert seconds are between 0 and 60

    Parameters
    ----------
    seconds : float | int
        number of seconds to be checked

    Returns
    -------
    float
        number of seconds if valid
    """
    if not 0 <= seconds < 60.0:
        msg = (
            f"seconds should be 0 < > 60, currently {seconds:.0f} "
            "conversion will account for non-uniform "
            "time. Be sure to check accuracy."
        )
        logger.warning(msg)

    return seconds


def validate_position(value: str | float, position_type: str) -> float:
    """
    Validate position value (latitude or longitude) and convert to float.

    Parameters
    ----------
    value : str | float
        The position value to validate and convert.
    position_type : str
        The type of position ('latitude' or 'longitude').

    Returns
    -------
    float
        The validated and converted position value.

    Raises
    ------
    ValueError
        If the value is not a valid latitude or longitude.
    """
    if position_type not in ["latitude", "longitude"]:
        raise ValueError("position_type must be 'latitude' or 'longitude'")

    if isinstance(value, str) and ":" in value:
        value = convert_position_str2float(value)
    else:
        try:
            value = float(value)
        except ValueError:
            raise ValueError("latitude and longitude must be float or str")

    if not (abs(value) <= 90) and position_type in ["latitude", "lat"]:
        raise ValueError("latitude must be between -90 and 90 degrees")
    if not (abs(value) <= 180) and position_type in ["longitude", "lon"]:
        raise ValueError("longitude must be between -180 and 180 degrees")
    return value


class DatumEnum(str, Enum):
    """
    Enum of datums for use in the metadata model.

    This is a list of datums used in the metadata model. It is not an exhaustive list.
    """

    # List of datums
    Airy_1830 = "Airy 1830"
    Airy_Modified_1849 = "Airy Modified 1849"
    Australian_National_Spheroid = "Australian National Spheroid"
    Authalic_Sphere = "Authalic Sphere"
    Average_Terrestrial_System_1977 = "Average Terrestrial System 1977"
    Bessel_1841 = "Bessel 1841"
    Bessel_Modified = "Bessel Modified"
    Bessel_Namibia = "Bessel Namibia"
    Clarke_1858 = "Clarke 1858"
    Clarke_1866 = "Clarke 1866"
    Clarke_1866_Michigan = "Clarke 1866 Michigan"
    Clarke_1880_Arc = "Clarke 1880 (Arc)"
    Clarke_1880_Benoit = "Clarke 1880 (Benoit)"
    Clarke_1880_IGN = "Clarke 1880 (IGN)"
    Clarke_1880_RGS = "Clarke 1880 (RGS)"
    Clarke_1880_SGA_1922 = "Clarke 1880 (SGA 1922)"
    Clarke_1880 = "Clarke 1880"
    Everest_1830_Definition = "Everest (1830 Definition)"
    Everest_1830_1937_Adjustment = "Everest 1830 (1937 Adjustment)"
    Everest_1830_1962_Definition = "Everest 1830 (1962 Definition)"
    Everest_1830_1967_Definition = "Everest 1830 (1967 Definition)"
    Everest_1830_1975_Definition = "Everest 1830 (1975 Definition)"
    Everest_1830_Modified = "Everest 1830 Modified"
    GEM10C = "GEM10C"
    GRS67 = "GRS67"
    GRS80 = "GRS80"
    Helmert_1906 = "Helmert 1906"
    Indonesian_National_Spheroid = "Indonesian National Spheroid"
    International_1924 = "International 1924"
    Krassowsky_1940 = "Krassowsky 1940"
    NWL9D = "NWL9D"
    OSU86F = "OSU86F"
    OSU91A = "OSU91A"
    Plessis_1817 = "Plessis 1817"
    Struve_1860 = "Struve 1860"
    War_Office_ellipsoid = "War Office ellipsoid"
    NAD27 = "NAD27"
    NAD27_Carribbean = "NAD27 Carribbean"
    NAD27_Central_America_East = "NAD27 Central America - East"
    NAD27_Central_America_West = "NAD27 Central America - West"
    NAD27_Conus = "NAD27 Conus"
    NAD27_Cuba = "NAD27 Cuba"
    NAD27_Greenland = "NAD27 Greenland"
    NAD27_Hawaii = "NAD27 Hawaii"
    NAD27_Hawaii_NADCON = "NAD27 Hawaii (NADCON)"
    NAD27_Mexico = "NAD27 Mexico"
    NAD27_Michigan = "NAD27 Michigan"
    NAD27_Old_Hawaiian = "NAD27 Old Hawaiian"
    NAD27_Old_Hawaiian_Hawaii = "NAD27 Old Hawaiian - Hawaii"
    NAD27_Old_Hawaiian_Kauai = "NAD27 Old Hawaiian - Kauai"
    NAD27_Old_Hawaiian_Maui = "NAD27 Old Hawaiian - Maui"
    NAD27_Old_Hawaiian_Oahu = "NAD27 Old Hawaiian - Oahu"
    NAD27_Puerto_Rico_and_Virgin_Islands_NADCON = (
        "NAD27 Puerto Rico and Virgin Islands (NADCON)"
    )
    NAD27_San_Salvador = "NAD27 San Salvador"
    NAD27_St_George_NADCON = "NAD27 St. George (NADCON)"
    NAD27_St_Lawrence_NADCON = "NAD27 St. Lawrence (NADCON)"
    NAD27_St_Paul_NADCON = "NAD27 St. Paul (NADCON)"
    NAD27_United_States_Eastern = "NAD27 United States - Eastern"
    NAD27_United_States_Western = "NAD27 United States - Western"
    NAD27_76 = "NAD27(76)"
    NAD27_CGQ77 = "NAD27(CGQ77)"
    NAD83 = "NAD83"
    NAD83_Alabama_HARN = "NAD83 Alabama (HARN)"
    NAD83_Arizona_HARN = "NAD83 Arizona (HARN)"
    NAD83_Arkansas_HARN = "NAD83 Arkansas (HARN)"
    NAD83_California_North_HARN = "NAD83 California - North (HARN)"
    NAD83_California_South_HARN = "NAD83 California - South (HARN)"
    NAD83_Colorado_HARN = "NAD83 Colorado (HARN)"
    NAD83_Connecticut_HARN = "NAD83 Connecticut (HARN)"
    NAD83_Florida_HARN = "NAD83 Florida (HARN)"
    NAD83_Georgia_HARN = "NAD83 Georgia (HARN)"
    NAD83_Hawaii_HARN = "NAD83 Hawaii (HARN)"
    NAD83_Idaho_and_Montana_East_HARN = "NAD83 Idaho and Montana - East (HARN)"
    NAD83_Idaho_and_Montana_West_HARN = "NAD83 Idaho and Montana - West (HARN)"
    NAD83_Illinois_HARN = "NAD83 Illinois (HARN)"
    NAD83_Indiana_HARN = "NAD83 Indiana (HARN)"
    NAD83_Iowa_HARN = "NAD83 Iowa (HARN)"
    NAD83_Kansas_HARN = "NAD83 Kansas (HARN)"
    NAD83_Kentucky_HARN = "NAD83 Kentucky (HARN)"
    NAD83_Louisiana_HARN = "NAD83 Louisiana (HARN)"
    NAD83_Maine_HARN = "NAD83 Maine (HARN)"
    NAD83_Maryland_and_Delaware_HARN = "NAD83 Maryland and Delaware (HARN)"
    NAD83_Massachusetts_HARN = "NAD83 Massachusetts (HARN)"
    NAD83_Michigan_HARN = "NAD83 Michigan (HARN)"
    NAD83_Minnesota_HARN = "NAD83 Minnesota (HARN)"
    NAD83_Mississippi_HARN = "NAD83 Mississippi (HARN)"
    NAD83_Montana_HARN = "NAD83 Montana (HARN)"
    NAD83_Nebreska_HARN = "NAD83 Nebreska (HARN)"
    NAD83_Nevada_HARN = "NAD83 Nevada (HARN)"
    NAD83_New_England_HARN = "NAD83 New England (HARN)"
    NAD83_New_Hampshire_HARN = "NAD83 New Hampshire (HARN)"
    NAD83_New_Jersey_HARN = "NAD83 New Jersey (HARN)"
    NAD83_New_Mexico_HARN = "NAD83 New Mexico (HARN)"
    NAD83_New_York_HARN = "NAD83 New York (HARN)"
    NAD83_North_Carolina_HARN = "NAD83 North Carolina (HARN)"
    NAD83_North_Dakota_HARN = "NAD83 North Dakota (HARN)"
    NAD83_Ohio_HARN = "NAD83 Ohio (HARN)"
    NAD83_Oklahoma_HARN = "NAD83 Oklahoma (HARN)"
    NAD83_Pennsylvania_HARN = "NAD83 Pennsylvania (HARN)"
    NAD83_Puerto_Rico_and_Virgin_Islands_HARN = (
        "NAD83 Puerto Rico and Virgin Islands (HARN)"
    )
    NAD83_Rhode_Island_HARN = "NAD83 Rhode Island (HARN)"
    NAD83_South_Carolina_HARN = "NAD83 South Carolina (HARN)"
    NAD83_South_Dakota_HARN = "NAD83 South Dakota (HARN)"
    NAD83_Tennessee_HARN = "NAD83 Tennessee (HARN)"
    NAD83_Texas_East_HARN = "NAD83 Texas - East (HARN)"
    NAD83_Texas_West_HARN = "NAD83 Texas - West (HARN)"
    NAD83_Utah_HARN = "NAD83 Utah (HARN)"
    NAD83_Vermont_HARN = "NAD83 Vermont (HARN)"
    NAD83_Virginia_HARN = "NAD83 Virginia (HARN)"
    NAD83_Washington_and_Oregon_HARN = "NAD83 Washington and Oregon (HARN)"
    NAD83_West_Virginia_HARN = "NAD83 West Virginia (HARN)"
    NAD83_Wisconsin_HARN = "NAD83 Wisconsin (HARN)"
    NAD83_Wyoming_HARN = "NAD83 Wyoming (HARN)"
    NAD83_2011 = "NAD83(2011)"
    NAD83_CORS96 = "NAD83(CORS96)"
    NAD83_CSRS = "NAD83(CSRS)"
    NAD83_CSRS98 = "NAD83(CSRS98)"
    NAD83_HARN = "NAD83(HARN)"
    NAD83_MA11 = "NAD83(MA11)"
    NAD83_NSRS2007 = "NAD83(NSRS2007)"
    NAD83_PA11 = "NAD83(PA11)"
    Nahrwan_Oman = "Nahrwan (Oman)"
    Nahrwan_Saudi_Arabia = "Nahrwan (Saudi Arabia)"
    Nahrwan_United_Arab_Emirates = "Nahrwan (United Arab Emirates)"
    Nahrwan_1934 = "Nahrwan 1934"
    Nahrwan_1967 = "Nahrwan 1967"
    Nakhl_e_Ghanem = "Nakhl-e Ghanem"
    Naparima_1955 = "Naparima 1955"
    Naparima_1972 = "Naparima 1972"
    NDG_Paris = "NDG (Paris)"
    NEA74_Noumea = "NEA74 Noumea"
    Nepal_1981 = "Nepal 1981"
    New_Beijing = "New Beijing"
    NGN = "NGN"
    NGO_1948 = "NGO 1948"
    NGO_1948_Oslo = "NGO 1948 (Oslo)"
    Nord_Sahara_1959 = "Nord Sahara 1959"
    Nord_Sahara_1959_Paris = "Nord Sahara 1959 (Paris)"
    Nouakchott_1965 = "Nouakchott 1965"
    NSWC_9Z_2 = "NSWC 9Z-2"
    NTF = "NTF"
    NTF_NTv2 = "NTF (NTv2)"
    NTF_Paris = "NTF (Paris)"
    NTF_Paris_NTv2 = "NTF (Paris) (NTv2)"
    NZGD2000 = "NZGD2000"
    NZGD49 = "NZGD49"
    NZGD49_NTv2 = "NZGD49 (NTv2)"
    Observatario = "Observatario"
    Ocotepeque_1935 = "Ocotepeque 1935"
    Old_Hawaiian = "Old Hawaiian"
    OS_SN_80 = "OS(SN)80"
    OSGB_1936 = "OSGB 1936"
    OSGB_1936_NTv2 = "OSGB 1936 - NTv2"
    OSGB70 = "OSGB70"
    OSNI_1952 = "OSNI 1952"
    Ouvea_Iles_Loyaute = "Ouvea - Iles Loyaute (MHNC 1972 - OUVEA)"
    Padang = "Padang"
    Padang_Jakarta = "Padang (Jakarta)"
    Palestine_1923 = "Palestine 1923"
    Pampa_del_Castillo = "Pampa del Castillo"
    Panama_Colon_1911 = "Panama-Colon 1911"
    PD_83 = "PD/83"
    Perroud_1950 = "Perroud 1950"
    Peru96 = "Peru96"
    Petrels_1972 = "Petrels 1972"
    Phoenix_Islands_1966 = "Phoenix Islands 1966"
    Pico_de_las_Nieves_1984 = "Pico de las Nieves 1984"
    Pitcairn_1967 = "Pitcairn 1967"
    Pitcairn_2006 = "Pitcairn 2006"
    PNG94 = "PNG94"
    Point_58 = "Point 58"
    Pointe_Geologie_Perroud_1950 = "Pointe Geologie - Perroud 1950"
    Pointe_Noire = "Pointe Noire"
    Popular_Visualisation_CRS = "Popular Visualisation CRS"
    Porto_Santo_1936 = "Porto Santo 1936"
    Porto_Santo_1995 = "Porto Santo 1995"
    POSGAR = "POSGAR"
    POSGAR_2007 = "POSGAR 2007"
    POSGAR_94 = "POSGAR 94"
    POSGAR_98 = "POSGAR 98"
    Principe = "Principe"
    PRS92 = "PRS92"
    PSAD56 = "PSAD56"
    PSD93 = "PSD93"
    PTRA08 = "PTRA08"
    Puerto_Rico = "Puerto Rico"
    Pulkovo_1942 = "Pulkovo 1942"
    Pulkovo_1942_58 = "Pulkovo 1942(58)"
    Pulkovo_1942_83 = "Pulkovo 1942(83)"
    Pulkovo_1995 = "Pulkovo 1995"
    PZ_90 = "PZ-90"
    Qatar_1948 = "Qatar 1948"
    Qatar_1974 = "Qatar 1974"
    QND95 = "QND95"
    Qornoq = "Qornoq"
    Qornoq_1927 = "Qornoq 1927"
    Rassadiran = "Rassadiran"
    RD_83 = "RD/83"
    RDN2008 = "RDN2008"
    REGCAN95 = "REGCAN95"
    REGVEN = "REGVEN"
    Reunion_1947 = "Reunion 1947"
    Reykjavik_1900 = "Reykjavik 1900"
    RGAF09 = "RGAF09"
    RGF93 = "RGF93"
    RGFG95 = "RGFG95"
    RGM04 = "RGM04"
    RGNC_1991 = "RGNC 1991"
    RGNC91_93 = "RGNC91-93"
    RGPF = "RGPF"
    RGR92 = "RGR92"
    RGRDC_2005 = "RGRDC 2005"
    RGSPM06 = "RGSPM06"
    RRAF_1991 = "RRAF 1991"
    RSRGD2000 = "RSRGD2000"
    RT38 = "RT38"
    RT38_Stockholm = "RT38 (Stockholm)"
    RT90 = "RT90"
    SAD69 = "SAD69"
    SAD69_Argentina = "SAD69 (Argentina)"
    SAD69_Baltra_Galapagos = "SAD69 (Baltra, Galapagos)"
    SAD69_Bolivia = "SAD69 (Bolivia)"
    SAD69_Brazil = "SAD69 (Brazil)"
    SAD69_Chile = "SAD69 (Chile)"
    SAD69_Colombia = "SAD69 (Colombia)"
    SAD69_Ecuador = "SAD69 (Ecuador)"
    SAD69_Guyana = "SAD69 (Guyana)"
    SAD69_IBGE1989 = "SAD69 (IBGE1989)"
    SAD69_IBGE2005 = "SAD69 (IBGE2005)"
    SAD69_Paraguay = "SAD69 (Paraguay)"
    SAD69_Peru = "SAD69 (Peru)"
    SAD69_Trinidad_and_Tobago = "SAD69 (Trinidad and Tobago)"
    SAD69_Venezuela = "SAD69 (Venezuela)"
    SAD69_96 = "SAD69(96)"
    Saint_Pierre_et_Miquelon_1950 = "Saint Pierre et Miquelon 1950"
    Samboja = "Samboja"
    Santo_1965 = "Santo 1965"
    Sao_Tome = "Sao Tome"
    Sapper_Hill_1943 = "Sapper Hill 1943"
    Schwarzeck = "Schwarzeck"
    Scoresbysund_1952 = "Scoresbysund 1952"
    Segara = "Segara"
    Segara_Jakarta = "Segara (Jakarta)"
    Segora = "Segora"
    Selvagem_Grande = "Selvagem Grande"
    Serindung = "Serindung"
    Sibun_Gorge_1922 = "Sibun Gorge 1922"
    Sierra_Leone_1960 = "Sierra Leone (1960)"
    Sierra_Leone_1924 = "Sierra Leone 1924"
    Sierra_Leone_1968 = "Sierra Leone 1968"
    Sint_Maarten_Datum_of_1949 = "Sint Maarten Datum of 1949"
    SIRGAS_1995 = "SIRGAS 1995"
    SIRGAS_2000 = "SIRGAS 2000"
    SIRGAS_ES2007_8 = "SIRGAS_ES2007.8"
    SIRGAS_Chile = "SIRGAS-Chile"
    SIRGAS_ROU98 = "SIRGAS-ROU98"
    S_JTSK = "S-JTSK"
    S_JTSK_Ferro = "S-JTSK (Ferro)"
    S_JTSK_05 = "S-JTSK/05"
    S_JTSK_05_Ferro = "S-JTSK/05 (Ferro)"
    SLD99_Sri_Lanka_Datum_1999 = "SLD99 (Sri Lanka Datum 1999)"
    Slovenia_1996 = "Slovenia 1996"
    Solomon_1968_DOS_1968 = "Solomon 1968 (DOS 1968)"
    South_Asia = "South Asia"
    South_East_Asia = "South East Asia"
    South_East_Island_1943 = "South East Island 1943"
    South_Georgia_1968 = "South Georgia 1968"
    South_Yemen = "South Yemen"
    SREF98 = "SREF98"
    St_George_Island = "St. George Island"
    St_Helena_1971 = "St. Helena 1971"
    St_Kitts_1955 = "St. Kitts 1955"
    St_Lawrence_Island = "St. Lawrence Island"
    St_Lucia_1955 = "St. Lucia 1955"
    St_Paul_Island = "St. Paul Island"
    St_Vincent_1945 = "St. Vincent 1945"
    ST71_Belep = "ST71 Belep"
    ST84_Ile_des_Pins = "ST84 Ile des Pins"
    ST87_Ouvea = "ST87 Ouvea"
    strDatum = "strDatum"
    Sudan = "Sudan"
    SVY21 = "SVY21"
    SWEREF99 = "SWEREF99"
    Tahaa_54 = "Tahaa 54"
    Tahiti_52 = "Tahiti 52"
    Tahiti_79 = "Tahiti 79"
    Tananarive = "Tananarive"
    Tananarive_Paris = "Tananarive (Paris)"
    TC_1948 = "TC(1948)"
    Tern_Island_1961 = "Tern Island 1961"
    Tete = "Tete"
    TGD2005 = "TGD2005"
    Timbalai_1948 = "Timbalai 1948"
    TM65 = "TM65"
    TM75 = "TM75"
    Tokyo_1892 = "Tokyo 1892"
    Tokyo_1898 = "Tokyo 1898"
    Tokyo_1918 = "Tokyo 1918"
    Trinidad_1903 = "Trinidad 1903"
    Tristan_1968 = "Tristan 1968"
    TUREF = "TUREF"
    TWD67 = "TWD67"
    TWD97 = "TWD97"
    UCS2000 = "UCS2000"
    Ukraine_2000 = "Ukraine 2000"
    Unknown_datum_Airy_1830 = "Unknown datum based upon the Airy 1830 ellipsoid"
    Unknown_datum_Airy_Modified_1849 = (
        "Unknown datum based upon the Airy Modified 1849 ellipsoid"
    )
    Unknown_datum_Australian_National_Spheroid = (
        "Unknown datum based upon the Australian National Spheroid"
    )
    Unknown_datum_Authalic_Sphere = "Unknown datum based upon the Authalic Sphere"
    Unknown_datum_Average_Terrestrial_System_1977 = (
        "Unknown datum based upon the Average Terrestrial System 1977 ellipsoid"
    )
    Unknown_datum_Bessel_1841 = "Unknown datum based upon the Bessel 1841 ellipsoid"
    Unknown_datum_Bessel_Modified = (
        "Unknown datum based upon the Bessel Modified ellipsoid"
    )
    Unknown_datum_Bessel_Namibia = (
        "Unknown datum based upon the Bessel Namibia ellipsoid"
    )
    Unknown_datum_Clarke_1858 = "Unknown datum based upon the Clarke 1858 ellipsoid"
    Unknown_datum_Clarke_1866 = "Unknown datum based upon the Clarke 1866 ellipsoid"
    Unknown_datum_Clarke_1866_Michigan = (
        "Unknown datum based upon the Clarke 1866 Michigan ellipsoid"
    )
    Unknown_datum_Clarke_1880_Arc = (
        "Unknown datum based upon the Clarke 1880 (Arc) ellipsoid"
    )
    Unknown_datum_Clarke_1880_Benoit = (
        "Unknown datum based upon the Clarke 1880 (Benoit) ellipsoid"
    )
    Unknown_datum_Clarke_1880_IGN = (
        "Unknown datum based upon the Clarke 1880 (IGN) ellipsoid"
    )
    Unknown_datum_Clarke_1880_RGS = (
        "Unknown datum based upon the Clarke 1880 (RGS) ellipsoid"
    )
    Unknown_datum_Clarke_1880_SGA_1922 = (
        "Unknown datum based upon the Clarke 1880 (SGA 1922) ellipsoid"
    )
    Unknown_datum_Clarke_1880 = "Unknown datum based upon the Clarke 1880 ellipsoid"
    Unknown_datum_Everest_1830_Definition = (
        "Unknown datum based upon the Everest (1830 Definition) ellipsoid"
    )
    Unknown_datum_Everest_1830_1937_Adjustment = (
        "Unknown datum based upon the Everest 1830 (1937 Adjustment) ellipsoid"
    )
    Unknown_datum_Everest_1830_1962_Definition = (
        "Unknown datum based upon the Everest 1830 (1962 Definition) ellipsoid"
    )
    Unknown_datum_Everest_1830_1967_Definition = (
        "Unknown datum based upon the Everest 1830 (1967 Definition) ellipsoid"
    )
    Unknown_datum_Everest_1830_1975_Definition = (
        "Unknown datum based upon the Everest 1830 (1975 Definition) ellipsoid"
    )
    Unknown_datum_Everest_1830_Modified = (
        "Unknown datum based upon the Everest 1830 Modified ellipsoid"
    )
    Unknown_datum_GEM10C = "Unknown datum based upon the GEM 10C ellipsoid"
    Unknown_datum_GRS67 = "Unknown datum based upon the GRS 1967 ellipsoid"
    Unknown_datum_GRS80 = "Unknown datum based upon the GRS 1980 ellipsoid"
    Unknown_datum_Helmert_1906 = "Unknown datum based upon the Helmert 1906 ellipsoid"
    Unknown_datum_Indonesian_National_Spheroid = (
        "Unknown datum based upon the Indonesian National Spheroid"
    )
    Unknown_datum_International_1924 = (
        "Unknown datum based upon the International 1924 ellipsoid"
    )
    Unknown_datum_Krassowsky_1940 = (
        "Unknown datum based upon the Krassowsky 1940 ellipsoid"
    )
    Unknown_datum_NWL9D = "Unknown datum based upon the NWL 9D ellipsoid"
    Unknown_datum_OSU86F = "Unknown datum based upon the OSU86F ellipsoid"
    Unknown_datum_OSU91A = "Unknown datum based upon the OSU91A ellipsoid"
    Unknown_datum_Plessis_1817 = "Unknown datum based upon the Plessis 1817 ellipsoid"
    Unknown_datum_Struve_1860 = "Unknown datum based upon the Struve 1860 ellipsoid"
    Unknown_datum_War_Office = "Unknown datum based upon the War Office ellipsoid"
    Unknown_datum_WGS72 = "Unknown datum based upon the WGS 72 ellipsoid"
    Unknown_datum_WGS84 = "Unknown datum based upon the WGS 84 ellipsoid"
    Unspecified_datum_Clarke_1866_Authalic_Sphere = (
        "Unspecified datum based upon the Clarke 1866 Authalic Sphere"
    )
    Unspecified_datum_GRS80_Authalic_Sphere = (
        "Unspecified datum based upon the GRS 1980 Authalic Sphere"
    )
    Unspecified_datum_Hughes_1980 = (
        "Unspecified datum based upon the Hughes 1980 ellipsoid"
    )
    Unspecified_datum_International_1924_Authalic_Sphere = (
        "Unspecified datum based upon the International 1924 Authalic Sphere"
    )
    Vanua_Levu_1915 = "Vanua Levu 1915"
    Vientiane_1982 = "Vientiane 1982"
    Viti_Levu_1912 = "Viti Levu 1912"
    Viti_Levu_1916 = "Viti Levu 1916"
    VN_2000 = "VN-2000"
    Voirol_1875 = "Voirol 1875"
    Voirol_1875_Paris = "Voirol 1875 (Paris)"
    Voirol_1879 = "Voirol 1879"
    Voirol_1879_Paris = "Voirol 1879 (Paris)"
    Wake_Island_1952 = "Wake Island 1952"
    WGS66 = "WGS66"
    WGS72 = "WGS72"
    WGS72BE = "WGS72BE"
    WGS84 = "WGS84"
    Xian_1980 = "Xian1980"
    Yacare = "Yacare"
    Yemen_NGN96 = "YemenNGN96"
    Yoff = "Yoff"
    Zanderij = "Zanderij"
