from shutil import copyfile
import CardCrypto
from PIL import Image, ImageFont, ImageDraw, ImageEnhance




localeList = [
    [   8,   8, "Albanian Lek",                   "Albania",                                 "ALL", 2, False  ],
    [  12,  12, "Algerian dinar",                 "Algeria",                                 "DZD", 2, False  ],
    [  32,  32, "Argentine peso",                 "Argentina",                               "ARS", 2, False  ],
    [  36,  36, "Australian dollar",              "Australia",                               "AUD", 2, True   ],
    [  36, 162, "Australian dollar",              "Christmas Island",                        "AUD", 2, False  ],
    [  36, 166, "Australian dollar",              "Cocos Islands",                           "AUD", 2, False  ],
    [  36, 296, "Australian dollar",              "Kiribati",                                "AUD", 2, False  ],
    [  36, 334, "Australian dollar",              "Heard & McDonald Islands",                "AUD", 2, False  ],
    [  36, 520, "Australian dollar",              "Nauru",                                   "AUD", 2, False  ],
    [  36, 574, "Australian dollar",              "Norfolk Island",                          "AUD", 2, False  ],
    [  36, 798, "Australian dollar",              "Tuvalu",                                  "AUD", 2, False  ],
    [  44,  44, "Bahamian dollar",                "Bahamas",                                 "BSD", 2, False  ],
    [  48,  48, "Bahraini dinar",                 "Bahrain",                                 "BHD", 3, False  ],
    [  50,  50, "Bangladeshi taka",               "Bangladesh",                              "BDT", 2, False  ],
    [  51,  51, "Armenian dram",                  "Armenia",                                 "AMD", 2, False  ],
    [  52,  52, "Barbados dollar",                "Barbados",                                "BBD", 2, False  ],
    [  60,  60, "Bermudian dollar",               "Bermuda",                                 "BMD", 2, False  ],
    [  64,  64, "Ngultrum",                       "Bhutan",                                  "BTN", 2, False  ],
    [  68,  68, "Boliviano",                      "Bolivia",                                 "BOB", 2, False  ],
    [  72,  72, "Pula",                           "Botswana",                                "BWP", 2, False  ],
    [  84,  84, "Belize dollar",                  "Belize",                                  "BZD", 2, False  ],
    [  90,  90, "Solomon Islands dollar",         "Solomon Islands",                         "SBD", 2, False  ],
    [  96,  96, "Brunei dollar",                  "Brunei Darussalam",                       "BND", 2, False  ],
    [ 104, 104, "Kyat",                           "Myanmar",                                 "MMK", 2, False  ],
    [ 108, 108, "Burundian franc",                "Burundi",                                 "BIF", 0, False  ],
    [ 116, 116, "Riel",                           "Cambodia",                                "KHR", 2, False  ],
    [ 124, 124, "Canadian dollar",                "Canada",                                  "CAD", 2, False  ],
    [ 132, 132, "Cape Verde escudo",              "Cape Verde",                              "CVE", 0, False  ],
    [ 136, 136, "Cayman Islands dollar",          "Cayman Islands",                          "KYD", 2, False  ],
    [ 144, 144, "Sri Lanka rupee",                "Sri Lanka",                               "LKR", 2, False  ],
    [ 152, 152, "Chilean peso",                   "Chile",                                   "CLP", 0, False  ],
    [ 156, 156, "Chinese Yuan",                   "China",                                   "CNY", 2, False  ],
    [ 170, 170, "Colombian peso",                 "Columbia",                                "COP", 2, False  ],
    [ 174, 174, "Comoro franc",                   "Comoros",                                 "KMF", 0, False  ],
    [ 188, 188, "Costa Rican colon",              "Costa Rica",                              "CRC", 2, False  ],
    [ 191, 191, "Croatian kuna",                  "Croatia",                                 "HRK", 2, False  ],
    [ 192, 192, "Cuban peso",                     "Cuba",                                    "CUP", 2, False  ],
    [ 203, 203, "Czech Koruna",                   "Czech Republic",                          "CZK", 2, False  ],
    [ 208, 208, "Danish krone",                   "Denmark",                                 "DKK", 2, True   ],
    [ 208, 234, "Danish krone",                   "Faeroe Islands",                          "DKK", 2, False  ],
    [ 208, 304, "Danish krone",                   "Greenland",                               "DKK", 2, False  ],
    [ 214, 214, "Dominican peso",                 "Dominican Republic",                      "DOP", 2, False  ],
    [ 230, 230, "Ethiopian birr",                 "Ethiopia",                                "ETB", 2, False  ],
    [ 232, 232, "Nakfa",                          "Eritrea",                                 "ERN", 2, False  ],
    [ 238, 238, "Falkland Islands pound",         "Falkland Islands",                        "FKP", 2, False  ],
    [ 238, 239, "Falkland Islands pound",         "South Georgia + South Sandwich Islands",  "FKP", 2, False  ],
    [ 242, 242, "Fiji dollar",                    "Fiji",                                    "FJD", 2, False  ],
    [ 262, 262, "Djibouti franc",                 "Djibouti",                                "DJF", 0, False  ],
    [ 270, 270, "Dalasi",                         "Gambia",                                  "GMD", 2, False  ],
    [ 292, 292, "Gibraltar pound",                "Gibraltar",                               "GIP", 2, False  ],
    [ 320, 320, "Quetzal",                        "Guatemala",                               "GTQ", 2, False  ],
    [ 324, 324, "Guinea franc",                   "Guinea",                                  "GNF", 0, False  ],
    [ 328, 328, "Guyana dollar",                  "Guyana",                                  "GYD", 2, False  ],
    [ 332, 332, "Haiti gourde",                   "Haiti",                                   "HTG", 2, False  ],
    [ 340, 340, "Lempira",                        "Honduras",                                "HNL", 2, False  ],
    [ 344, 344, "Hong Kong dollar",               "Hong Kong",                               "HKD", 2, False  ],
    [ 348, 348, "Forint",                         "Hungary",                                 "HUF", 2, False  ],
    [ 352, 352, "Iceland krona",                  "Iceland",                                 "ISK", 0, False  ],
    [ 356, 356, "Indian rupee",                   "India",                                   "INR", 2, True   ],
    [ 360, 360, "Rupiah",                         "Indonesia",                               "IDR", 2, False  ],
    [ 364, 364, "Iranian rial",                   "Iran",                                    "IRR", 2, False  ],
    [ 368, 368, "Iraqi dinar",                    "Iraq",                                    "IQD", 3, False  ],
    [ 376, 376, "Israeli new sheqel",             "Israel",                                  "ILS", 2, False  ],
    [ 388, 388, "Jamaican dollar",                "Jamaica",                                 "JMD", 2, False  ],
    [ 392, 392, "Japanese yen",                   "Japan",                                   "JPY", 0, True   ],
    [ 398, 398, "Tenge",                          "Kazakhstan",                              "KZT", 2, False  ],
    [ 400, 400, "Jordanian dinar",                "Jordan",                                  "JOD", 3, False  ],
    [ 404, 404, "Kenyan shilling",                "Kenya",                                   "KES", 2, False  ],
    [ 408, 408, "Democratic",                     "Korea",                                   "KPW", 2, False  ],
    [ 410, 410, "Repulic of",                     "Korea",                                   "KRW", 0, False  ],
    [ 414, 414, "Kuwaiti dinar",                  "Kuwait",                                  "KWD", 3, False  ],
    [ 417, 417, "Som",                            "Kyrgyzstan",                              "KGS", 2, False  ],
    [ 418, 418, "Kip",                            "Lao Peoples Democratic Republic",         "LAK", 2, False  ],
    [ 422, 422, "Lebanese pound",                 "Lebanon",                                 "LBP", 2, False  ],
    [ 426, 426, "Lesotho loti",                   "Lesotho",                                 "LSL", 2, False  ],
    [ 430, 430, "Liberian dollar",                "Liberia",                                 "LRD", 2, False  ],
    [ 434, 434, "Libyan dinar",                   "Libyan Arab Jamahirian Republic",         "LYD", 3, False  ],
    [ 446, 446, "Pataca",                         "Macau",                                   "MOP", 2, False  ],
    [ 454, 454, "Kwacha",                         "Malawi",                                  "MWK", 2, False  ],
    [ 458, 458, "Malaysian ringgit",              "Malaysia",                                "MYR", 2, False  ],
    [ 462, 462, "Rufiyaa",                        "Maldives",                                "MVR", 2, False  ],
    [ 480, 480, "Mauritius rupee",                "Mauritius",                               "MUR", 2, False  ],
    [ 484, 484, "Mexican peso",                   "Mexico",                                  "MXN", 2, True   ],
    [ 496, 496, "Tugrik",                         "Mongolia",                                "MNT", 2, False  ],
    [ 498, 498, "Republic of",                    "Moldova",                                 "MDL", 2, False  ],
    [ 504, 504, "Moroccan dirham",                "Morrocco",                                "MAD", 2, False  ],
    [ 504, 732, "Moroccan dirham",                "Western Sahara",                          "MAD", 2, False  ],
    [ 512, 512, "Rial Omani",                     "Oman",                                    "OMR", 3, False  ],
    [ 516, 516, "Namibian dollar",                "Namibia",                                 "NAD", 2, False  ],
    [ 524, 524, "Nepalese rupee",                 "Nepal",                                   "NPR", 2, False  ],
    [ 532, 530, "Netherlands Antillean guilder",  "Netherlands Antilles",                    "ANG", 2, False  ],
    [ 533, 533, "Aruban guilder",                 "Aruba",                                   "AWG", 2, False  ],
    [ 548, 548, "Vatu",                           "Vanuatu",                                 "VUV", 0, False  ],
    [ 554, 554, "New Zealand dollar",             "New Zealand",                             "NZD", 2, True   ],
    [ 554, 184, "New Zealand dollar",             "Cook Islands",                            "NZD", 2, False  ],
    [ 554, 570, "New Zealand dollar",             "Niue",                                    "NZD", 2, False  ],
    [ 554, 612, "New Zealand dollar",             "Pitcairn Island",                         "NZD", 2, False  ],
    [ 554, 722, "New Zealand dollar",             "Tokelau",                                 "NZD", 2, False  ],
    [ 558, 558, "Cordoba oro",                    "Nicaraqua",                               "NIO", 2, False  ],
    [ 566, 566, "Naira",                          "Nigeria",                                 "NGN", 2, False  ],
    [ 578, 578, "Norwegian krone",                "Norway",                                  "NOK", 2, True   ],
    [ 578,  74, "Norwegian krone",                "Bouvet Island",                           "NOK", 2, False  ],
    [ 578, 744, "Norwegian krone",                "SvalBard & Jan Mayen",                    "NOK", 2, False  ],
    [ 586, 586, "Pakistan rupee",                 "Pakistan",                                "PKR", 2, False  ],
    [ 590, 591, "Balboa",                         "Panama",                                  "PAB", 2, False  ],
    [ 598, 598, "Kina",                           "Papua New Guinea",                        "PGK", 2, False  ],
    [ 600, 600, "Guarani",                        "Paraguay",                                "PYG", 0, False  ],
    [ 604, 604, "Nuevo sol",                      "Peru",                                    "PEN", 2, False  ],
    [ 608, 608, "Philippine peso",                "Philippines",                             "PHP", 2, True   ],
    [ 634, 634, "Qatari rial",                    "Qatar",                                   "QAR", 2, False  ],
    [ 643, 643, "Russian ruble",                  "Russian Federation",                      "RUB", 2, True   ],
    [ 646, 646, "Rwanda franc",                   "Rwanda",                                  "RWF", 0, False  ],
    [ 654, 654, "Saint Helena pound",             "St. Helena",                              "SHP", 2, False  ],
    [ 682, 682, "Saudi riyal",                    "Saudi Arabia",                            "SAR", 2, False  ],
    [ 690, 690, "Seychelles rupee",               "Seychelles",                              "SCR", 2, False  ],
    [ 694, 694, "Leone",                          "Seirra Leone",                            "SLL", 2, False  ],
    [ 702, 702, "Singapore dollar",               "Singapore",                               "SGD", 2, True   ],
    [ 704, 704, "Vietnamese d?ng",                "Viet Nam",                                "VND", 0, False  ],
    [ 706, 706, "Somali shilling",                "Somalia",                                 "SOS", 2, False  ],
    [ 710, 710, "South African rand",             "South Africa",                            "ZAR", 2, True   ],
    [ 710, 516, "South African rand",             "Namibia",                                 "ZAR", 2, False  ],
    [ 748, 748, "Lilangeni",                      "Swaziland",                               "SZL", 2, False  ],
    [ 752, 752, "Swedish krona",                  "Sweden",                                  "SEK", 2, False  ],
    [ 756, 756, "Swiss franc",                    "Switzerland",                             "CHF", 2, True   ],
    [ 756, 438, "Swiss franc",                    "Liechtenstein",                           "CHF", 2, False  ],
    [ 760, 760, "Syrian pound",                   "Syrian Arab Republic",                    "SYP", 2, False  ],
    [ 764, 764, "Baht",                           "Thailand",                                "THB", 2, True   ],
    [ 776, 776, "Paanga",                         "Tonga",                                   "TOP", 2, False  ],
    [ 780, 780, "Trinidad and Tobago dollar",     "Trinadad and Tobago",                     "TTD", 2, False  ],
    [ 784, 784, "United Arab Emirates dirham",    "United Arab Emirates",                    "AED", 2, True   ],
    [ 788, 788, "Tunisian dinar",                 "Tunisia",                                 "TND", 3, False  ],
    [ 800, 800, "Uganda shilling",                "Uganda",                                  "UGX", 0, False  ],
    [ 818, 818, "Egyptian pound",                 "Egypt",                                   "EGP", 2, False  ],
    [ 826, 826, "Pound sterling",                 "United Kingdom",                          "GBP", 2, True   ],
    [ 826, 831, "Pound sterling",                 "Guernsey",                                "GBP", 2, False  ],
    [ 834, 834, "Tanzanian shilling",             "Tanzia",                                  "TZS", 2, False  ],
    [ 840, 840, "US dollar",                      "United States",                           "USD", 2, True   ],
    [ 840,  16, "US dollar",                      "American Samoa",                          "USD", 2, False  ],
    [ 840,  86, "US dollar",                      "British Indian Ocean",                    "USD", 2, False  ],
    [ 840,  92, "US dollar",                      "Virgin Islands (British)",                "USD", 2, False  ],
    [ 840, 218, "US dollar",                      "Ecuador",                                 "USD", 2, False  ],
    [ 840, 222, "US dollar",                      "El Salvador",                             "USD", 2, False  ],
    [ 840, 316, "US dollar",                      "Guam",                                    "USD", 2, False  ],
    [ 840, 580, "US dollar",                      "Northern Mariana Islands",                "USD", 2, False  ],
    [ 840, 581, "US dollar",                      "US Minor Outlying Islands",               "USD", 2, False  ],
    [ 840, 583, "US dollar",                      "Micronesia",                              "USD", 2, False  ],
    [ 840, 584, "US dollar",                      "Marshall Islands",                        "USD", 2, False  ],
    [ 840, 585, "US dollar",                      "Palau",                                   "USD", 2, False  ],
    [ 840, 626, "US dollar",                      "Timor Leste",                             "USD", 2, False  ],
    [ 840, 630, "US dollar",                      "Puerto Rico",                             "USD", 2, False  ],
    [ 840, 796, "US dollar",                      "Turks & Caicos Islands",                  "USD", 2, False  ],
    [ 840, 850, "US dollar",                      "US Virgin Islands",                       "USD", 2, False  ],
    [ 858, 858, "Peso Uruguayo",                  "Urugruay",                                "UYU", 2, False  ],
    [ 860, 860, "Uzbekistan som",                 "Uzbekistan",                              "UZS", 2, False  ],
    [ 882, 882, "Samoan tala",                    "Samoa",                                   "WST", 2, False  ],
    [ 886, 887, "Yemeni rial",                    "Yemen",                                   "YER", 2, False  ],
    [ 901, 158, "New Taiwan dollar",              "Taiwan",                                  "TWD", 2, False  ],
    [ 929, 478, "Ouguiya",                        "Mauritinia",                              "MRU", 1, False  ],
    [ 930, 678, "Dobra",                          "San Tome and Principe",                   "STN", 2, False  ],
    [ 931, 192, "Cuban convertible peso",         "Cuba",                                    "CUC", 2, False  ],
    [ 932, 716, "Zimbabwe dollar",                "Zimbabwe",                                "ZWL", 2, False  ],
    [ 933, 112, "Belarussian ruble",              "Belarus",                                 "BYN", 2, False  ],
    [ 934, 795, "Manat",                          "Turkmenistan",                            "TMT", 2, False  ],
    [ 936, 288, "Cedi",                           "Ghana",                                   "GHS", 2, False  ],
    [ 937, 862, "Venezuelan bolivar fuerte",      "Venezuela",                               "VEF", 2, False  ],
    [ 938, 736, "Sudanese pound",                 "Sudan",                                   "SDG", 2, False  ],
    [ 941, 688, "Republic of",                    "Serbia",                                  "RSD", 2, False  ],
    [ 943, 508, "Metical",                        "Mozambique",                              "MZN", 2, False  ],
    [ 944,  31, "Azerbaijanian manat",            "Azerbaijan",                              "AZN", 2, False  ],
    [ 946, 642, "Romanian new leu",               "Romania",                                 "RON", 2, False  ],
    [ 949, 792, "Turkish lira",                   "Turkey",                                  "TRY", 2, True   ],
    [ 950, 120, "CFA franc BEAC",                 "Cameroon",                                "XAF", 0, False  ],
    [ 950, 140, "CFA franc BEAC",                 "Central African Republic",                "XAF", 0, False  ],
    [ 950, 148, "CFA franc BEAC",                 "Chad",                                    "XAF", 0, False  ],
    [ 950, 226, "CFA franc BEAC",                 "Equatorial Guinea",                       "XAF", 0, False  ],
    [ 950, 266, "CFA franc BEAC",                 "Gabon",                                   "XAF", 0, False  ],
    [ 951,  28, "East Caribbean dollar",          "Antigua and Barbuda",                     "XCD", 2, False  ],
    [ 951, 212, "East Caribbean dollar",          "Dominica",                                "XCD", 2, False  ],
    [ 951, 308, "East Caribbean dollar",          "Grenada",                                 "XCD", 2, False  ],
    [ 951, 500, "East Caribbean dollar",          "Montserrat",                              "XCD", 2, False  ],
    [ 951, 659, "East Caribbean dollar",          "St. Kitts-Nevis-Anguilla",                "XCD", 2, False  ],
    [ 951, 660, "East Caribbean dollar",          "Anguilla",                                "XCD", 2, False  ],
    [ 951, 662, "East Caribbean dollar",          "St. Lucia",                               "XCD", 2, False  ],
    [ 951, 670, "East Caribbean dollar",          "St. Vincent and the Grenadines",          "XCD", 2, False  ],
    [ 952, 204, "CFA Franc BCEAO",                "Benin",                                   "XOF", 0, False  ],
    [ 952, 384, "CFA Franc BCEAO",                "Ivory Coast",                             "XOF", 0, False  ],
    [ 952, 466, "CFA Franc BCEAO",                "Mali",                                    "XOF", 0, False  ],
    [ 952, 562, "CFA Franc BCEAO",                "Niger",                                   "XOF", 0, False  ],
    [ 952, 624, "CFA Franc BCEAO",                "Guinea-Bissau",                           "XOF", 0, False  ],
    [ 952, 686, "CFA Franc BCEAO",                "Senegal",                                 "XOF", 0, False  ],
    [ 952, 768, "CFA Franc BCEAO",                "Togo",                                    "XOF", 0, False  ],
    [ 952, 854, "CFA Franc BCEAO",                "Burkina Faso",                            "XOF", 0, False  ],
    [ 953, 258, "CFP franc",                      "French Polynesia",                        "XPF", 0, False  ],
    [ 953, 540, "CFP franc",                      "New Caledonia",                           "XPF", 0, False  ],
    [ 953, 876, "CFP franc",                      "Wallis and Futuna Islands",               "XPF", 0, False  ],
    [ 967, 894, "Kwacha",                         "Zambia",                                  "ZMW", 2, False  ],
    [ 968, 740, "Surinam dollar",                 "Suriname",                                "SRD", 2, False  ],
    [ 969, 450, "Malagasy ariary",                "Madagascar",                              "MGA", 1, False  ],
    [ 970, 170, "Unidad de Valor Real",           "Columbia",                                "COU", 2, False  ],
    [ 971,   4, "Afghani",                        "Afganistan",                              "AFN", 2, False  ],
    [ 972, 762, "Somoni",                         "Tajikistan",                              "TJS", 2, False  ],
    [ 973,  24, "Kwanza",                         "Angola",                                  "AOA", 2, False  ],
    [ 975, 100, "Bulgarian lev",                  "Bulgaria",                                "BGN", 2, False  ],
    [ 976, 178, "Franc Congolais",                "Congo",                                   "CDF", 2, False  ],
    [ 977,  70, "Convertible marks",              "Bosnia and Herzegovina",                  "BAM", 2, False  ],
    [ 978,  56, "Euro",                           "Belgium",                                 "EUR", 2, True   ],
    [ 978,  20, "Euro",                           "Andorra",                                 "EUR", 2, False  ],
    [ 978,  40, "Euro",                           "Austria",                                 "EUR", 2, False  ],
    [ 978, 175, "Euro",                           "Mayotte",                                 "EUR", 2, False  ],
    [ 978, 196, "Euro",                           "Cyprus",                                  "EUR", 2, False  ],
    [ 978, 233, "Euro",                           "Estonia",                                 "EUR", 2, False  ],
    [ 978, 246, "Euro",                           "Finland",                                 "EUR", 2, False  ],
    [ 978, 250, "Euro",                           "France",                                  "EUR", 2, False  ],
    [ 978, 254, "Euro",                           "French Guiana",                           "EUR", 2, False  ],
    [ 978, 260, "Euro",                           "French Southern Territories",             "EUR", 2, False  ],
    [ 978, 276, "Euro",                           "Germany",                                 "EUR", 2, False  ],
    [ 978, 300, "Euro",                           "Greece",                                  "EUR", 2, False  ],
    [ 978, 312, "Euro",                           "Guadeloupe",                              "EUR", 2, False  ],
    [ 978, 336, "Euro",                           "Vatican City State",                      "EUR", 2, False  ],
    [ 978, 372, "Euro",                           "Ireland",                                 "EUR", 2, False  ],
    [ 978, 380, "Euro",                           "Italy",                                   "EUR", 2, False  ],
    [ 978, 428, "Euro",                           "Latvia",                                  "EUR", 2, False  ],
    [ 978, 440, "Euro",                           "Lithuania",                               "EUR", 2, False  ],
    [ 978, 442, "Euro",                           "Luxembuurg",                              "EUR", 2, False  ],
    [ 978, 470, "Euro",                           "Malta",                                   "EUR", 2, False  ],
    [ 978, 474, "Euro",                           "Martinique",                              "EUR", 2, False  ],
    [ 978, 492, "Euro",                           "Monaco",                                  "EUR", 2, False  ],
    [ 978, 499, "Euro",                           "Montenegro",                              "EUR", 2, False  ],
    [ 978, 528, "Euro",                           "Netherlands",                             "EUR", 2, False  ],
    [ 978, 620, "Euro",                           "Portugal",                                "EUR", 2, False  ],
    [ 978, 638, "Euro",                           "Reunion",                                 "EUR", 2, False  ],
    [ 978, 652, "Euro",                           "Saint Barthelemy",                        "EUR", 2, False  ],
    [ 978, 666, "Euro",                           "St. Pierre and Mique",                    "EUR", 2, False  ],
    [ 978, 674, "Euro",                           "San Marino",                              "EUR", 2, False  ],
    [ 978, 703, "Euro",                           "Slovakia",                                "EUR", 2, False  ],
    [ 978, 705, "Euro",                           "Slovenia",                                "EUR", 2, False  ],
    [ 978, 724, "Euro",                           "Spain",                                   "EUR", 2, False  ],
    [ 980, 804, "Hryvnia",                        "Ukraine",                                 "UAH", 2, False  ],
    [ 981, 268, "Lari",                           "Georgia",                                 "GEL", 2, False  ],
    [ 985, 616, "Zloty",                          "Poland",                                  "PLN", 2, False  ],
    [ 986,  76, "Brazilian real",                 "Brazil",                                  "BRL", 2, False  ]
    ]





def handleLocale(audit, currency, country, args = dict([])):
    
    sCurrency = currency
    sCountry = country
    bOverride = False
    
    if args.has_key('OverrideCurrency'):
        sCurrency = args['OverrideCurrency']
        bOverride = True
        
    if args.has_key('OverrideCountry'):
        sCountry = args['OverrideCountry']
        bOverride = True

    while len(sCurrency) < 4:
        sCurrency = "0" + sCurrency
        
    while len(sCountry) < 4:
        sCountry = "0" + sCountry
        
    if bOverride == True and audit != None:
        audit.write("Using locale override: %s" % buildLocaleString(int(sCurrency), int(sCountry)))
        audit.write("")
        
    
    return sCurrency, sCountry


def handleInternationalLocale(audit, args = dict([])):
    
    sCurrency = "0840"
    sCountry = "0840"
    
    if args.has_key('OverrideCurrency'):
        if int(args['OverrideCurrency']) == int(sCurrency):
            sCurrency = "0826"
            
    if args.has_key('OverrideCountry'):
        if int(args['OverrideCountry']) == int(sCountry):
            sCountry = "0826"
        
    while len(sCurrency) < 4:
        sCurrency = "0" + sCurrency
        
    while len(sCountry) < 4:
        sCountry = "0" + sCountry
        
    if audit != None:
        audit.write("Using locale: %s" % buildLocaleString(int(sCurrency), int(sCountry)))
        audit.write("")
        
    
    return sCurrency, sCountry


def buildLocaleString(currency, country):
    
    countryName = "Unknown"
    currencyName = "Unknown"
    
    for l in localeList:
        if l[1] == int(country):
            countryName = l[3]
            break
        
    for l in localeList:
        if l[0] == int(currency):
            currencyName = l[2]
            break
        
    
    return "%s, %s" %(countryName, currencyName)


def getNextFullLocale(currency, country):
    
    nCurrency = int(currency)
    nCountry = 0
    if len(country) > 0: nCountry = int(country)
    
    currencyList = []
    selected_locale = None
    
    for l in localeList:
        if l[0] == nCurrency:
            currencyList.append(l)
        
    if len(currencyList) == 0:
        return None
    
    if nCountry == 0:
        selected_locale = currencyList[0]
    else:
        pos = -1
        for i in range(len(currencyList)):
            l = currencyList[i]
            if l[1] == nCountry:
                print nCountry, l[1]
                pos = i
            
        if pos == -1 or pos > len(currencyList)-2:
            selected_locale = currencyList[0]
        else:
            selected_locale = currencyList[pos+1]

    if selected_locale != None:
        s = "%s (%d/%s)/%s (%d)" % (selected_locale[2], selected_locale[0], selected_locale[4], selected_locale[3], selected_locale[1])
        it = [selected_locale[0], selected_locale[1], s]
        return it
    
    return None 
        
    

def getLocaleListForPicker():
    
    pickerlist = []
    
    for l in localeList:
        if l[6] == True:
            s = "%s (%d/%s)\n%s (%d)" % (l[2], l[0], l[4], l[3], l[1])
            it = [l[0], l[1], s]
            pickerlist.append(it)
            
    return pickerlist



def handleInternationalLocalePrint(front_file, args = dict([])):
    
    sCurrency, sCountry = handleInternationalLocale(None, args)
    
    if int(sCurrency) == 840 and int(sCountry) == 840: 
        return front_file
    
    ag = dict([])
    ag['OverrideCurrency'] = sCurrency
    ag['OverrideCountry'] = sCountry
    if args.has_key('PrintTempDir'): ag['PrintTempDir'] = args['PrintTempDir']
    
    return handleLocalePrint(front_file, ag)
    

def handleLocalePrint(front_file, args = dict([])):
           
    if args.has_key('OverrideCurrency') and args.has_key('OverrideCountry'):
        sCurrency = args['OverrideCurrency']
        sCountry = args['OverrideCountry']
        
        sLocale = buildLocaleString(sCurrency, sCountry)
        
        sPrintTempDir = "C:\\Temp\\"
        if args.has_key('PrintTempDir'): sPrintTempDir = args['PrintTempDir']
        
        sLocaleFile = sPrintTempDir + "tempfile.bmp"
        
        copyfile(front_file, sLocaleFile)
        
        img = Image.open(sLocaleFile)
        draw = ImageDraw.Draw(img)
        draw.rectangle(((360, 260), (800, 290)), fill="white")
        draw.text((363, 265), sLocale, font=ImageFont.truetype("calibri.ttf", 29), fill=(0,0,0,255))
      
        img.save(sLocaleFile)
        
        

        
        return sLocaleFile
        
    else:
        return front_file



def handlePrintFileDCC(front_file, prefix, nDigits, args = dict([])):
           
    currency = "0840"
    country = "0840"
    currency, country = handleLocale(None, currency, country, args)
    PAN = DCC_BuildPAN(prefix, currency, nDigits)
    text_color = 'black'
    
    type = "Uknown"
    if prefix == "994":
        type = "VISA"
    if prefix == "995":
        type = "MasterCard"
        
    if prefix == "997":
        type = "Electron"
    if prefix == "998":
        type = "Maestro"
        
    
    printable_PAN = ""
    for i in range(len(PAN)):
        printable_PAN = printable_PAN + PAN[i]
        if (i+1) % 4 == 0:
            printable_PAN = printable_PAN + " "
    
    
    sPrintTempDir = "C:\\Temp\\"
    if args.has_key('PrintTempDir'): sPrintTempDir = args['PrintTempDir']
    sDCCFile = sPrintTempDir + "dccfile.bmp"
    
    copyfile(front_file, sDCCFile)
        
    img = Image.open(sDCCFile)
    draw = ImageDraw.Draw(img)
    
    
    #draw.rectangle(((145, 520), (900, 600)), fill="white")
    x = 160
    if len(PAN) > 16: x = 95
    draw.text((x, m*534), printable_PAN, font=ImageFont.truetype("lucon.ttf", 60), fill=text_color)
    
    #draw.rectangle(((363, 216), (820, 470)), fill="white")
    x1 = 364
    x2 = 553
    y = 219
    y_step = 43
    font_size = 29
    
    
    draw.text((x1, y), "Card Type:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), type, font=ImageFont.truetype("calibrib.ttf", font_size), fill=text_color)
    
    y = y + y_step
    draw.text((x1, y), "Alpha Code:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), DCC_CurrencyAlpha(currency), font=ImageFont.truetype("calibrib.ttf", font_size), fill=text_color)
    
    y = y + y_step
    draw.text((x1, y), "Description:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), DCC_CurrencyName(currency), font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    
    y = y + y_step
    draw.text((x1, y), "ISO Code:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), currency[1:], font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    
    y = y + y_step
    draw.text((x1, y), "Minor Units:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), DCC_MinorUnits(currency), font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    
    y = y + y_step
    draw.text((x1, y), "Expiry Date:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), "12/2022", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    
    y = y + y_step
    draw.text((x1, y), "PIN:", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    draw.text((x2, y), "1234", font=ImageFont.truetype("calibri.ttf", font_size), fill=text_color)
    
  
    img.save(sDCCFile)
        
    return sDCCFile
        
    
    
def handlePrintFileCustom(front_file, tags = dict([]), args = dict([])):
    
    currency = tags['Currency_code']
    country = tags['Country_code']
           

    sPrintTempDir = "C:\\Temp\\"
    if args.has_key('PrintTempDir'): sPrintTempDir = args['PrintTempDir']
    sCustomFile = sPrintTempDir + "customfile.bmp"
    
    copyfile(front_file, sCustomFile)
        
    img = Image.open(sCustomFile)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle(((360, 210), (900, 240)), fill="white")
    if args.has_key('Custom_Card_name'):
        cardname = args['Custom_Card_name']
        if len(cardname) > 0:
            draw.text((361, 213), cardname, font=ImageFont.truetype("calibrib.ttf", 40), fill=(0,0,0,255))
    
    draw.rectangle(((300, 300), (900, 350)), fill="white")
    sLocale = buildLocaleString(currency, country)
    draw.text((361, 313), sLocale, font=ImageFont.truetype("calibri.ttf", 29), fill=(0,0,0,255))

    
    draw.rectangle(((680, 350), (900, 390)), fill="white")
    if tags.has_key('Offline_PIN'):
        if len(tags['Offline_PIN']) > 0: 
            sPIN = "PIN " + tags['Offline_PIN']
            draw.text((686, 356), sPIN, font=ImageFont.truetype("calibri.ttf", 29), fill=(0,0,0,255))
  
    draw.rectangle(((100, 420), (200, 450)), fill="white")
    if args.has_key('Custom_Card_notes_1'):
        notes_1 = args['Custom_Card_notes_1']
        if len(notes_1) > 0:
            draw.text((114, 427), "Notes:", font=ImageFont.truetype("calibri.ttf", 29), fill=(0,0,0,255))
            draw.text((215, 427), notes_1, font=ImageFont.truetype("calibri.ttf", 29), fill=(0,0,0,255))
            
    if args.has_key('Custom_Card_notes_2'):
        notes_2 = args['Custom_Card_notes_2']
        if len(notes_2) > 0:
            draw.text((215, 470), notes_2, font=ImageFont.truetype("calibri.ttf", 29), fill=(0,0,0,255))
  
    img.save(sCustomFile)
        
    return sCustomFile



def handleBrandPrint(SetName, front_file, Card_Number, PAN, Description, PIN, args = dict([])):
    
    print_color = 'black'

    printable_PAN = ""
    for i in range(len(PAN)):
        printable_PAN = printable_PAN + PAN[i]
        if (i+1) % 4 == 0:
            printable_PAN = printable_PAN + " "

    sPrintTempDir = "C:\\Temp\\"
    if args.has_key('PrintTempDir'): sPrintTempDir = args['PrintTempDir']
    sBrandFile = sPrintTempDir + "brandfile.bmp"
    
    copyfile(front_file, sBrandFile)
        
    img = Image.open(sBrandFile)
    draw = ImageDraw.Draw(img)

    draw.text((374, 232), "Test card %02d" % Card_Number, font=ImageFont.truetype("calibrib.ttf", 40), fill=print_color)
  
    draw.text((374, 286), SetName, font=ImageFont.truetype("calibri.ttf", 29), fill=print_color)
    draw.text((374, 329), Description, font=ImageFont.truetype("calibri.ttf", 29), fill=print_color)
    
    y_warning = 415
    if len(PIN) > 0:
        draw.text((374, 372), "PIN %s" % PIN, font=ImageFont.truetype("calibri.ttf", 29), fill=print_color)
        y_warning = y_warning + 20
    
    draw.text((374, y_warning), "Not to be used for certification", font=ImageFont.truetype("calibri.ttf", 29), fill=print_color)
  
    x = 160
    if len(PAN) > 16: x = 95
    draw.text((x, 533), printable_PAN, font=ImageFont.truetype("lucon.ttf", 60), fill=print_color)
  
    img.save(sBrandFile, "BMP")
    #img.show()
        
    return sBrandFile
    


def handleBrandPrint_ADVT_7(front_file, Card_Number, PAN, Description, PIN, args = dict([])):

    SetName = "ADVT 7.0"
    
    return handleBrandPrint(SetName, front_file, Card_Number, PAN, Description, PIN, args)
    

def handleBrandPrint_ADVT_6(front_file, Card_Number, PAN, Description, PIN, args = dict([])):

    SetName = "ADVT 6.1.1"
    
    return handleBrandPrint(SetName, front_file, Card_Number, PAN, Description, PIN, args)
    




def handlePrintFileOverride(front_file, args = dict([])):
    
    file_to_print = front_file

    if args.has_key('OverridePrintingFile'):
        file_to_print = args['OverridePrintingFile']
        
    if len(file_to_print) > 3:
        if file_to_print[-4:].upper() != ".BMP":
            sPrintTempDir = "C:\\Temp\\"
            if args.has_key('PrintTempDir'): sPrintTempDir = args['PrintTempDir']
            sLocaleFile = sPrintTempDir + "convertedfile.bmp"
            
            img = Image.open(file_to_print)
            img = img.resize((1016, 648), Image.ANTIALIAS)
            img.save(sLocaleFile)
            file_to_print = sLocaleFile

    return file_to_print
    
   

def DCC_BuildPAN(prefix, currency, nDigits):
    PAN = prefix + currency[1:]
    
    while len(PAN) < nDigits-1:
        PAN = PAN + "0"
    
    PAN = PAN + CardCrypto.luhn10(PAN)
    
    return PAN


def DCC_CurrencyAlpha(currency):
    
    s = "UNK"
    for l in localeList:
        if l[0] == int(currency):
            s = l[4]
            break
    
    return s


def DCC_MinorUnits(currency):
    
    s = "-"
    for l in localeList:
        if l[0] == int(currency):
            s = "%d" % l[5]
            break
    
    return s


def DCC_CurrencyName(currency):
    
    s = "Unknown currency"
    for l in localeList:
        if l[0] == int(currency):
            s = l[2]
            break
    
    return s


def DCC_DisplayAllCards():
    
    cur = 0
    for l in localeList:
        if cur != l[0]:
            
            currency = "%04d" % l[0]
            PAN_VISA = DCC_BuildPAN("994", currency, 16)
            PAN_MASTERCARD = DCC_BuildPAN("995", currency, 16)
            PAN_ELECTRON = DCC_BuildPAN("997", currency, 16)
            PAN_MAESTRO = DCC_BuildPAN("998", currency, 19)
            
            s = "%03d\t%s\t%s\t%s\t%s\t%s\t%s\t" %(l[0], l[4], l[2].ljust(30), PAN_VISA, PAN_MASTERCARD, PAN_ELECTRON, PAN_MAESTRO)
            print s
        
        cur = l[0]
        
        


def to_ASCII_hex(s):
    
    l = list(s)
    ascii_str = ""
    for c in l:
        ascii_str = ascii_str + "%02X" % ord(c)
        
    return ascii_str
        

def makeTLV(tag, value):
    
    value = value.replace(" ", "")
    length = len(value)/2
    if length == 0: return ""
    L = "%02X" % (length)
    if length > 0x7F: L = "81" + L
    
    return "%s%s%s" % (tag, L, value)
       

def fixTLV_apdu(s):
    
    s = s.replace(" ", "")
    
    while "XX" in s:
        p = s.rfind("XX")
        left = s[:p]
        right = s[p+2:]
        length = len(right)/2
        L = "%02X" % (length)
        if length > 0x7F and len(left) > 16:
            L = "81" + L
        
        s = left + L + right
        
    return s


def fixTLV(s):
    
    s = s.replace(" ", "")
    
    while "XX" in s:
        p = s.rfind("XX")
        left = s[:p]
        right = s[p+2:]
        length = len(right)/2
        L = "%02X" % (length)
        if length > 0x7F:
            L = "81" + L
        
        s = left + L + right
        
    return s


def Custom_updateTags(tags = dict([]), args = dict([])):
    
    tags['Currency_code'], tags['Country_code'] = handleLocale(None, tags['Currency_code'], tags['Country_code'], args)

    for tag in tags.keys():
        if args.has_key("TagOverride_" + tag):
            tags[tag] = args["TagOverride_" + tag]

    


    
if __name__ == '__main__':
    
#     front_file = "..\\..\\..\\..\\..\\Business lines\\Merchant test cards\\Card designs\\Test and training pack\\bitmap\\Card 01 - Visa Credit.bmp"
#     
#     args = dict([])
#     args['PrintTempDir'] = "..\\..\\..\\..\\..\\Business lines\\Merchant test cards\\Card designs\\Custom cards\\temp\\"
#     args['OverrideCurrency'] = "978"
#     args['OverrideCountry'] = "56"
#         
#     handleLocalePrint(front_file, args)
    
    DCC_DisplayAllCards()
 
    print "finished"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    