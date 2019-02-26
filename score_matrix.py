import numpy as np

#penalties
match = 4
transition = -3
transversion = -4
gap = -2

#list of transitions and transversions possible
transition_list = [("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")]
transversion_list = [("A", "T"), ("A", "C"), ("C", "A"), ("C", "G"), ("T", "A"), ("T", "G"), ("G", "C"), ("G", "T")]

#sequences. seq2 should always be larger than seq1
seq1 = 'TGTTACGG'
seq2 = 'GGTTGACTA'

#scoring matrix size
rows = len(seq1) + 1
cols = len(seq2) + 1

def create_score_matrix(rows, cols):
    '''
    Create a matrix of scores representing trial alignments of the two sequences.
    Sequence alignment can be treated as a graph search problem. This function
    creates a graph (2D matrix) of scores, which are based on trial alignments
    of different base pairs. The path with the highest cummulative score is the
    best alignment.
    '''
    score_matrix = [[0 for col in range(cols)] for row in range(rows)]
    # Fill the scoring matrix.
    max_score = 0
    max_pos   = None    # The row and column of the highest score in matrix.
    for i in range(1, rows):
        for j in range(1, cols):
            score = calc_score(score_matrix, i, j)
            if score > max_score:
                max_score = score
                max_pos   = (i, j)
            score_matrix[i][j] = score
    assert max_pos is not None, 'the x, y position with the highest score was not found'
    return score_matrix, max_pos

def calc_score(matrix, x, y):
    if seq1[x-1] == seq2[y-1]:
        score = match
    elif (seq1[x-1], seq2[y-1]) in transition_list:
        score = transition
    elif (seq1[x-1], seq2[y-1]) in transversion_list:
        score = transversion    
    diag_score = matrix[x - 1][y - 1] + score
    up_score   = matrix[x - 1][y] + gap
    left_score = matrix[x][y - 1] + gap
    return max(0, diag_score, up_score, left_score)


def print_matrix(matrix):
    '''
    Print the scoring matrix.
    ex:
    0   0   0   0   0   0
    0   2   1   2   1   2
    0   1   1   1   1   1
    0   0   3   2   3   2
    0   2   2   5   4   5
    0   1   4   4   7   6
    '''
    print(np.matrix(matrix).T)

def path(score_matrix, start_pos, final_path):
    row,col = start_pos[0], start_pos[1]
    surrounds = [(row-1, col), (row-1, col-1), (row, col-1)]
    if score_matrix[row][col] == 0:
        final_path.append(start_pos)
    else:
        checks = {}
        for item in surrounds:
            checks[score_matrix[item[0]][item[1]]] = item
        next_pos = max(checks)
        final_path.append(start_pos)
        return path(score_matrix, checks[next_pos], final_path)

def print_path(score_matrix, start_pos):
    final_path = []
    path(score_matrix, start_pos, final_path)
    for item in final_path[::-1][:-1]:
        print ("c" + str(item[0]) + ",r" + str(item[1]) + " -> ", end = "")
    print ("c" + str(final_path[0][0]) + ",r" + str(final_path[0][1]))
    return final_path

def print_alignment(matrix, path):
    seq_1 = "seq1:\t"
    seq_2 = "\nseq2:\t"
    matches = "\n\t"
    path = path[::-1]
    checks_c = []
    checks_r = []
    for item in path:
        if matrix[item[0]][item[1]] == 0:
            if item[0] == 0:
                seq_1 += " "*(item[1]-1)
                seq_2 += " "*item[0]
                checks_r.append(item[1]-2)
            else:
                seq_1 += " "*item[1]
                seq_2 += " "*(item[0]-1)
                checks_c.append(item[0]-2)
        else:
            checks_c.append(item[0]-1)
            checks_r.append(item[1]-1)
    for num in range(len(checks_c)):
        if checks_c[num] == checks_c[num-1]:
            seq_1 += "-"
        else:
            seq_1 += seq1[checks_c[num]]
    for num in range(len(checks_r)):
        if checks_r[num] == checks_r[num-1]:
            seq_2 += "-"
        else:
            seq_2 += seq2[checks_r[num]]
    for num in range(len(seq_1)):
        if num > 5:
            if seq_1[num] == seq_2[num+1]:
                matches += "*"
            else:
                matches += " "
    print (seq_1, seq_2, matches)
    
if __name__ == '__main__':
    #my main
    score_matrix, start_pos = create_score_matrix(rows, cols)
    print_matrix(score_matrix)
    final_path = print_path(score_matrix, start_pos)
    print_alignment(score_matrix, final_path)
