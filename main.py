# import torch
try:
    import oatomobile
    import oatomobile.baselines.torch
    import oatomobile.baselines.rulebased
except ImportError as e:
    print("oatomobile import error, ", e.msg)
    exit(1)

# Initializes a CARLA environment.
environment = oatomobile.envs.CARLAEnv(town="Town01")

# Makes an initial observation.
observation = environment.reset()
done = False

# Rule-based agents.
agent = oatomobile.baselines.rulebased.AutopilotAgent(environment)

while not done:
    # Selects a random action.
    action = agent.act(observation)
    observation, reward, done, info = environment.step(action)

    # Renders interactive display.
    environment.render(mode="human")

# Book-keeping: closes
environment.close()
