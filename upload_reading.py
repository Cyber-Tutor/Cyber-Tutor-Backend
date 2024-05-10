import os
import argparse
from firebase import Firebase


def upload_reading(section, chapter, reading_path, group):
    db = Firebase()

    if os.path.isdir(reading_path):
        for file in os.listdir(reading_path):
            if file.endswith(".txt"):
                reading_file_path = os.path.join(reading_path, file)
                reading = load_reading(reading_file_path)
                db.store_reading(section, chapter, reading, group)
    else:
        reading = load_reading(reading_path)
        db.store_reading(section, chapter, reading, group)


def load_reading(reading_path):
    with open(reading_path, 'r') as f:
        reading = f.readlines()
    return ''.join(reading)


if __name__ == '__main__':
    """
    Store reading from file/directory into firebase
    """
    parser = argparse.ArgumentParser(description='Store reading into firebase')
    parser.add_argument('--reading_path', type=str, help='reading path for a file or directory containing readings', required=True)
    parser.add_argument('--group', type=str, help='group for the reading', required=True)
    parser.add_argument('--section', type=int, help='section for the reading', required=True)
    parser.add_argument('--chapter', type=int, help='chapter for the reading', required=True)
    args = parser.parse_args()

    upload_reading(args.section, args.chapter, args.reading_path, args.group)