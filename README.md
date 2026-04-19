# Wordle CLI & Auto-Solver Bot

This project implements a command-line version of the popular game Wordle, paired with an automated bot that can intelligently play and solve the game.

## Project Structure

- `wordleserver.py`: The game engine/API. It manages the game state, handles guesses, and returns emoji feedback (💚, 💛, 🩶).
- `wordlebot.py`: The automated player. It interfaces with the server, creates games, and uses an intelligent feedback-filtering strategy to guess the word within 6 tries.
- `sowpods.txt`: The dictionary file containing valid Scrabble/Wordle words.
- `state.json`: A state file generated during active games to track game progress across CLI executions.

## Prerequisites

- Python 3.12.1 (or compatible 3.x version)

## How to Play Manually (The Server)

You can play the game yourself via the command line.

1. **Create a new game:**
   ```bash
   python3 wordleserver.py create
   ```
2. **Make a guess** (must be a 5-letter word):
   ```bash
   python3 wordleserver.py guess APPLE
   ```
   You will receive feedback in the form of emojis:
   - 💚 (Green): Correct letter in the correct position.
   - 💛 (Yellow): Correct letter in the wrong position.
   - 🩶 (Grey): Letter is not in the word.

Keep guessing until you win or run out of your 6 guesses!

## How to Run the Bot

The bot plays the game autonomously using the list of valid words.

1. **Watch the bot play a game:**
   ```bash
   python3 wordlebot.py attempt
   ```
   The bot will create a game, print its series of guesses, and show the feedback it receives until it successfully solves the puzzle or runs out of attempts.

2. **Evaluate the bot's performance:**
   ```bash
   python3 wordlebot.py evaluate
   ```
   This command runs a benchmarking simulation:
   - 100 games played by the bot (which uses feedback to filter the word list).
   
   It will output the win rate to show the efficiency of the strategy.
