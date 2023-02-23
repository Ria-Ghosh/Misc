# python3 assign_ids.py reassign --path 09_29_2022_product_copy/ --current 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 --new 1 0 0 1 0 1 1 0 0 1 1 1 1 1 1 1 1 1 1

import os
import sys
import fileinput
import argparse
from pathlib import Path

import cv2


def generate_id_map(old, new):
    id_map = dict(zip(old, new))
    return id_map


def remove_labels(files_path, id_list):
    """
    Reads txt files and deletes lables associated with the
    id_list provided
    """
    labels_updated = 0
    for file in os.listdir(files_path):
        if file.endswith('.txt'):
            with open(os.path.join(files_path, file), 'r') as f:
                lines = f.read().splitlines()
                for x in range(len(lines)):
                    split_label = lines[x].split(' ')
                    if split_label[0] in id_list:
                        lines[x] = "<del>"
                lines = list(filter(("<del>").__ne__, lines))
            with open(os.path.join(files_path, file), 'w') as f:
                f.write('\n'.join(lines))


def reassign_ids(files_path, id_map):
    """
    Reads txt files and replaces the object ids provided in the
    id_map
    """
    labels_updated = 0
    for root, dirs, files in os.walk(files_path):
        for file in files:
            if file.endswith('.txt'):
                for line in fileinput.input(os.path.join(root, file), inplace=1):
                    split_label = line.split(' ')
                    if split_label[0] in id_map:
                        split_label[0] = id_map[split_label[0]]
                        labels_updated += 1
                    sys.stdout.write(' '.join(split_label))
    print(f'Total labels reassigned: {labels_updated}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest="command")
    delete_op = sub_parser.add_parser("delete", help="Parser for deleting labels")
    delete_op.add_argument(
            '--path', 
            type=str, 
            help='source folder path', 
            required=True
            ) 
    delete_op.add_argument(
            '--id_list', 
            help='List of object ids to delete',
            nargs='+',
            default= [],
            required=True
            )
    reassign_op = sub_parser.add_parser("reassign", help="Parser for reassigning object label IDs")
    reassign_op.add_argument(
            '--path', 
            type=str, help='source folder path', 
            required=True
            ) 
    reassign_op.add_argument(
            '--current',
            nargs='+', 
            help='List of current ids to be replaced',
            default=[],
            required=True
            )
    reassign_op.add_argument(
            '--new',
            nargs='+', 
            help='List of new ids',
            default=[],
            required=True
            )
    args = parser.parse_args()
    print(args)
    if(args.command == 'reassign'):
        reassign_ids(args.path, generate_id_map(args.current, args.new))
    elif(args.command == 'delete'):
        remove_labels(args.path, args.id_list)

