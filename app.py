from flask import Flask, jsonify, request
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10
number_window = deque(maxlen=WINDOW_SIZE)
VALID_IDS = {'p', 'f', 'e', 'r'}

@app.route('/')
def home():
    return "Welcome to the Average Calculator API. Use /numbers/{p|f|e|r}?numbers=[num1,num2,...]."

@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in VALID_IDS:
        return jsonify({"error": "Invalid ID. Use p, f, e, or r."}), 400

    prev_state = list(number_window)

    # Get numbers from query parameter
    try:
        numbers = request.args.get('numbers', '')
        if numbers:
            # Parse numbers from query parameter (e.g., "[2,1,8,3]")
            numbers = numbers.strip('[]').split(',')
            numbers = [int(num) for num in numbers if num.strip().isdigit()]
        else:
            numbers = []
    except ValueError:
        return jsonify({"error": "Invalid numbers format. Use numbers=[num1,num2,...] with integers."}), 400

    # Add numbers to window if they are unique
    for num in numbers:
        if num not in number_window:
            number_window.append(num)

    curr_state = list(number_window)
    avg = round(sum(curr_state) / len(curr_state), 2) if curr_state else 0.0

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": numbers,
        "avg": avg
    })

if __name__ == '__main__':
    app.run(port=9876)