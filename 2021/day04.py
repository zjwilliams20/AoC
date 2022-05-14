#!/usr/bin/env python
# day04.py

import numpy as np

with open("./input/day04", 'r') as file:
    callouts = [int(n) for n in file.readline().split(',')]
    boards = []
    board = []
    for line in file.readlines()[1:]:
        if len(line) == 1:
            boards.append(board.copy())
            board = []
            continue
        board.append([int(n) for n in line.strip().split()])

boards.append(board)
boards = np.array(boards)

# Part 1
def find_winner(boards, mask):
    """Determine whether and who won."""
    sums = np.hstack([np.sum(mask, axis=1), np.sum(mask, axis=2)])
    is_winner = np.any(sums == 5)
    n_boards = boards.shape[0]

    if is_winner:
        win_inds = np.argwhere(sums == 5)
        i_win = np.unique(win_inds[:,0])
        return [np.sum(boards[i][~mask[i]]) for i in i_win], i_win
    return None, None


call_mask = np.zeros(boards.shape, dtype=bool)
for call in callouts:
    call_mask |= boards == call
    sum_uncalled, _ = find_winner(boards, call_mask)
    if sum_uncalled is not None:
        score = sum_uncalled[0] * call
        break

print(f'Part 1: {score}')

# Part 2
last_ind = None
n_boards = boards.shape[0]
call_mask = np.zeros(boards.shape, dtype=bool)
win_mask = np.zeros((n_boards), dtype=bool)
for call in callouts:
    call_mask |= boards == call
    
    sum_uncalled, i_win = find_winner(boards, call_mask)
    if sum_uncalled is not None:
        score = sum_uncalled * call
        win_mask[i_win] = True
    
    n_winners = np.count_nonzero(win_mask)
    if n_winners == n_boards-1:
        last_ind = np.argwhere(~win_mask)

    if last_ind is not None and n_winners == n_boards:
        match_ind = np.argwhere(i_win == last_ind)
        last_score = sum_uncalled[match_ind[0,1]] * call
        break

print(f'Part 2: {last_score}')

