from gym.envs.registration import register


register(
    id='joinemio-v0',
    entry_point='gym_joinemio.envs:ConnectFourEnv',
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )