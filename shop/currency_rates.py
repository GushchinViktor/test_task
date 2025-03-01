import requests

def get_exchange_rate(to_currency='usd'):
    dict_currencies = {"USD": 1, "AED": 3.67, "AFN": 73.55, "ALL": 94.49, "AMD": 394.01, "ANG": 1.79, "AOA": 920.06,
                       "ARS": 1062.38, "AUD": 1.6, "AWG": 1.79, "AZN": 1.7, "BAM": 1.88, "BBD": 2, "BDT": 121.52,
                       "BGN": 1.88, "BHD": 0.376, "BIF": 2966.65, "BMD": 1, "BND": 1.34, "BOB": 6.93, "BRL": 5.81,
                       "BSD": 1, "BTN": 87.32, "BWP": 13.84, "BYN": 3.26, "BZD": 2, "CAD": 1.44, "CDF": 2858.75,
                       "CHF": 0.899, "CLP": 942.42, "CNY": 7.29, "COP": 4129.78, "CRC": 506.49, "CUP": 24,
                       "CVE": 105.81, "CZK": 23.93, "DJF": 177.72, "DKK": 7.16, "DOP": 62.4, "DZD": 134.79,
                       "EGP": 50.66, "ERN": 15, "ETB": 126.66, "EUR": 0.96, "FJD": 2.3, "FKP": 0.792, "FOK": 7.16,
                       "GBP": 0.792, "GEL": 2.81, "GGP": 0.792, "GHS": 15.54, "GIP": 0.792, "GMD": 72.63,
                       "GNF": 8649.97, "GTQ": 7.72, "GYD": 209.59, "HKD": 7.78, "HNL": 25.61, "HRK": 7.23,
                       "HTG": 131.24, "HUF": 383.95, "IDR": 16479.65, "ILS": 3.57, "IMP": 0.792, "INR": 87.32,
                       "IQD": 1312.32, "IRR": 42000.89, "ISK": 138.91, "JEP": 0.792, "JMD": 157.86, "JOD": 0.709,
                       "JPY": 149.8, "KES": 129.26, "KGS": 87.43, "KHR": 4016.09, "KID": 1.6, "KMF": 472.07,
                       "KRW": 1446.08, "KWD": 0.309, "KYD": 0.833, "KZT": 500.19, "LAK": 21696.63, "LBP": 89500,
                       "LKR": 295.08, "LRD": 199.5, "LSL": 18.45, "LYD": 4.89, "MAD": 9.92, "MDL": 18.67,
                       "MGA": 4706.96, "MKD": 58.74, "MMK": 2102.69, "MNT": 3455.95, "MOP": 8.01, "MRU": 39.86,
                       "MUR": 46.27, "MVR": 15.47, "MWK": 1745.53, "MXN": 20.46, "MYR": 4.44, "MZN": 63.95,
                       "NAD": 18.45, "NGN": 1497.78, "NIO": 36.85, "NOK": 11.23, "NPR": 139.72, "NZD": 1.77,
                       "OMR": 0.384, "PAB": 1, "PEN": 3.69, "PGK": 4.03, "PHP": 57.99, "PKR": 280.01, "PLN": 3.98,
                       "PYG": 7919.13, "QAR": 3.64, "RON": 4.75, "RSD": 111.86, "RUB": 87.23, "RWF": 1426.87,
                       "SAR": 3.75, "SBD": 8.67, "SCR": 14.42, "SDG": 589.16, "SEK": 10.73, "SGD": 1.34, "SHP": 0.792,
                       "SLE": 22.89, "SLL": 22891.37, "SOS": 572.49, "SRD": 35.59, "SSP": 4417.34, "STN": 23.51,
                       "SYP": 13020.17, "SZL": 18.45, "THB": 33.99, "TJS": 10.95, "TMT": 3.5, "TND": 3.17, "TOP": 2.39,
                       "TRY": 36.52, "TTD": 6.77, "TVD": 1.6, "TWD": 32.89, "TZS": 2599.23, "UAH": 41.52,
                       "UGX": 3681.24, "UYU": 42.82, "UZS": 12875.65, "VES": 64.25, "VND": 25549.96, "VUV": 123.58,
                       "WST": 2.82, "XAF": 629.43, "XCD": 2.7, "XDR": 0.761, "XOF": 629.43, "XPF": 114.51, "YER": 247.7,
                       "ZAR": 18.45, "ZMW": 28.4, "ZWL": 26.55}
    """Получаем курс обмена USD к указанной валюте."""
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates'].get(to_currency, 1)  # Возвращаем курс или 1, если валюта не найдена
    else:
        return dict_currencies.get(to_currency, 1)  # Если API не доступен, то ищем в словаре, если а там нет, то возвращаем 1
