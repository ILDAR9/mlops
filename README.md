# AWS DeepRacer Reward Function

## Observation
<img src="./imgs/agent_environment.png" alt="environment" width="210"
    style="background-color:white"/>

## Action Space

<img src="./imgs/action_space.png" alt="action space" width="300"
    style="background-color:white"/>

## Reward params
    {
        "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
        "x": float,                            # agent's x-coordinate in meters
        "y": float,                            # agent's y-coordinate in meters
        "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
        "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
        "distance_from_center": float,         # distance in meters from the track center 
        "crashed": Boolean,                    # Boolean flag to indicate whether the agent has crashed.
        "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
        "offtrack": Boolean,                   # Boolean flag to indicate whether the agent has gone off track.
        "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
        "heading": float,                      # agent's yaw in degrees
        "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_len.
        "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
        "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
        "objects_location": [(float, float),], # list of of object locations [(x,y), ...].
        "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
        "progress": float,                     # percentage of track completed
        "speed": float,                        # agent's speed in meters per second (m/s)
        "steering_angle": float,               # agent's steering angle in degrees
        "steps": int,                          # number steps completed
        "track_length": float,                 # track length in meters.
        "track_width": float,                  # width of the track
        "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center

    }

## Hyperparameter Values

<img src="./imgs/hyperparams_description.png" alt="hyperparameters" width="600"
    style="background-color:white"/>

| Hyperparameter (Default)                                       | Value |
|----------------------------------------------------------------|-------|
| Gradient Descent Batch Size                                    | 64    |
| Entropy                                                        | 0.01  |
| Discount Factor                                                | 0.999 |
| Loss Type                                                      | Huber |
| Learning Rate                                                  | 0.0003 or 0.001|
| No# Experience Episodes between each policy-updating iteration | 20    |
| No# of Epochs                                                  | 10    |
