from datetime import date

COMPANY = [(
        1,
        'AA',
        'Alcoa Corporation Common Stock ',
        4012360466,
        '',
        2016,
        5422363,
        'Basic Industries',
        'Aluminum',
        False,
        False,
        False,
        False,
        False,
        False,
        date(2021, 12, 30)
    )]

SOURCE_DETAILS = [(3, 'stock_analysis', 'API')]

NORMALIZED_FIELDS = [
    (1, 'total_revenue', 'Total Revenue', 'income_statement'),
    (3, 'cost_of_revenue', 'Cost of Revenue', 'income_statement')
]

STATEMENT_TYPE = [
    (1, 'income_statement')
]

STATEMENT_LINE = [
    (3, 'Revenue', None, 3, 1, 1),
    (4, 'Cost of Revenue', None, 3, 3, 1)
]

STATEMENT_FACT = [
    (1394, date(2021, 12, 30), None, 3340, 1, 3),
    (1407, date(2021, 9, 30), None, 3109, 1, 3),
    (2117, date(2021, 6, 30), None, 2833, 1, 3),
    (2130, date(2021, 3, 30), None, 2870, 1, 3),
    (2143, date(2020, 12, 30), None, 2392, 1, 3),
    (2156, date(2020, 9, 30), None, 2365, 1, 3),
    (2169, date(2020, 6, 30), None, 2148, 1, 3),
    (2182, date(2020, 3, 30), None, 2381, 1, 3),
]


DUMMY_DATA = [
    ['Quarter Ended', date(2022, 3, 30), date(2021, 12, 30), date(2021, 9, 30), date(2021, 6,30), date(2021, 3, 30), date(2020, 12, 30), date(2020, 9, 30), date(2020, 6, 30), date(2020, 3, 30), date(2019, 12, 30), date(2019, 9, 30), date(2019, 6, 30), date(2019, 3, 30), date(2018, 12, 30), date(2018, 9, 30), date(2018, 6, 30), date(2018, 3, 30), date(2017, 12, 30), date(2017, 9, 30), date(2017, 6, 30), date(2017, 3, 30), date(2016, 12, 30), date(2016, 9, 30), date(2016, 6, 30), date(2016, 3, 30), date(2015, 12, 30), date(2015, 9, 30)],
    ['total_revenue', 3293, 3340, 3109, 2833, 2870, 2392, 2365, 2148, 2381, 2436, 2567, 2711, 2719, 3344, 3390, 3579, 3090, 3174, 2964, 2859, 2655, 2537, 2329, 2323, 2129, 2451, 2679],
    ['cost_of_revenue', 2181, 2383, 2322, 2156, 2292, 1974, 2038, 1932, 2025, 2048, 2120, 2189, 2180, 2513, 2485, 2753, 2302, 2298, 2340, 2289, 2023, 2102, 1968, 1941, 1866, 2157, 2239],
    ['gross_profit', 1112, 957, 787, 677, 578, 418, 327, 216, 356, 388, 447, 522, 539, 831, 905, 826, 788, 876, 624, 570, 632, 435, 361, 382, 263, 294, 440],
    ['selling_general_and_administrative', 44, 68, 53, 54, 52, 55, 47, 44, 60, 62, 66, 68, 84, 59, 58, 64, 67, 69, 70, 70, 71, 89, 92, 90, 85, 92, 95],
    ['research_and_development', 9, 10, 8, 6, 7, 9, 6, 5, 7, 6, 7, 7, 7, 7, 7, 9, 8, 9, 8, 8, 7, 7, 8, 7, 11, 15, 14],
    ['operating_expense', 324, 1000, 232, 149, 224, 338, 264, 289, 239, 658, 469, 669, 417, 410, 417, 505, 271, 565, 310, 308, 188, 512, 192, 260, 396, 1030, 357],
    ['operating_income', 788, -43, 555, 528, 354, 80, 63, -73, 117, -270, -22, -147, 122, 421, 488, 321, 517, 311, 314, 262, 444, -77, 169, 122, -133, -736, 83],
    ['net_non_operating_interest_income_expense', 25, 28, 58, 67, 42, 43, 41, 32, 30, 31, 30, 30, 30, 31, 33, 32, 26, 27, 26, 25, 26, 46, 67, 66, 64, 62, 69],
    ['other_income_expense', 84, 23, 33, 41, 44, 21, 29, 47, -73, -52, 74, 109, 141, 176, 201, 121, 145, 154, 56, 63, 83, -4, 20, 43, -5, -64, 61],
    ['pretax_income', 679, -94, 464, 420, 268, 16, -7, -152, 160, -249, -126, -286, -49, 214, 254, 168, 346, 130, 232, 174, 335, -119, 82, 13, -192, -734, -47],
    ['tax_provision', 210, 298, 127, 111, 93, 20, 42, 45, 80, 54, 95, 116, 150, 163, 260, 158, 151, 264, 119, 99, 110, 6, 92, 68, 18, 92, 77],
    ['net_income', 469, -392, 337, 309, 175, -4, -49, -197, 80, -303, -221, -402, -199, 51, -6, 10, 195, -134, 113, 75, 225, -125, -10, -55, -210, -826, -124],
    ['basic_average_shares', 185, 187, 187, 187, 186, 186, 186, 186, 186, 186, 186, 186, 185, 186, 186, 186, 186, 185, 184, 184, 184, 183, 183, 183, 183, 183]
]