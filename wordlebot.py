import sys
import random
import os
from typing import List, Dict, Set

import wordleserver

def filter_words(words: List[str], guess: str, feedback: str) -> List[str]:
    #Filter words based on emoji feedback from the previous guess.
    must_have_at_index: Dict[int, str] = {}
    must_not_have_at_index: Dict[int, Set[str]] = {}
    must_in_word: Dict[str, int] = {}
    greyed_letters: Set[str] = set()
    
    for i in range(5):
        letter: str = guess[i]
        status: str = feedback[i]
        
        if status == "💚":
            must_have_at_index[i] = letter
            must_in_word[letter] = must_in_word.get(letter, 0) + 1
        elif status == "💛":
            must_not_have_at_index.setdefault(i, set()).add(letter)
            must_in_word[letter] = must_in_word.get(letter, 0) + 1
        elif status == "🩶":
            if letter not in must_in_word:
                greyed_letters.add(letter)
            else:
                must_not_have_at_index.setdefault(i, set()).add(letter)

    def is_valid(word: str) -> bool:
        for idx, letter in must_have_at_index.items():
            if word[idx] != letter:
                return False
                
        for idx, letters in must_not_have_at_index.items():
            if word[idx] in letters:
                return False
                
        for letter, min_count in must_in_word.items():
            if word.count(letter) < min_count:
                return False
                
        for char in word:
            if char in greyed_letters and char not in must_in_word:
                return False
                
        for letter in guess:
            if letter in must_in_word and letter in greyed_letters:
                if word.count(letter) > must_in_word[letter]:
                    return False
                    
        return True
        
    return [w for w in words if is_valid(w)]

def bot_attempt() -> bool:
    #Play a single game of Wordle autonomously
    wordleserver.create_game()
    print("Game successfully created.")
    words: List[str] = wordleserver.get_words()
        
    for attempt in range(6):
        if not words: break
            
        guess: str = random.choice(words)
        print(f"Word guessed: {guess}")
        
        state: wordleserver.GameState = wordleserver.make_guess(guess)
        feedback: str = state["history"][-1]["feedback"]
        
        print(f"Feedback received: {feedback}")
        
        if feedback == "💚💚💚💚💚":
            print("Victory!")
            return True
            
        words = filter_words(words, guess, feedback)
        
    print("Failure.")
    return False

def evaluate() -> None:
    #Run 100 attempts and report the win rate.
    print("\n--- Running Evaluation (100 Games) ---")
    wins: int = 0
    num_games: int = 100
    
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        for _ in range(num_games):
            if bot_attempt():
                wins += 1
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout
            
    print(f"Bot Win Rate: {wins}/{num_games}")

if __name__ == "__main__":
    cmd: str = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    
    if cmd == "attempt":
        bot_attempt()
    elif cmd == "evaluate":
        evaluate()
    else:
        print("Usage: python3 wordlebot.py attempt | evaluate")
