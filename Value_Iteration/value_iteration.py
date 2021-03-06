import gym
import numpy as np
import pandas as pd
from gym import wrappers
from gym import spaces, utils
from gym.envs.toy_text import discrete

def value_iterate(env):
	tot_iterations = 10000
	gamma = 1
	no_states = env.observation_space.n
	no_actions = env.action_space.n
	v = np.zeros(no_states)
	for i in range(tot_iterations):
		pre_v = np.copy(v)
		error_epsilon = 1e-30
		for s in range(env.nS):
			qval = [sum([reward + prob*gamma*pre_v[st] for prob, st, reward, _ in env.P[s][a]]) for a in range(env.nA)] 		
			v[s] = max(qval)		
		error = np.sum(np.fabs(v - pre_v))
		if(error<= error_epsilon):
			print "Value Function has converged"
			break
	return v

def findpolicy(env, optv):
	policy = np.zeros(env.nS)
	gamma = 1	
	for s in range(env.nS):
		qval = [sum([reward + prob*gamma*optv[st] for prob, st, reward, _ in env.P[s][a]]) for a in range(env.nA)] 		
		policy[s] = np.argmax(qval) 		
	return policy   


def run_policy(env, optimal_policy, render=False):
	state = env.reset()
	final_reward = 0
	index = 0 
	gamma = 1
	while True:
		if render:
			env.render()
		state, reward, done, ext = env.step(optimal_policy[state])
		final_reward += ((gamma**index)*reward)
		index += 1
		if done:
			break
	return final_reward		



def policy_evaluate(env, optimal_policy):
	scores = [run_policy(env, optimal_policy, render = False) for i in range(200)]
	return np.mean(scores)


if __name__ == '__main__':
    env = gym.make('Taxi-v1')
    print env.nS
    optimal_value_function = value_iterate(env)
    optimal_policy = findpolicy(env, optimal_value_function)
    score = policy_evaluate(env, optimal_policy)
    print score