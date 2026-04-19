import sys
import random
import json
import os
from typing import List, TypedDict

class GuessHistory(TypedDict):
    guess: str
    feedback: str

class GameState(TypedDict):
    answer: str
    guesses: int
    history: List[GuessHistory]
    status: str

WORDS_FILE: str = "sowpods.txt"
STATE_FILE: str = "state.json"

_cached_words: List[str] = []
_words_loaded: bool = False

def get_words() -> List[str]:
    #Retrieve and cache the SOWPODS 5-letter word list.
    global _cached_words, _words_loaded
    if _words_loaded:
        return _cached_words
        
    if not os.path.exists(WORDS_FILE):
        raise FileNotFoundError(f"Dictionary file '{WORDS_FILE}' not found.")
        
    with open(WORDS_FILE, "r") as f:
        words: List[str] = [line.strip().upper() for line in f if len(line.strip()) == 5]
        
    if not words:
        raise ValueError(f"Dictionary file '{WORDS_FILE}' contains no valid 5-letter words.")
        
    _cached_words = words
    _words_loaded = True
    return words

def load_state() -> GameState:
    #Load the game state from local JSON.
    if not os.path.exists(STATE_FILE):
        raise FileNotFoundError("out of guesses, please run python3 wordleserver create")
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state: GameState) -> None:
    #Persist the current game state to the local JSON
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def create_game() -> GameState:
    #Initialize a new Wordle session with a random answer.
    words: List[str] = get_words()
    answer: str = random.choice(words)
    state: GameState = {
        "answer": answer,
        "guesses": 0,
        "history": [],
        "status": "playing"
    }
    save_state(state)
    return state

def get_feedback(guess: str, answer: str) -> str:
    #Exact Wordle-style matching feedback for a guess.
    feedback: List[str] = ["🩶"] * 5
    answer_chars: List[str] = list(answer)
    guess_chars: List[str] = list(guess)
    
    for i in range(5):
        if guess_chars[i] == answer_chars[i]:
            feedback[i] = "💚"
            answer_chars[i] = "_"
            guess_chars[i] = "_"
            
    for i in range(5):
        if guess_chars[i] != "_" and guess_chars[i] in answer_chars:
            feedback[i] = "💛"
            idx: int = answer_chars.index(guess_chars[i])
            answer_chars[idx] = "_"
            
    return "".join(feedback)

def make_guess(guess: str) -> GameState:
    #User guess against the active game session.
    state: GameState = load_state()
        
    if state["status"] != "playing":
        raise ValueError("out of guesses, please run python3 wordleserver create")
        
    guess = guess.upper()
    words: List[str] = get_words()
    
    if guess not in words:
        raise ValueError("Invalid word. Please guess a 5-letter word from SOWPODS.")
        
    state["guesses"] += 1
    feedback: str = get_feedback(guess, state["answer"])
    state["history"].append({"guess": guess, "feedback": feedback})
            
    if feedback == "💚💚💚💚💚":
        state["status"] = "won"
    elif state["guesses"] >= 6:
        state["status"] = "lost"
        
    save_state(state)
        
    return state

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
        
    cmd: str = sys.argv[1].lower()
    
    try:
        if cmd == "create":
            create_game()
            print("New game created.")
        elif cmd == "guess":
            if len(sys.argv) >= 3:
                state = load_state()
                if state["status"] != "playing":
                    print("out of guesses, please run python3 wordleserver create")
                else:
                    state = make_guess(sys.argv[2])
                    if state["history"] and state["history"][-1]["guess"] == sys.argv[2].upper():
                        print(state["history"][-1]["feedback"])
    except Exception as e:
        print(e)
