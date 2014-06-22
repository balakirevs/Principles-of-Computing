
"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import poc_clicker_provided as provided
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._ttl_cookies = 0.0
        self._current_cookies = 0.0
        self._current_t = 0.0
        self._current_cps = 1.0
        self._item_name = None
        self._item_cost = 0.0
        self._history_lst = [(self._current_t, self._item_name, self._item_cost, self._ttl_cookies)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "\n" + "TotalCookies:" + str(self._ttl_cookies) + "\n"\
    + "CurrentCookies:" + str(self._current_cookies) + "\n"\
    + "CurrentTime:" + str(self._current_t) + "\n"\
    + "CurrentCPS:" + str(self._current_cps) + "\n"
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_name(self):
        """
        Return current upgrade item name
        
        Should return None or a string
        """
        return self._item_name
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_t
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history_lst

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > 0 and cookies >= self._current_cookies:
            return math.ceil((cookies-self._current_cookies)/self._current_cps)
        else:
            return 0.0
        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_t += time
            self._current_cookies += self._current_cps * time
            self._ttl_cookies += self._current_cps * time
        else:
            pass
    
    def buy_item(self, _item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._item_name = _item_name
            self._item_cost = cost
            self._current_cookies -= cost
            self._current_cps += additional_cps
            his_tuple = (self._current_t, self._item_name, self._item_cost, self._ttl_cookies)
            self._history_lst.append(his_tuple)
        else:
            pass
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    upgrade = build_info.clone()
    action = ClickerState()

    while action.get_time() <= duration:
        t_left = duration - action.get_time()
        item_name = action.get_name()
        item_name = strategy(action.get_cookies(), action.get_cps(), t_left, upgrade)
        if item_name == None:
            break
        if action.time_until(upgrade.get_cost(item_name)) > t_left:
            break 
        else:
            item_name = strategy(action.get_cookies(), action.get_cps(), t_left, upgrade)
            action.wait(action.time_until(upgrade.get_cost(item_name)))
            action.buy_item(item_name, upgrade.get_cost(item_name), upgrade.get_cps(item_name))
            upgrade.update_item(item_name)
    
    action.wait(t_left)
    return action


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always return the cheapest item to upgrade

    """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)
    cheap_idx = cost_lst.index(min(cost_lst))
    cheap_item = item_lst[cheap_idx]
    if (cookies + cps * time_left) < cost_lst[cheap_idx]:
        return None
    else:
        return cheap_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always return the most expensive item to upgrade

    """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)
    temp_lst_item = []
    temp_lst_cost = []
    for dummy_i in range(len(cost_lst)):
        if cost_lst[dummy_i] <= cookies + (cps * time_left):
            temp_lst_cost.append(cost_lst[dummy_i])
            temp_lst_item.append(item_lst[dummy_i])
    if temp_lst_cost == []:
        return None
    else:
        expensive_idx = temp_lst_cost.index(max(temp_lst_cost))
        expensive_item = temp_lst_item[expensive_idx]
        return expensive_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    Always return the most efficient item to upgrade
    aka greatest cps/cost

    """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)
    cps_lst = map(build_info.get_cps, item_lst)
    eff_lst = []
    for dummy_i in range(len(item_lst)):
        efficiency = cps_lst[dummy_i] / cost_lst[dummy_i]
        eff_lst.append(efficiency)
    most_eff_idx = eff_lst.index(max(eff_lst))
    most_eff_item = item_lst[most_eff_idx] 
    return most_eff_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    #run_strategy("None", SIM_TIME, strategy_none)

run()
