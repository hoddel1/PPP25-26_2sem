import random
import sys

ROCK = 'rock'
SCISSORS = 'scissors'
PAPER = 'paper'

PLAYER_WIN = 'player'
COMPUTER_WIN = 'computer'
DRAW = 'draw'

WIN_SCORE = 3

WIN_RULES = {
    ROCK: SCISSORS,
    SCISSORS: PAPER,
    PAPER: ROCK
}

def get_computer_move():
    return random.choice([ROCK, SCISSORS, PAPER])


def determine_winner(player_move, computer_move):
    if player_move == computer_move:
        return DRAW
    elif WIN_RULES[player_move] == computer_move:
        return PLAYER_WIN
    else:
        return COMPUTER_WIN

def display_move(move):
    moves = {
        ROCK: "Камень",
        SCISSORS: "Ножницы",
        PAPER: "Бумага"
    }
    return moves.get(move, move)

def display_score(player_score, computer_score):
    print(f"\nСчёт: Игрок {player_score} : {computer_score} Компьютер")


def display_round_result(player_move, computer_move, winner):
    print(f"\nИгрок: {display_move(player_move)}")
    print(f"Компьютер: {display_move(computer_move)}")
    
    if winner == PLAYER_WIN:
        print("Вы выиграли этот раунд!")
    elif winner == COMPUTER_WIN:
        print("Компьютер выиграл этот раунд!")
    else:
        print("Ничья!")


def display_match_winner(winner):
    if winner == PLAYER_WIN:
        print("Поздравляем! Вы выиграли матч!")
    else:
        print("Компьютер выиграл матч. Попробуйте снова!")


def is_valid_move(move):
    return move in [ROCK, SCISSORS, PAPER]


def process_command(command, player_score, computer_score):
    if command == 'score':
        display_score(player_score, computer_score)
        return True, player_score, computer_score 
    
    elif command == 'restart':
        print("\nИгра перезапущена! Счёт обнулён.")
        return True, 0, 0  
    
    elif command == 'exit':
        print("\nСпасибо за игру! До свидания!")
        return False, player_score, computer_score
    
    return None, player_score, computer_score  
  
def play_match():
    player_score = 0
    computer_score = 0
    
    print("Игра 'Камень-ножницы-бумага'")
    print(f"Матч идёт до {WIN_SCORE} побед.")
    print("Доступные ходы: rock, scissors, paper")
    print("Специальные команды: score, restart, exit")
    
    while player_score < WIN_SCORE and computer_score < WIN_SCORE:
        display_score(player_score, computer_score)
        
        user_input = input("\nВаш ход или команда: ").strip().lower()
        
        if not user_input:
            print("Ошибка: введите ход или команду.")
            continue
        
        if user_input in ['score', 'restart', 'exit']:
            result, new_player, new_computer = process_command(user_input, player_score, computer_score)
            
            if result is False:
                return False
            elif result is True:
                player_score, computer_score = new_player, new_computer
                if user_input == 'restart':
                    continue 
                else:  
                    continue
       
        if not is_valid_move(user_input):
            print(f"Ошибка: '{user_input}' - недопустимый ход.")
            print("Допустимые ходы: rock, scissors, paper")
            print("Команды: score, restart, exit")
            continue
        
        player_move = user_input
        computer_move = get_computer_move()
        winner = determine_winner(player_move, computer_move)
        
        display_round_result(player_move, computer_move, winner)
        
        
        if winner == PLAYER_WIN:
            player_score += 1
        elif winner == COMPUTER_WIN:
            computer_score += 1
        
        if player_score >= WIN_SCORE or computer_score >= WIN_SCORE:
            display_score(player_score, computer_score)
    
    if player_score >= WIN_SCORE:
        display_match_winner(PLAYER_WIN)
    else:
        display_match_winner(COMPUTER_WIN)
    
    return True 


def main():
    while True:
        should_continue = play_match()
        
        if not should_continue:
            break
        
        while True:
            answer = input("Хотите сыграть ещё один матч? (да/нет): ").strip().lower()
            if answer in ['да', 'yes', 'y', 'lf']:
                print("\nНачинаем новый матч!")
                break
            elif answer in ['нет', 'no', 'n', 'ytn']:
                print("\nСпасибо за игру! До свидания!")
                return
            else:
                print("Пожалуйста, ответьте 'да' или 'нет'.")

if __name__ == "__main__":
    main()
