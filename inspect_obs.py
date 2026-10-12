import footsiesgym
import numpy as np
from footsiesgym.footsies.encoder import FootsiesEncoder

env = footsiesgym.make(
    platform="mac",
    launch_binaries=False,
    config={"port": 50051, "headless": False},
)

try:
    obs, _ = env.reset()
    encoder = FootsiesEncoder()
    state = env.last_game_state

    def player_features(player):
        raw = getattr(state, "player1" if player == "p1" else "player2")
        return encoder.encode_player_state(
            raw,
            env.prev_selected_actions[player],
            env._holding_special_charge[player],
            env.num_actions,
        )

    own = player_features("p1")
    opponent = player_features("p2")

    fields = [("distance", np.array([obs["p1"][0]]))]
    fields += [(f"self.{k}", np.atleast_1d(v)) for k, v in own.items()]
    fields += [
        (f"opponent.{k}", np.atleast_1d(v))
        for k, v in opponent.items()
        if k not in encoder.privileged_feature_names
    ]

    start = 0
    for name, value in fields:
        end = start + value.size
        print(f"obs['p1'][{start}:{end}]  {name}")
        start = end

    assert start == 88
finally:
    env.close()
