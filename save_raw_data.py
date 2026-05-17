import sys, json

# python-shell からは UTF-8 で JSON が流れてくるため明示的に固定する
# (Windows のデフォルト cp932 だと非 ASCII の文字キーで例外になる)
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")


def get_data():
    x_y = sys.stdin.readline()
    return x_y


def main():
    """平均化前の生の点群データを raw_x_y.json に追記保存する。

    入力(stdin): {"<文字>": [[{"x": [...], "y": [...]}, ...], ...]}
        - 外側の配列 : 同じ文字を書いた回数分のリスト
        - 内側の配列 : 一文字分の画ごとの点群
        - 各要素     : 1画分の x, y 座標列

    既存ファイルに同じ文字のエントリがあれば、書いた回数分を追記する。
    """
    raw_str = get_data()
    add_dict = json.loads(raw_str)

    json_dict = {}
    try:
        with open('raw_x_y.json', 'r', encoding='utf-8') as read_f:
            json_dict = json.load(read_f)
    except (FileNotFoundError, json.JSONDecodeError):
        json_dict = {}

    for char, drawings in add_dict.items():
        if char in json_dict and isinstance(json_dict[char], list):
            json_dict[char].extend(drawings)
        else:
            json_dict[char] = drawings

    with open('raw_x_y.json', 'w', encoding='utf-8') as write_f:
        json.dump(json_dict, write_f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
