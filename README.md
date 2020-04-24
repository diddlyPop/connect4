# connect4
Connect 4 AI

Project goals:
- Connect4 console game, two player
  - Uses numpy for efficient board computation
  - Provide framework for agents to be placed in as players and access game data
- Build AlphaZero-style agent for connect4
  - Neural network / Monte carlo search tree
  - Train and apply agent to console style game
- Deploy api for interfacing with our trained Connect4 agent
- Deploy GUI version of game
  - Pygame or web app

<hr>

AlphaZero
============
The AlphaZero algorithm runs three processes in parallel:
- Monte-Carlo search tree self-play, guided by the policy and value given by the neural network for each move
- Constant training on the turns from the Monte-Carlo search tree self-play
- Evaluation of the neural networks performance at pre-defined checkpoints, uses best model

Our Architecture
============
Our neural network model takes as input the current board state in a binary format. The AlphaGo Zero model sends as input both players board states in a binary format and a few previous board states for each player. We will first construct our model using only the two players board states in a binary format, and hope to later iterate on the network architecture.

The network will have two ouput nodes at the head of the network. The policy output is a list of probabilities mapped to each possible move. The value output displays the amount of turns until a player is expected to lose or to win.

The policy output is a great indicator of what moves are the best at the current board state. It makes sense to assume that this would be more than enough to base the agent's decisions off of. The value head is tremenedously helpful in determining what is expected to happen in x turns from now. The Monte-Carlo Search Tree utilizes the value head to restrict the overrall search space while still making informed decisions about what will happen in the future. The combination of both outputs is key to the agent's artificial intuition of the current state of play.

Todo
============
Neural network currently takes current board state as a 6x7 numpy matrix as input, and outputs a policy distribution to predict the best move. Without the MCTS the state-space is too high to get a good training in a short period of time. After about 10,000 rounds the agent would win quickly against a RandomAgent. When playing against a Human, it is easily outwitted.

- The input layer should be expanded to an input block. Extra layers should be added that consist of previous turn states.
- The value head needs to be implemented using the MCTS traversal.
- An API needs to be developed, likely in flask, to interface with the game as a WebAgent.
- Front end can be a simple grid with colored buttons representing the current board state.
