import os
import sys
import shutil


SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
PROBLEM_BASE_DIR = os.path.join(SCRIPT_PATH)
README_FILE = os.path.join(SCRIPT_PATH, 'README.md')
EXAMPLE_NOTEBOOK = os.path.join(SCRIPT_PATH, 'x.ipynb')
NOTEBOOK_FILE_PATH = ''


def create_notebook(id, name):
    notebook_file_path = os.path.join(PROBLEM_BASE_DIR, '{}.{}.ipynb'.format(id, name))
    if os.path.exists(notebook_file_path):
        raise Exception('Error: notebook:{} exists!'.format(notebook_file_path))
    shutil.copyfile(EXAMPLE_NOTEBOOK, notebook_file_path)
    global NOTEBOOK_FILE_PATH
    NOTEBOOK_FILE_PATH = notebook_file_path


def process_notebook(id, name, url):
    file_content = list()
    with open(NOTEBOOK_FILE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('%题目%', '{}.{}'.format(id, name))
            line = line.replace('%链接%', url)
            file_content.append(line)
    with open(NOTEBOOK_FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(file_content)


def process_readme(id, name, url):
    file_content = list()
    added_content = False
    with open(README_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            cells = line.split('|')
            if added_content or len(cells) != 6:
                file_content.append(line)
                continue
            try:
                cell_id = int(cells[1])
                if cell_id > id:
                    file_content += '| {} | [{}]({}) | [{}.ipynb]({}) | |\n'.format(
                        id, name, url, name, '{}.{}.ipynb'.format(id, name)
                    )
                    added_content = True
                elif cell_id == id:
                    raise Exception('重复的题目id:{}'.format(id))
                file_content.append(line)
            except:
                file_content.append(line)
        if not added_content:
            file_content += '| {} | [{}]({}) | [{}.ipynb]({}) | |\n'.format(
                        id, name, url, name, '{}.{}.ipynb'.format(id, name)
                    )
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.writelines(file_content)


def main():
    if len(sys.argv) < 4:
        print('start.py id name url')
        exit(1)
    id = int(sys.argv[1])
    name = sys.argv[2].replace(' ', '-')
    url = sys.argv[3]
    create_notebook(id, name)
    process_notebook(id, name, url)
    process_readme(id, name, url)
    os.system('code {}'.format(NOTEBOOK_FILE_PATH))


if __name__ == '__main__':
    main()
