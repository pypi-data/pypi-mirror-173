import gym
from gym import spaces
import pygame
import numpy as np
import math

class ModelSpinEnv(gym.Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    ori = np.array([1, 0, 0])

    def __init__(self, render_mode=None, initial_ori=ori):
        # 模型初始方向
        self.initial_ori = initial_ori
        self._agent_orientation = self.initial_ori

        # 这里说明每次旋转模型，模型绕某个轴旋转 pi/36 = 5°
        self.cos = math.cos(math.pi / 36)
        self.sin = math.sin(math.pi / 36)

        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, 1, shape=(2,), dtype=int),
            }
        )

        # we have 2 actions, spin with "x", "y"
        # 三维空间中只要绕x,y旋转就能遍历每一种情况
        self.action_space = spaces.Discrete(2)

        # 下面的是旋转矩阵 0: 绕"x" 1: 绕"y"
        self._action_to_direction = {
            0: np.array([[1, 0, 0],
                         [0, self.cos, -self.sin],
                         [0, self.sin, self.cos]]),
            1: np.array([[self.cos, 0, self.sin],
                         [0, 1, 0],
                         [-self.sin, 0, self.cos]])
        }

        # 暂定此模型效果最好的角度是[0, 0, 1]
        self._target_orientation = np.array([0, 0, 1])

    def _get_obs(self):
        # 这里会获得一个模型当前角度
        return self._agent_orientation

    def _get_info(self):
        # 暂时没什么info需要返回
        return 1

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._agent_orientation = self.initial_ori

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        spin = self._action_to_direction[action]
        self._agent_orientation.dot(spin)

        # 是否结束
        terminated = np.array_equal(self._agent_orientation, self._target_orientation)

        # 如果结束获得奖励，未结束的时候获得的奖励不能为0，应该为负，避免模型停在原地不动
        reward = -0.1 if terminated else 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info

    # 下面这些都是用pygame写的游戏需要的，暂时不动
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            return 1
        return 0

    def close(self):
        if self.window is not None:
            pass
        pass