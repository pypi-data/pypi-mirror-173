import logging

import gym
import numpy as np


class ObsDict(gym.ObservationWrapper):
    """
    Wraps the observation in the given key.
    Allows to easily convert from single observation environments to a dict based environment for further processing.
    e.g. from [[....]] to {"image": [
    """

    def __init__(self, env: gym.Env, key: str):
        if isinstance(env.observation_space, gym.spaces.Dict):
            logging.warning(
                "Found environment space of type Dict to be wrapped again in Dict. Are you sure about that?"
                "If not, remove ObsDictWrapper."
            )
        super().__init__(env)
        self.key = key
        self.observation_space = gym.spaces.Dict({key: env.observation_space})

    def observation(self, obs):
        return {self.key: obs}


class ActionDict(gym.ActionWrapper):
    """
    Wraps the action in the given key.
    Allows to easily convert from single action environments to a dict based environment for further processing.
    e.g. from [....] to {"action": [...]}
    """

    def __init__(self, env: gym.Env, key: str = "action"):
        if isinstance(env.action_space, gym.spaces.Dict):
            logging.warning(
                "Found environment space of type Dict to be wrapped again in Dict. Are you sure about that?"
                "If not, remove ObsDictWrapper."
            )
        super().__init__(env)
        self.key = key
        self.action_space = gym.spaces.Dict({key: env.action_space})

    def action(self, action):
        return action[self.key]

    def reverse_action(self, action):
        return {self.key: action}


class RewardInObs(gym.Wrapper):
    """
    Allows to add the reward as key in the dict observations.
    By default, adds the reward as 'reward' into the dict.

    Does not work when the observation spae is another type besides Dict.
    """

    def __init__(self, env: gym.Env, key='reward'):
        super().__init__(env)
        assert isinstance(
            env.observation_space, gym.spaces.Dict
        ), "Reward can only be added in Dict obs spaces"
        assert (
            key not in env.observation_space
        ), f"Cannot add reward as {key}. {key} already found in space."
        self._key = key
        reward_space = gym.spaces.Box(-np.inf, np.inf, (), dtype=np.float32)
        self.observation_space = gym.spaces.Dict(
            {
                **env.observation_space.spaces,
                self._key: reward_space,
            }
        )

    def step(self, action):
        obs, reward, *others = self.env.step(action)
        return ({**obs, self._key: reward}, reward, *others)

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        return {**obs, self._key: 0.0}, info


class ResetInObs(gym.Wrapper):
    def __init__(self, env, key='reset'):
        super().__init__(env)
        assert isinstance(
            env.observation_space, gym.spaces.Dict
        ), "Reset can only be added in Dict obs spaces"
        assert (
            key not in env.observation_space
        ), f"Cannot add reset as {key}. {key} already found in space."
        self._key = key
        self.observation_space = gym.spaces.Dict(
            {
                **self.env.observation_space,
                self._key: gym.spaces.Box(0, 1, (), dtype=np.bool),
            }
        )

    def step(self, action):
        obs, *others = self.env.step(action)
        return ({**obs, self._key: np.array(False, np.bool)}, *others)

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        return {**obs, self._key: np.array(True, np.bool)}, info
