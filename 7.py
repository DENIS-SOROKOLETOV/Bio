import os
import re
import statistics


def list_files(directory: str) -> list:

    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


def only_correct_suffix(file_list: list, suff=".txt") -> list:

    correct_paths = []
    for path in file_list:
        if path.endswith(suff):
            correct_paths.append(path)
    return correct_paths


def records_filter(file_list: list, max_records=50) -> list:

    selected_files = []
    pattern = re.compile(r'^\d+\s+')
    for file in file_list:
        with open(file, 'r') as f:
            lines = f.readlines()
            count = 0
            for line in lines:
                if pattern.match(line):
                    count += 1
            if count <= max_records + 1:
                selected_files.append(file)
    return selected_files


def valid_researches(file_list: list) -> list:

    researches = []
    for file in file_list:
        with open(file, 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                if line:
                    id, name, hour, machine, seq = line.strip().split('\t')

                    # Invalid research contains sequence of repeating letter
                    if len(set(seq)) > 1:
                        new_research = {
                            'id': id,
                            'name': name,
                            'hour': hour,
                            'machine': machine,
                            'seq': seq
                        }
                        researches.append(new_research)
    return researches


def max_tenacity(researches_list: list) -> tuple:

    employees = {}
    for res in researches_list:
        name = res['name']
        employees[name] = employees.get(name, 0) + 1

    best = max(employees, key=employees.get)
    return (best, employees[best])


def hottest_work_hour(researches_list: list) -> dict:

    machines_whs = {}
    for res in researches_list:
        machine = res['machine']
        current_wh = machines_whs.get(machine, [])
        machines_whs[machine] = machines_whs.get(
            machine, []) + [int(res['hour'])]

    machines_hottest = {k: statistics.mode(
        machines_whs[k]) for k in sorted(machines_whs.keys())}

    return machines_hottest


def main():
    directory_name = input()
    assert (os.path.exists(directory_name)), "no such directory"

    all_files = list_files(directory_name)
    correct_suffs = only_correct_suffix(all_files)
    no_more_than_50 = records_filter(correct_suffs)
    researches = valid_researches(no_more_than_50)

    top_name, max_logged = max_tenacity(researches)
    machines_wh = hottest_work_hour(researches)

    for k in machines_wh.keys():
        print(k, machines_wh[k], sep=":")
    print(top_name, max_logged, sep=':')


if __name__ == "__main__":
    main()