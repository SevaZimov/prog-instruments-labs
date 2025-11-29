import pandas as pd
import re
from checksum import calculate_checksum, serialize_result


def find_errors(df, cleaning_rules):
    error_rows = set()
    for column, pattern in cleaning_rules.items():
        if column in df.columns:
            for idx, value in df[column].items():
                if not re.match(pattern, str(value)):
                    error_rows.add(idx)

    error_rows_list = list(error_rows)
    return error_rows_list


def main():
    var = 11
    rules = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'height': r'^[1-2]\.\d{1,2}$',
        'snils': r'^\d{11}$',
        'passport': r'^\d{2} \d{2} \d{6}$',
        'occupation': r'^[а-яА-Яa-zA-Z\s\-\.,]+$',
        'longitude': r'^-?(1[0-7][0-9]|[0-9]{1,2})\.\d+$',
        'hex_color': r'^#[0-9A-Fa-f]{6}$',
        'issn': r'^\d{4}-\d{4}$',
        'locale_code': r'^[a-z]{2}(-[a-z]{2,4})?$',
        'time': r'^([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\.[0-9]{6}$'
    }
    try:
        df = pd.read_csv('11.csv',
                         encoding='utf-16',
                         delimiter=';',
                         engine='python')
        result = find_errors(df, rules)
        print(len(result))
        checksum = calculate_checksum(result)
        print(checksum)
        serialize_result(var,checksum)
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()