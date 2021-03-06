from collections import deque,namedtuple
import random
import torch
import numpy as np

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

class ReplayBuffer:

    def __init__(self,buffer_size = 100000,batch_size = 64):
        self.memory = deque(maxlen = buffer_size)
        self.experience = namedtuple("Experience",field_names = ['state','action','reward','next_state','done'])
        self.batch_size = batch_size
    
    def add(self,experience):
        state,action,reward,next_state,done = experience
        e = self.experience(state,action,reward,next_state,done)
        self.memory.append(e)
    
    def sample(self):
        size = min(len(self.memory),self.batch_size)
        indices = random.choices(range(len(self.memory)),k = size)

        states = torch.from_numpy(np.vstack([self.memory[i].state for i in indices if self.memory[i] is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([self.memory[i].action for i in indices if self.memory[i] is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([self.memory[i].reward for i in indices if self.memory[i] is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([self.memory[i].next_state for i in indices if self.memory[i] is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([self.memory[i].done for i in indices if self.memory[i] is not None]).astype(np.uint8)).float().to(device)

        return (states,actions,rewards,next_states,dones)
    
    def __len__(self):
        return len(self.memory)