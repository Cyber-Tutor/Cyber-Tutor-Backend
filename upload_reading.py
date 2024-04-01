import os
import argparse
from firebase import Firebase


"""
Upload reading to firebase
Can upload a single reading file or all reading files in a directory
"""
def upload_reading(section, chapter, reading_path, group):
    db = Firebase()

    # if reading path is a directory, upload all reading files in the directory
    if os.path.isdir(reading_path):
        for file in os.listdir(reading_path):
            if file.endswith(".txt"):
                # get difficulty for each reading file from file name
                difficulty = "beginner" if "beginner" in file else "intermediate" if "intermediate" in file else "expert" if "expert" in file else None
                if difficulty:
                    reading_file_path = os.path.join(reading_path, file)
                    reading = load_reading(reading_file_path)
                    db.create_reading(section, chapter, group, reading, difficulty)
    else:
        # if reading path is a file, upload the reading file
        reading = load_reading(reading_path)
        file = os.path.basename(reading_path)
        difficulty = "beginner" if "beginner" in file else "intermediate" if "intermediate" in file else "expert" if "expert" in file else None
        if difficulty:
            db.create_reading(section, chapter, group, reading)


"""
Load reading from file
"""
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
    parser.add_argument('--section', type=str, help='section for the reading', required=True)
    parser.add_argument('--chapter', type=str, help='chapter for the reading', required=True)
    parser.add_argument('--group', type=str, help='group for the reading', default='experimental')
    # optional arguments
    args = parser.parse_args()

    upload_reading(args.section, args.chapter, args.reading_path, args.group)
    # python upload_reading.py --reading_path content_generation/content/reading/2fa --section two_factor_authentication --chapter introduction_to_2fa