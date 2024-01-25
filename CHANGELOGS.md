# Release 0.0.1

#### Requirements

- Python installed on your computer
- requirements.txt installed

### Minimum System Requirements (for Stockfish)

> ### Windows & Linux-Ubuntu
> https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX2

#### How to install required libraries?

Download zip file and extract it in a directory then open command line and then type the below things

```cmd
pip install -r requirements.txt
```

**Full Changelog**: https://github.com/shijian-wow/Python-Chess-GUI/commits/0.0.1

# Release 0.0.2

#### Requirements

- Python installed on your computer
- requirements.txt installed

### Minimum System Requirements (for Stockfish)

> #### Windows & Linux-Ubuntu
> https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX2

### How to install required libraries?

Download zip file and extract it in a directory then open command line and then type the below things

```cmd
pip install -r requirements.txt
```

### What are new?

* Bugs fixed
  - Bot gets disabled for a turn and forces you to play as white (changes color of the players) > Fixed
* News
  - When you reset the board, If you have imported a FEN code, It will start with that FEN code again
  
**Full Changelog**: https://github.com/shijian-wow/Python-Chess-GUI/compare/0.0.1...0.0.2

# Release 0.1.1

### Requirements

- Python installed on your computer
- requirements.txt installed

## Minimum System Requirements (for Stockfish)

> ### Windows & Linux-Ubuntu
> https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX2

### How to install required libraries?

Download zip file and extract it in a directory then open command line and then type the below things

```cmd
pip install -r requirements.txt
```

## What are new?

* Bugs fixed
  - Kings and Queens were at wrong square and that might make confusing on players, So we flipped board 
  
* News
  - New hotkey 'u' that unmakes (undos) the move
  - New -> Rendering algebraic notations (chess notations)
  - New file 'setup.sh' to install requirements (required libraries) in Linux-Ubuntu
  - New file 'setup.bat' to install requirements (required libraries) in Windows

* Updates
  - Changed the checkmate - check effect
  
* Performance
  - We fixed the game source code, So users can play game with very low lag and high frame rate

**Full Changelog**: https://github.com/shijian-wow/Python-Chess-GUI/compare/0.0.2...0.1.1
