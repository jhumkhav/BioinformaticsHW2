import numpy as np

#penalty box
match    = 3
mismatch = -3
gap      = -2

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
    max_pos   = None    # The row and columbn of the highest score in matrix.
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
    #Calculate score for a given x, y position in the scoring matrix.
    #The score is based on the up, left, and upper-left diagnol neighbors
    similarity = match if seq1[x - 1] == seq2[y - 1] else mismatch
    diag_score = matrix[x - 1][y - 1] + similarity
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

#add your function(s) to find a solution here.
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
        print ("r" + str(item[0]) + ",c" + str(item[1]) + " -> ", end = "")
    print ("r" + str(final_path[0][0]) + ",c" + str(final_path[0][1]))
#end of your function(s)

if __name__ == '__main__':
    #my main
    score_matrix, start_pos = create_score_matrix(rows, cols)
    print_path(score_matrix, start_pos)
