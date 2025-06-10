import turtle
# pip install turtle
import numpy as np
import yaml
import random
import time






# Set up the screen
screen = turtle.Screen()
screen.setup(700, 700)
screen.title("Q-Learning with Turtles")
screen.addshape("1.3 jerry.gif")
screen.addshape("1.5 tom.gif")


score_turtle = turtle.Turtle()
score_turtle.penup()
score_turtle.goto(-300, 400)
score_turtle.hideturtle()
# score = 0
# prey_score = 0 
# score_turtle.write(f"Tom score: {score}  Jerry score: {prey_score}" , font=("Arial",3,"bold"))


# Create the turtles
target_turtle = turtle.Turtle()
target_turtle.shapesize(2.5)
target_turtle.speed(1000)
target_turtle.shape("1.3 jerry.gif")
target_turtle.color("green")
target_turtle.penup()
target_turtle.goto(-325, -325)


target_turtle.pendown()
target_turtle.goto(-325, 325)
target_turtle.goto(325, 325)
target_turtle.goto(325, -325)
target_turtle.goto(-325, -325)

target_turtle.penup()
target_turtle.goto(300, 300)  # Set the target turtle's position

agent_turtle = turtle.Turtle()
agent_turtle.shapesize(2.5)
agent_turtle.shape("1.5 tom.gif")
agent_turtle.color("blue")
agent_turtle.penup()
agent_turtle.goto(-300, -300)  # Set the agent turtle's initial position
agent_turtle.speed(1000)

# Create the obstacle turtle
obstacles = [(0, 0), (50, 0), (100, 0), (0, 50), (0, 100), (-100, 0), (-50, -50), (-100, 250),
             (250, -200), (200, -200), (250, -150), (250, -50), (250, 0), (250, 100),
             (250, 250), (200, 250), (150, 250), (-200, -250), (-150, -250), (-200, -150),
             (-200, -100), (-250, -50), (-250, 0), (-250, 50), (-250, 150), (-250, 250)]
for obstacle in obstacles:
    obstacle_turtle = turtle.Turtle()
    obstacle_turtle.speed(1000)
    obstacle_turtle.shape("square")
    obstacle_turtle.shapesize(2.5)
    obstacle_turtle.color("blue")
    obstacle_turtle.penup()
    obstacle_turtle.goto(obstacle)  # Set the obstacle turtle's position

print((0, 0)in obstacles)
# Define the state space
states = []
for x in range(-300, 301, 50):
    for y in range(-300, 301, 50):
        states.append((x, y))

print(states)
goal_states =[]
for state in states:
    if state not in obstacles:
        goal_states.append(state)
print(len(goal_states))

# Define the action space
actions = ['up', 'down', 'left', 'right']





predator_table = {}
prey_table = {}

# with open('1.2 condition.yaml', 'r') as f:
#     predator_table = yaml.load(f, Loader=yaml.FullLoader)

# with open('1.4 prey.yaml', 'r') as f:
#     prey_table = yaml.load(f, Loader=yaml.FullLoader)



# # Define the hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

# Q-Learning algorithm
predator_state = (-300, -300)  # Start from the initial state
prey_state = (300, 300)
score= 0
prey_score= 0

for s in goal_states:
    # with open('condition.yaml', 'w') as f:
    #     yaml.dump(predator_table, f)
    
    # with open('prey.yaml', 'w') as f:
    #     yaml.dump(prey_table, f)

    print(s)
    for g_state in goal_states:
        # print(g_state)

        min_duration = 0
        min_duration_time = 0
        # print("Hello")
        while min_duration_time != 500:






            randomm = True
            show = True

            if not randomm:
                predator_state = s  # Start from the initial state
                prey_state = g_state

            if show:
                agent_turtle.goto(predator_state)
                score_turtle.clear()
                score_turtle.write(f"Tom's Score: {score}  Jerry's Score: {prey_score}", font=("Arial", 25, "bold"))
                agent_turtle.speed(5)
                target_turtle.speed(5)
                target_turtle.goto(prey_state)



            done = False



            start = time.time()

            step = 0
            while not done:
                step +=1

                # Train Prey
                x, y = predator_state
                goal_x, goal_y = prey_state
                condition = (x, y, goal_x, goal_y)
                if condition not in prey_table.keys():
                    prey_table[condition] = {action: 0 for action in actions}
                # print(prey_table[condition])
                # Choose an action using epsilon-greedy policy
                if np.random.uniform() < epsilon:
                    action = np.random.choice(actions)  # Explore
                else:
                    action = max(prey_table[condition], key=prey_table[condition].get)  # Exploit
                # print(action)
                # Get the next state
                goal_x, goal_y = prey_state
                if action == 'up':
                    next_state = (goal_x, goal_y + 50)
                elif action == 'down':
                    next_state = (goal_x, goal_y - 50)
                elif action == 'left':
                    next_state = (goal_x - 50, goal_y)
                else:  # 'right'
                    next_state = (goal_x + 50, goal_y)

                # Get the reward
                if next_state not in states:
                    next_state = prey_state
                    reward = -5  # Penalty for hitting the wall
                elif ((next_state[0]-predator_state[0])**2 + (next_state[1]-predator_state[1])**2)**(1/2) <= 5000**(1/2):  # This condition is good for tom but not jerry
                    reward = -10  # Reached the target turtle
                elif next_state in obstacles:
                    next_state = prey_state
                    reward = -5  # Hit the obstacle turtle
                else:
                    current_distance= ((prey_state[0]-predator_state[0])**2 + (prey_state[1]-predator_state[1])**2)**(1/2)  
                    next_distance = ((next_state[0]-predator_state[0])**2 + (next_state[1]-predator_state[1])**2)**(1/2)
                    reward = (next_distance - current_distance)/10 # if jerry get far away form tom reward will be postive not then it will ne negative

                x, y = predator_state
                goal_x, goal_y = next_state
                next_condition = (x, y, goal_x, goal_y)
                if next_condition not in prey_table.keys():
                    prey_table[next_condition] = {action: 0 for action in actions}

                # Update the Q-table 
                # Q formula Q(S,A) <- Q(S,A) + aplha (R + gamma* max(Q(S' , A') - Q(S,A)))
                prey_table[condition][action] += alpha * (
                        reward + gamma * max(prey_table[next_condition].values()) -
                        prey_table[condition][action])

                # Update the state and move the agent turtle
                prey_state = next_state
                if show:
                    target_turtle.goto(prey_state)


                #Train Predator
                x, y = predator_state
                goal_x, goal_y = prey_state
                condition = (x, y, goal_x, goal_y)
                if condition not in predator_table.keys():
                    predator_table[condition] = {action: 0 for action in actions}

                # Choose an action using epsilon-greedy policy
                if np.random.uniform() < epsilon:
                    action = np.random.choice(actions)  # Explore
                else:
                    action = max(predator_table[condition], key=predator_table[condition].get)  # Exploit

                # Get the next state
                x, y = predator_state
                if action == 'up':
                    next_state = (x, y + 50)
                elif action == 'down':
                    next_state = (x, y - 50)
                elif action == 'left':
                    next_state = (x - 50, y)
                else:  # 'right'
                    next_state = (x + 50, y)

                # Get the reward
                if next_state not in states:
                    next_state = predator_state
                    reward = -5 # Penalty for hitting the wall
                elif next_state == prey_state:
                    reward = 10 # Reached the target turtle
                elif next_state in obstacles:
                    next_state = predator_state
                    reward = -5  # Hit the obstacle turtle
                else:
                    reward = -1

                x, y = next_state
                goal_x, goal_y = prey_state
                next_condition = (x, y, goal_x, goal_y)
                if next_condition not in predator_table.keys():
                    predator_table[next_condition] = {action: 0 for action in actions}

                # Update the Q-table
                predator_table[condition][action] += alpha * (reward + gamma * max(predator_table[next_condition].values()) - predator_table[condition][action])

                # Update the state and move the agent turtle
                predator_state = next_state
                if show:
                    agent_turtle.goto(predator_state)








                if step == 70:
                    done = True

                    if randomm:
                        prey_state = random.choice(goal_states)
                    if show:
                        prey_score +=1
                        target_turtle.hideturtle()
                        target_turtle.goto(prey_state)
                        target_turtle.showturtle()
                # Check if the target turtle  is reached
                if ((prey_state[0]-predator_state[0])**2 + (prey_state[1]-predator_state[1])**2)**(1/2) <= 5000**(1/2): # distance between the jerry and tom

                    done = True

                    if randomm:
                        prey_state = random.choice(goal_states)
                    if show:
                        score += 1
                        target_turtle.hideturtle()
                        target_turtle.goto(prey_state)
                        target_turtle.showturtle()

            duration = time.time() - start

            if duration > min_duration:
                min_duration = duration
                min_duration_time = 0
            else:
                min_duration_time += 1




with open('condition.yaml', 'w') as f:
    yaml.dump(predator_table, f)
with open('prey.yaml', 'w') as f:
    yaml.dump(prey_table, f)



# Keep the screen open until it's closed manually
turtle.done()
