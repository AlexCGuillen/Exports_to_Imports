import os
import json
import pandas as pd
from copy import deepcopy

class ExportToCSV:
    def __init__(self, tasks):
        if isinstance(tasks, str) and tasks.endswith('.json'):
            if not os.path.exists(tasks):
                raise Exception(f'Task file not found {tasks}')
            with open(tasks, encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = tasks

    def _get_result_name(self, result):
        return result.get('from_name')

    def _minify_result(self, result):
        value = result['value']
        name = self._get_result_name(result)
        if len(value) == 1:
            item = next(iter(value.values()))
            if len(item) == 0:
                return {name: None}
            if len(item) == 1:
                return {name: item[0]}
            else:
                return {name: item}
        else:
            return value

    def _get_annotation_results(self, annotation, minify, flat_regions):
        results = annotation['result']
        if not flat_regions:
            yield {'result': results}
        for result in annotation['result']:
            if minify:
                yield self._minify_result(result)
            else:
                yield {self._get_result_name(result): result}

    def _get_annotator_id(self, annotation):
        annotator = annotation.get('completed_by', {})
        if isinstance(annotator, int):
            return annotator
        elif isinstance(annotator, dict):
            return annotator.get('email') or annotator.get('id')

    def to_records(self, minify=True, flat_regions=True):
        records = []
        for task in self.tasks:
            annotations = task.get('annotations')
            if annotations is None:
                annotations = task['completions']
            for annotation in annotations:
                record = {
                    'id': task['id'],
                    'annotation_id': annotation.get('id'),
                    'annotator': self._get_annotator_id(annotation),
                }
                record.update(task['data'])
                for result in self._get_annotation_results(annotation, minify, flat_regions):
                    rec = deepcopy(record)
                    rec.update(result)
                    records.append(rec)
        return records

    def to_dataframe(self, minify=True, flat_regions=True):
        return pd.DataFrame.from_records(self.to_records(minify, flat_regions))

    def to_file(self, file, minify=True, flat_regions=True, **kwargs):
        return self.to_dataframe(minify, flat_regions).to_csv(file, **kwargs)


def convert_all_json_in_folder(folder_path):
    """Batch convert all JSON files in a folder to CSV using ExportToCSV."""
    found = False
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    files = os.listdir(folder_path)
    print(f"First 2 files found in the folder: {files[:2]}")
    for filename in files:
        if filename.endswith('.json'):
            found = True
            json_path = os.path.join(folder_path, filename)
            csv_path = os.path.join(folder_path, filename.replace('.json', '.csv'))
            try:
                exporter = ExportToCSV(json_path)
                exporter.to_file(csv_path)
                if os.path.exists(csv_path):
                    print(f"Success: Created CSV file '{csv_path}' from '{json_path}'.")
                else:
                    print(f"Warning: CSV file '{csv_path}' was not created.")
            except Exception as e:
                print(f"Error processing '{json_path}': {e}")
    if not found:
        print("No JSON files found in the specified folder.")

if __name__ == "__main__":
    folder = input("Enter the path to the folder containing JSON files: ")
    convert_all_json_in_folder(folder)
