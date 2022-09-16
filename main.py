import json
import os
from json import JSONDecodeError
import argparse
import operator


def get_all_boards(folder):
    files = os.listdir(folder)

    # get boards list
    boards = []
    for file in files:
        # if isn't JSON file, continue
        if file.split('.')[-1] != 'json':
            continue

        path = os.path.join(folder + '\\' + file)
        f = open(path)
        try:
            data = json.load(f)
        except JSONDecodeError:
            f.close()
            continue

        for d in data['boards']:
            if d['vendor'] is None or d['name'] is None:
                continue
            else:
                boards.append(d)

        f.close()

    # sort boards alphabetically first by vendor, then by name
    boards.sort(key=operator.itemgetter('vendor', 'name'))

    return boards


def get_metadata(boards):
    # get total vendors
    vendors = set()
    for board in boards:
        vendors.add(board['vendor'])
    total_vendors = len(vendors)

    # get total boards
    total_boards = len(boards)
    return {'total_vendors': total_vendors, 'total_boards': total_boards}


def get_single_json_file(folder):
    # generate all boards
    boards = get_all_boards(folder)

    # generate metadata
    metadata = get_metadata(boards)

    # combine boards and _metadata object
    output = {'boards': boards, '_metadata': metadata}
    with open('./boards.json', 'w') as fp:
        json.dump(output, fp)


def get_folder_route():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', help="input the route of folder")
    args = parser.parse_args()
    return args.r


def main():
    # get the route of folder which covers JSON files
    folder = get_folder_route()

    # handle JSON files
    get_single_json_file(folder)


if __name__ == '__main__':
    main()
