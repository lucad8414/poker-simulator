from game import game, evaluate, Result
from card_types import Values, Symbols
from card import Cards
from random import randint
from hand import Hand

def analyze() -> tuple[list[Hand], list[Hand]]:
    """
    Runs one game and evaluates the result. Returns the winning hand and all the loosing hands.
    Does not differentiate between split pots.
    """

    players = randint(2, 21)
    result = game(players)
    (board, hands) = result

    evaluations: list[tuple[Hand, Result, tuple[list[Cards], list[Cards]]]] = [evaluate(board, hands[0])]
    
    split_pot = 1
    for hand in hands[1:]:
        current_evaluation = evaluate(board, hand)
        i = 0
        for evaluation in evaluations:
            if current_evaluation[0].value > evaluation[1].value:
                evaluations.insert(i, (hand, current_evaluation[0], current_evaluation[1]))
                if i == 0:
                    split_pot = 1
                break

            elif current_evaluation[0].value == evaluation[1].value:
                if current_evaluation[1][0][0] > evaluation[2][0][0]:
                    evaluations.insert(i, (hand, current_evaluation[0], current_evaluation[1]))
                    if i == 0:
                        split_pot = 1
                    break

                elif current_evaluation[1][0][0] == evaluation[2][0][0]:
                    if current_evaluation[1][0][1] > evaluation[2][0][1]:
                        evaluations.insert(i, (hand, current_evaluation[0], current_evaluation[1]))
                        if i == 0:
                            split_pot = 1
                        break

                    elif current_evaluation[1][0][1] == evaluation[2][0][1]:
                        evaluations.insert(i, (hand, current_evaluation[0], current_evaluation[1]))
                        if i == 0:
                            split_pot += 1
                        break

            i += 1

    assert len(evaluations) == players

    winners: list[Hand] = evaluations[0:split_pot]
    loosers: list[Hand] = evaluations[split_pot:]
    
    return (winners,loosers)


if __name__ == "__main__":
    analyze()
    
    
    
        
    