"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    return 0 if len(hand)==0 \
            else max([_num*hand.count(_num) for \
                      _num in set(hand)])
        
    

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    _rolls = gen_all_sequences(range(1, num_die_sides+1), num_free_dice)
    return sum([score(held_dice + _roll) for _roll in _rolls]) / float(len(_rolls))
 
    


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    def gen_all_hold_recur(hand,_len):
        """
        The recursion function to 
        generate all possible choices of dice from hand to hold.
        hand: full yahtzee hand
        _len: length of list hand 
        
        Returns a set of tuples, where each tuple is dice to hold

        """
        if _len == 0:
            return set([()])
        
        _drop = hand[0]
        _hand = gen_all_hold_recur(hand[1:],_len-1)
        _set = set([()])
        for _item in _hand:
            _store = list(_item)
            _store.append(_drop)
            _set.add(tuple(sorted(_store)))
        _set.update(_hand)
        return _set
            
    
    return gen_all_hold_recur(hand,len(hand))
    
    

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    _rolls = gen_all_holds(hand)
    _max = 0
    _set_hold = ()
    #_expect_value = sum([score(hand+_roll) for _roll in _rolls]) / float(len(_rolls))
    for _item in _rolls:
        _value = expected_value(_item,num_die_sides,len(hand)-len(_item))
        if _max < _value:
            _max = _value
            _set_hold = _item
    return (_max,_set_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
#s =  ()
#print gen_all_sequences(range(2),2)
#import user35_oGFuhcPNLh_0 as score_testsuite
#score_testsuite.run_suite(score)
#import user35_uLOFnLQSJV29rFh_5 as expected_value_testsuite
#expected_value_testsuite.run_suite(expected_value)    
#print gen_all_holds((1,))    
#print gen_all_holds((1,2,3))      
#import user35_mGREPnDxbs_0 as strategy_testsuite
#strategy_testsuite.run_suite(strategy)
