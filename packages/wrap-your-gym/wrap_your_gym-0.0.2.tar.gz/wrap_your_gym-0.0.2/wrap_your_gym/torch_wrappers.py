import gym
import numpy as np
import torch


class ObsPyTorchWrapper(gym.ObservationWrapper):
    def observation(self, observation):
        return torch.from_numpy(np.ascontiguousarray(observation))


class ActionToNumpyWrapper(gym.ActionWrapper):
    def action(self, action):
        return action.detach().numpy()

    def reverse_action(self, action):
        return torch.from_numpy(action)
