import os
import requests # type: ignore

def call_ollama_api(model, prompt):
	"""
	Call the OLLAMA API with the given model and prompt.

	Args:
	model (str): The model to be used.
	prompt (str): The prompt to be used.

	Returns:
	str: The output from the OLLAMA API.
	"""
	ollama_api_url = 'http://localhost:11434/api/generate'
	data = {
    "model": f"{model}",
    "prompt": f"{prompt}",
		# "system": "You are an undergraduate student participating in a lab experiment. You play a game with an anonymous player in which you simultaneously make a choice. You have to make one choice and one choice only.",
    "stream": False
}
	response = requests.post(ollama_api_url, json=data)
	return response.json()['response']

def save_output(exp, output, model, game, output_dir):
	"""
	Save the output to a file.

	Args:
	exp (int): The experiment number.
	output (str): The output to be saved.
	model (str): The model used to generate the output.
	game (str): The game used to generate the output.
	output_dir (str): The directory where the output file will be saved.
	"""
	filename = f"exp{exp}_{model}_{game}.txt"
	filepath = os.path.join(output_dir, filename)
	with open(filepath, 'w', encoding="utf-8") as file:
		file.write(output)

if __name__ == "__main__":
	models = ['llama2', 'llama3', 'phi3', 'gemma', 'mistral']
	prompts = {
		'sh': f"You are an undergraduate student participating in a lab experiment. You play a game with an anonymous player in which you simultaneously make a choice. Your payoff depends on both choices. If you both pick R, you each get 100$. If you choose R while they choose B, you get 10$, and they get 65$. Similarly, if you pick B while they pick R, you get 65$, and they get 10$. If you both pick B, you each earn 35$. The game has only one round. What's your choice? Perform reasoning as a human player. Append your choice letter in curly brackets as a last character.",
		'pd': f"You are an undergraduate student participating in a lab experiment. You play a game with an anonymous player in which you simultaneously make a choice. Your payoff depends on both choices. If you both pick R, you each get 65$. If you choose R while they choose B, you get 10$, and they get 100$. Similarly, if you pick B while they pick R, you get 100$, and they get 10$. If you both pick B, you each earn 35$. The game has only one round. What's your choice? Perform reasoning as a human player. Append your choice letter in curly brackets as a last character.",
		'hd': f"You are an undergraduate student participating in a lab experiment. You play a game with an anonymous player in which you simultaneously make a choice. Your payoff depends on both choices. If you both pick R, you each get 65$. If you choose R while they choose B, you get 35$, and they get 100$. Similarly, if you pick B while they pick R, you get 100$, and they get 35$. If you both pick B, you each earn 10$. The game has only one round. What's your choice? Perform reasoning as a human player. Append your choice letter in curly brackets as a last character."
		# 'sh': f"You are a stag-hunter. You need to decide whether to hunt alone or join a group. If you're alone, you'll get 10 points for your stag. But if you're with a group, you can catch a bigger stag and share the points (20 each). However, there's a risk that other hunters will steal your stag if you're in a group. Would you play it safe and hunt alone, or take the risk and join a group?. Give your reasoning, and append your choice in a new line at the end in square brackets 'A' if alone, 'G' if group.",
		# 'pd': f"You've been arrested for a crime and are being interrogated by the police. If you confess and tell them everything, they'll go easy on you and give you 1 year in prison. But if your partner remains silent and doesn't confess, they'll get 3 years while you get off scot-free. What's the best thing to do - confess and cooperate with the police, or stay quiet and hope for the best?  Give your reasoning, and append your choice in a new line at the end in square brackets 'C' if confess, 'S' if silent.",
		# 'hd': f"You're playing a game of hawk-dove with another player. If you play dove (retreat) and they play hawk (attack), you'll lose 1 point. But if you play hawk and they play dove, you'll win 2 points! What's the best strategy for you - play hawk and try to bully your opponent, or play dove and hope they back down? Give your reasoning, and append your choice in a new line at the end in square brackets 'H' if hawk, 'D' if dove."
	}
	num_experiments = 5

	for model in models:
		for exp in range(1, num_experiments + 1):
			for game in prompts.keys():
				print(f"Calling OLLAMA API for model [{model}] and game [{game}]")
				output = call_ollama_api(model, prompts[game])
				print('-'*50)
				print(f"Model: {model}")
				print(f"Game: {game}")
				print(f"Output: {output}")
				print('-'*50)
				print('Saving output to file')
				save_output(exp, output, model, game, 'out')