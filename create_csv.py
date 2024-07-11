import os
import pandas as pd # type: ignore
import re

def create_summary_df(logs_directory):
	"""
	Generate a DataFrame with results summary.

	Explanation for each column:
	- 'file': The name of the log.
	- 'game': The type of game played ('sh', 'pd', 'hd').
	- 'error_type': The type of error encountered in reasoning
	- 'sentence': Sentence(s) containing an error.
	- 'choice': Chosen action
	- 'correct': Indicates whether the reasoning was correct (binary: 0 or 1).
	The following columns are filled automatically: 'file', 'game', 'choice'
	The following has to be later filled manually: 'error_type', 'sentence', 'correct'

	Returns:
	DataFrame: A DataFrame sorted by the 'file' column.
	"""
	data = []
	for file_name in os.listdir(logs_directory):
		if file_name.endswith('.txt'):
			row = []
			name = file_name
			row.append(name)

			splitted_name = name.split("_")
			game = splitted_name[2].replace(".txt", "")
			row.append(game)
			row += ["", ""]

			with open(os.path.join(logs_directory, file_name)) as result_file:
				content = result_file.read()
				choice = get_choices(content)
				row += [choice]

				row += [""]

			data.append(row)

	df = pd.DataFrame(data)
	df.columns = ["file", "game", "err_type", "sentence", "choice", "correct"]
	return df.sort_values('file')


def create_csv(exp_dir):
	"""
	Create a CSV file from experiment data.

	This function generates a CSV file containing summarized data from the experiment log directory.

	Args:
	exp_dir (str): The directory containing experiment logs.
	"""
	df = create_summary_df(exp_dir)
	print(df)
	df.to_csv('summary.csv', index=False)


def get_choices(log):
	matches = re.findall("{[A-Z]}", log)
	if len(matches) == 0:
		print("No curly braces detected, the file has to be evaluated manually")
		return ""
	return matches[-1]


if __name__ == '__main__':
	create_csv('out') # 'LOGS_DIRECTORY' is a directory containing SLMs responses in .txt files
