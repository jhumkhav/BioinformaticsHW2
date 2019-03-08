states = {'Rainy', 'Sunny'}
observations = {'happy', 'sad'}

start_prob = {'Rainy': 1/3, 'Sunny': 2/3}
transition_prob = {'Rainy': {'Rainy': 0.6,'Sunny': 0.4},'Sunny':{'Rainy': 0.2, 'Sunny':0.8}}
emission_prob = {'Rainy': {'happy': 0.4,'sad': 0.6},'Sunny':{'happy': 0.8, 'sad':0.2}}


def calculate (observed):
    overall_prob = 1
    overall_states = []
    count = 0
    
    for item in observed:
        count += 1
        sunny = 1
        rainy = 1
        
        if count == 1:
            sunny *= start_prob['Sunny']
            rainy *= start_prob['Rainy']
        else:
            sunny *= transition_prob[overall_states[(observed.index(item)-1)]]['Sunny']
            rainy *= transition_prob[overall_states[(observed.index(item)-1)]]['Rainy']

        sunny *= emission_prob['Sunny'][item]
        rainy *= emission_prob['Rainy'][item]

        overall_prob *= max(sunny, rainy)
        overall_states.append('Sunny' if sunny > rainy else 'Rainy')
        
    return overall_prob, overall_states
        
        

def print_states (observed):
    prob, states = calculate(observed)
    print ("The observations are: " + str(print_list(observed)))
    print ("The most likely states are: " + str(print_list(states)))
    print ("The probability of this order of states is: " + str(prob) + "\n")

def print_list (l):
    string = ''
    for item in l[::-1][:-1]:
        string += item + " -> "
    string += l[0]
    return string



if __name__ == "__main__":
    print_states(['happy','sad'])
    print_states(['happy', 'sad', 'happy'])
    print_states(['happy', 'happy', 'sad', 'sad', 'sad', 'happy'])
    print_states(['happy', 'sad', 'happy', 'sad', 'happy', 'sad', 'happy'])
