import argparse
from glob import glob
import jupytext
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('base', type=str)
parser.add_argument('students', type=str, nargs='+')

args = parser.parse_args()

rel_path = args.base #'../../GPacBase/'
file_exclude = ['.pyc', '.pyo']
provided_code = set()

assert Path(rel_path).is_dir(), f"Directory {rel_path} doesn't exist!"
filenames = glob(rel_path + '**/*' + '.py' + '*', recursive=True)
filenames = [i for i in filenames if not any([ex for ex in file_exclude if ex in i])]
for filename in filenames:
	with open(filename) as file:
		for line in file:
			code = line.strip() 
			if code != '':
				provided_code.add(code)

filenames = glob(rel_path + '**/*' + '.ipynb' + '*', recursive=True)
filenames = [i for i in filenames if not any([ex for ex in file_exclude if ex in i])]
for filename in filenames:
	notebook = jupytext.read(filename, fmt='py')
	for cell in notebook['cells']:
		if cell['cell_type'] == 'code':
			source = cell['source']
			for line in source.split('\n'):
				code = line.strip()
				if code != '':
					provided_code.add(code)

for student_dir in args.students:
	filenames = glob(student_dir + '**/*' + '.py' + '*', recursive=True)
	filenames = [i for i in filenames if not any([ex for ex in file_exclude if ex in i])]
	for filename in filenames:
		cleanfile = list()
		with open(filename) as file:
			for line in file:
				code = line.strip() 
				if code != '' and code not in provided_code:
					cleanfile.append(code)
		localfile = filename.lstrip('./')
		localdir = localfile.rpartition('/')[0]
		if localdir != '':
			Path(f'./diff/{localdir}').mkdir(parents=True,exist_ok=True)
		
		if cleanfile:
			with open(f'./diff/{localfile}', mode='w') as file:
				for i in range(len(cleanfile)-1):
					cleanfile[i] = f'{cleanfile[i]}\n'
				for line in cleanfile:
					file.write(line)

	filenames = glob(student_dir + '**/*' + '.ipynb' + '*', recursive=True)
	filenames = [i for i in filenames if not any([ex for ex in file_exclude if ex in i])]
	for filename in filenames:
		cleanfile = list()
		notebook = jupytext.read(filename, fmt='py')
		for cell in notebook['cells']:
			if cell['cell_type'] == 'code':
				source = cell['source']
				for line in source.split('\n'):
					code = line.strip()
					if code != '' and code not in provided_code:
						cleanfile.append(code)
		localfile = filename.lstrip('./')
		localdir = localfile.rpartition('/')[0]
		if localdir != '':
			Path(f'./diff/{localdir}').mkdir(parents=True,exist_ok=True)
		
		if cleanfile:
			with open(f'./diff/{localfile}', mode='w') as file:
				for i in range(len(cleanfile)-1):
					cleanfile[i] = f'{cleanfile[i]}\n'
				for line in cleanfile:
					file.write(line)