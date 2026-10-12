import time

import footsiesgym

env = footsiesgym.make(
    platform="mac",
    launch_binaries=False,
    config={"port": 50051, "headless": False},
)

'''
All observations defined here:
https://github.com/como-research/FootsiesGym/blob/main/footsiesgym/footsies/encoder.py

All actions defined here:
https://github.com/como-research/FootsiesGym/blob/main/footsiesgym/footsies/game/constants.py

0	NONE	不输入
1	BACK	后退
2	FORWARD	前进
3	ATTACK	攻击
4	BACK_ATTACK	后退 + 攻击
5	FORWARD_ATTACK	前进 + 攻击

'''

try:
    obs, _ = env.reset()

    print("Observation shape:", obs["p1"].shape)
    print("Action space:", env.action_space("p1"))

    for step in range(300):
        distance = obs["p1"][0]
        action = 2 if distance > 0.2 else 3

        obs, rewards, terminated, truncated, infos = env.step({
            "p1": action,
            "p2": 0,
        })

        if step % 5 == 0:
            distance = obs["p1"][0]
            print(
                f"Step {step}: distance={distance:.3f}, reward={rewards['p1']}")

        if any(terminated.values()) or any(truncated.values()):
            break

        time.sleep(0.05)
finally:
    env.close()
