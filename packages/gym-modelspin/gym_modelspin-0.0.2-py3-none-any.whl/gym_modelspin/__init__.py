from gym.envs.registration import register

# 旋转一次是5°，绕x旋转一周需要360/5=72步，所以最多72*72步可以遍历完每个面
register(
    id='modelspin-v0',
    entry_point='gym_modelspin.envs.mzy:ModelSpinEnv',
)
