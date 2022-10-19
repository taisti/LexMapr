import argparse
import os

"""
A script that loads BRAT annotations and transforms it into a CSV processable by LexMapr.
example usage (assuming that BRAT annotation *.ann files are in ./brat/ folder and we want to
load first 50 annotation files): 

    python3 prepare_data.py --number_of_annotations_to_parse 50 --annotations_path ./brat/ --output_file_path ./data.csv

Each line in the data.csv file consists of a pair of elements separated with a comma, where:
- First element is a concatenated file and entity identifier
  (e.g., 10_T2, which means that it represents second entity from file 10.ann)
- The second element is a text representation of a given entity
"""

def main(number_of_annotations_to_parse: int, annotations_path: str, output_file_path: str):
    """ Entry point """
    with open(output_file_path, 'w') as out_file:
        for idx in range(number_of_annotations_to_parse):
            annotation_path = f"{annotations_path}/{idx}.ann"
            
            if not os.path.exists(annotation_path):
                continue
            
            with open(annotation_path) as in_file:
                for line in in_file:
                    annotation_parts = line.split('\t')
                    # filter out annotations that do not relate to entities
                    if len(annotation_parts) != 3:
                        continue

                    # filter out entities that do not relate to food products
                    if not annotation_parts[1].lower().startswith('food'):
                        continue

                    file_token_id = f"{idx}_{annotation_parts[0]}"
                    entity_text = annotation_parts[2].strip()
                    out_file.write(f"{file_token_id},{entity_text}\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number_of_annotations_to_parse',
                        help='Number of annotation files to process',
                        type=int,
                        required=True)
    parser.add_argument('-ap', '--annotations_path',
                        help='Path to BRAT annotations folder',
                        type=str,
                        required=True)

    parser.add_argument('-out', '--output_file_path',
                        help='Path to generated output file',
                        type=str,
                        default='./report.txt')

    args = parser.parse_args()
    main(args.number_of_annotations_to_parse, args.annotations_path, args.output_file_path)
