import random, os, openai
from flask import Flask, render_template, request

openai.api_key = os.environ['GOOSE_API_KEY']
openai.api_base = "https://api.goose.ai/v1"

app = Flask(__name__)

def get_word(t):
    with open(f"words/{t}.txt", "r") as file:
        words = file.readlines()
    return random.choice(words)

def gen_stories():
    rand = random.randint(1, 3)
    if rand:
        place = get_word('places')
        return f"It was during the battle of {get_word('nouns')} when I was running through a {get_word('nouns')} when a {get_word('nouns')} went off right next to my platoon. Our {get_word('occupations')} yelled for us to {get_word('verbs')} to the nearest {place} we could find. When we got to the {place} we {get_word('verbs-ed')} to start a fire. As we were starting the fire the enemy saw the {get_word('nouns')} from the fire and started {get_word('verbs-ing')} {get_word('nouns')} at us. we all quickly ducked behind the {get_word('nouns')} at the {place} and returned fire. we quickly eliminated the enemy and were {get_word('emotions')} that we had won the battle."

@app.route('/')
def index():
    story_type = request.args.get("type")
    if story_type == "plain":
        return render_template("index.html", story=gen_stories())
    elif story_type == "ai":
        prompt = f"Generate a {get_word('genre')} short story with {get_word('names')} as the main character. They are a {get_word('occupations')} that lives in {get_word('places')}.\n\n--\n\n"
        start_list = ["One day, ", "Once upon a time, ", "It was during "]
        start = random.choice(start_list)
        completion = openai.Completion.create(
            engine="fairseq-2-7b",
            prompt=prompt+start,
            max_tokens=100,
            stream=True
        )
        comp = ""
        for c in completion:
            comp += c.choices[0].text
        return render_template("index.html", story=start+comp)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)