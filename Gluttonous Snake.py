# 开发者：李哎呦的蓝盆友
# 设备：HUAWEI MATEBOOK 16S
# 亲爱的PYTHON玩家，请开始你的表演！
# 冒号别忘记打！！！
# the part of the imports
import turtle
import random
from functools import partial

# the part of the global variables
g_screen = None  # is the main area that the snack and monter exist
g_snake = None  # the snake turtle objec
g_monster = None  # the monster turtle object
g_snake_sz = 5  # an int that shows the length of the snake(not including the head)
g_intro = None  # the turtle object that shows the information of pauses
g_keypressed = None  # the variable that store the keyboard events
g_status = None  # the turtle object of the status column
g_countstop = 0  # the int variable to decide whether the turtle object is in a pause
g_time = 0  # the int that storing the total time that showed in the status column
g_counttime = 0  # an int that used to count the g_time
g_countflash = 0  # an int that record the time of the hidden of the foods
g_contact = 0  # an int that counts the contracts of the monster and the snack's bodies
g_contact_valid=True# a bool to chech if the we still need to count the contract
tmp_flash = None  # to count last time the index x, y position of the hidden food to help replace it
tmp_time = 26  # an int to store the time of the hidden and the first time will be an unique 26
flash_index = 0  # an int to store the index of the hidden food to helpp restore it
Food_List = []  # the list to store all the food turtle object
Stamp_List = []  # a list to store all the x,y position of existed stamp
Stamp_List2=[] # a list is used to check if the length of the snack is increasing

COLOR_BODY = ("blue", "black")  # to decide the color of the body
COLOR_HEAD = "red"  # to decide the color of the head
COLOR_MONSTER = "purple"  # to decide the color of the monster
FONT = ("Arial", 16, "normal")  # to decide the font,size of the words

# to store all the five keyboard events
KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
    "Up", "Down", "Left", "Right", "space"
# to store the corresponding heading after the keyboard events
HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


def configScreen():  # this function is to set up the UI and the relevent information
    s = turtle.Screen()
    s.tracer(0)  # disable auto screen refresh, 0=disable, 1=enable
    s.title("Welcome to Stephen's Snack Game")
    s.setup(500 + 120, 500 + 120 + 80)
    s.mode("standard")
    return s


def SetFood():  # this funtion is to set food in the screen randomly
    for i in range(5):  # there are 5 foods:1,2,3,4,5
        x = random.randint(-11, 11) * 20-5
        y = random.randint(-13, 8) * 20+5
        food = createTurtle(x, y)
        food.hideturtle()
        food.write(f"{i + 1}", font=('Arial', 15, 'normal'))  # to  make it visible
        Food_List.append(food)  # to append it into the food list one by one

def configurePlayArea():  # this function is to draw the area of the monster and the snack
    # to draw the border
    m = createTurtle(0, 0, "", "black")
    m.shapesize(25, 25, 5)
    m.goto(0, -40)  # to move it to the corresponding space

    # to draw the information column
    s = createTurtle(0, 0, "", "black")
    s.shapesize(4, 25, 5)
    s.goto(0, 250)  # to move it to the corresponding space

    # to print some information to let the player know how to play the game
    intro = createTurtle(-200, 150)
    intro.hideturtle()
    intro.write(
                "Click anywhere to start the game .....\n"
                "You can use the 4 arrow keys to move the snake\n "
                "Try to consume all the foods and avoid the monster\n"
                "Good luck!",
                font=("Arial", 16, "normal"))  # to write the information in the iintro

    # status is the object that are the words in the status column
    status = createTurtle(0, 0, "", "black")
    status.hideturtle()
    status.goto(-200, s.ycor())  # to move it to the corresponding space

    return intro, status


def createTurtle(x, y, color="red", border="black"):  # this function is to create the head turtle of the snack
    t = turtle.Turtle("square")
    t.color(border, color)  # to set the color
    t.up()
    t.goto(x, y)  # to move it to the corresponding space
    return t


def updateStatus():  # this function is to update the words  in the status column
    g_status.clear()  # to clean the former information
    g_status.write(f"Motion:{g_keypressed}    Time:{g_time}    Contract:{g_contact}",
                   font=('arial', 15, 'bold'))  # to show those informations in the status column
    g_screen.update()  # to update the new information


def timeout():  # this function is to set what to do when tab the space
    global g_countstop
    if g_countstop == 0:  # if the program was not in a pause
        g_intro.write("TIMEOUT! Space to continue .....",
                      font=("Arial", 26, "normal"))  # to show those informations in the status column
        g_countstop = 1  # to prepare for the next time
        return
    if g_countstop == 1:  # if the program is in a pause
        g_intro.clear()  # to clear the former information
        g_countstop = 0  # to prepare for the next time
        return


def setSnakeHeading(key):  # choose the direction of the way the snack is heading due to the keyboard input
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading(HEADING_BY_KEY[key])


def onArrowKeyPressed(key):  # to handle what to do when receive a keyboard click
    global g_keypressed,g_countstop
    if key == "space":  # if click the space
        timeout()
        return
    g_keypressed = key  # if click other 4 directions
    g_countstop=0# to cancel it if there is a pause
    setSnakeHeading(key)
    updateStatus()


def checkborder():  # this function is to check if the snack touches the border
    global g_countstop
    x = g_snake.xcor()
    y = g_snake.ycor()  # to get the x, y position of the snake
    if (g_snake.heading() == 0 and x >= 239) or (g_snake.heading() == 90 and y >= 199) or (
            g_snake.heading() == 180 and x <= -239) or (
            g_snake.heading() == 270 and y <= -279):  # if it touches the border
        g_intro.write("You touched the border, please choose another way", font=('arial', 15, 'bold'))
        return False
    else:  # else if it doesn't touch the border
        g_intro.clear()
        return True


def touch():  # this function is to check if the snack's head touches its body
    global g_intro, g_snake_sz, g_contact
    direction = g_snake.heading()  # direction is to store the direction of the heading

    if len(Stamp_List) >= 5:
        for i in range(len(Stamp_List) - 1, len(Stamp_List) - 1 - g_snake_sz, -1):
            if (direction == 90 and (
                    0 < Stamp_List[i][1] - g_snake.ycor() <= 21 and abs(Stamp_List[i][0] - g_snake.xcor()) < 1)) or (
                    direction == 180 and -21 < Stamp_List[i][0] - g_snake.xcor() <= 0 and abs(
                Stamp_List[i][1] - g_snake.ycor()) < 1) or (
                    direction == 270 and -21 < Stamp_List[i][1] - g_snake.ycor() <= 0 and abs(
                Stamp_List[i][0] - g_snake.xcor()) < 1) or (
                    direction == 0 and 0 < Stamp_List[i][0] - g_snake.xcor() <= 21 and abs(
                Stamp_List[i][1] - g_snake.ycor()) < 1):  # to check if the head's heading will reach the snake's bodies
                g_intro.write("the snake touched its body,please choose another way!",
                              font=("Arial", 16, "normal"))  # if so print some information and pause the game
                return False
            else:
                g_intro.clear()  # else, go on and clear the former information
    return True


def onTimerSnake():  # if there is no keyboard input, run the function every 0.2s, also the main body of the program
    global g_countstop, g_counttime, g_time, g_contact, g_snake_sz, g_countflash, Food_List, tmp_flash, tmp_time, flash_index,g_contact_valid
    g_counttime += 1  # to count the time of the time
    g_countflash += 1  # to coount the time of the flash

    if g_counttime == 5:  # if the time reaches 1 sec, update the status column and return to 0
        g_time += 1
        g_counttime = 0
        g_status.clear()
        g_status.write(f"Motion:{g_keypressed}    Time:{g_time}    Contract:{g_contact}", font=('arial', 15, 'bold'))

    if g_countflash == tmp_time:  # if the time of the flash reaches its setting, choose another food and time to hide
        if tmp_time == 26:  # for the first time
            flash_index = random.randint(0, 4)
        if tmp_flash != None:  # to replce the hidden food in the last time
            Food_List[tmp_flash[0]].goto(tmp_flash[1], tmp_flash[2])
            Food_List[tmp_flash[0]].write(f"{flash_index + 1}", font=('Arial', 15, 'normal'))
        # to choose a new food to hide
        flash_index = random.randint(0, 4)
        tmp_flash = (flash_index, Food_List[flash_index].xcor(), Food_List[flash_index].ycor())
        Food_List[flash_index].goto(1000, 1000)  # to remove it from the area
        Food_List[flash_index].clear()
        tmp_time = random.randint(5, 25)
        g_countflash = 0  # start to count the time again

    s_x, s_y = g_snake.xcor(), g_snake.ycor()  # to record the x,y position of the snake
    m_x, m_y = g_monster.xcor(), g_monster.ycor()  # to record the x,y position of the monster
    # if monster touched the head
    if (s_x - m_x) ** 2 + (s_y - m_y) ** 2 <= 200:  # if the snake's head reaches the monster
        g_countstop = 1
        g_contact_valid = False  # stop counting contact
        g_screen.textinput("the game is gone", "you lost the game")
        turtle.bye()
    for i in Food_List:
        if (i.xcor() + 5 - s_x) ** 2 + (i.ycor() + 12 - s_y) ** 2 <= 200:  # if the snake reaches the food
            i.hideturtle()  # remove the food
            i.clear()
            g_snake_sz = g_snake_sz + Food_List.index(i) + 1  # to enlarge the size of the snake
            temp = turtle.Turtle()  # place a new turtle object to replace the existence of the snake
            temp.penup()
            temp.goto(1000, 1000)
            Food_List[Food_List.index(i)] = temp
            if g_snake_sz == 20:  # if the snake has atte all the foods
                g_monster.hideturtle()
                g_screen.textinput("the game is gone",
                                   "Congratulations, you won the game!!")  # print some information to congratulate the player
                g_monster.penup()
                g_monster.goto(1000, 1000)
                g_countstop = 1  # pause the game
                g_screen.bye()

    if g_countstop == 0 and checkborder() == True and touch() == True:  # if the snake is in a valid motion
        if g_keypressed == None:
            g_screen.ontimer(onTimerSnake, 200)
            return

        # Clone the head as body
        Stamp_List.append((g_snake.xcor(), g_snake.ycor()))
        Stamp_List2.append((g_snake.xcor(), g_snake.ycor()))
        g_snake.color(*COLOR_BODY)
        g_snake.stamp()
        g_snake.color(COLOR_HEAD)

        # Advance snake
        g_snake.forward(20)

        # Shifting or extending the tail.
        # Remove the last square on Shifting.
        if len(g_snake.stampItems) > g_snake_sz:  # stop cloning when the real length of the snake reaches g_snake_sz
            g_snake.clearstamps(1)  # to cancel the first stamp
            Stamp_List2.pop(0)
        # to calculate the tome of the contract
        g_screen.update()  # to update the screen
    # to change the speed of the snake with its length increasing
    speed = 200
    if len(Stamp_List2)<g_snake_sz :
        speed=speed+200
    g_screen.ontimer(onTimerSnake, speed)


def onTimerMonster():  # to set the motion of the monster
    global g_countstop, g_contact
    direction = 0
    s_x, s_y = g_snake.xcor(), g_snake.ycor()  # to record the x,y position of the snake
    m_x, m_y = g_monster.xcor(), g_monster.ycor()  # to record the x,y position of the monster
    # to make the monster always follows the head of the snake
    if abs(s_x - m_x) <= abs(s_y - m_y):  # the monster should walk alone the y direction
        if s_y - m_y > 0:  # the monster should walk upwards
            direction = 90
        else:  # the monster should walk downwards
            direction = 270
    else:  # the monster  should walk along the x asix
        if s_x - m_x > 0:  # the monster should walk to the right
            direction = 0
        else:  # the monster should walk to the left
            direction = 180
    g_monster.setheading(direction)  # to use that direction
    g_monster.forward(20)  # to walk a step forward
    if len(Stamp_List) > 5:
        count_contract()

    g_screen.update()
    speed = random.randint(100, 800)  # to set a random speed
    g_screen.ontimer(onTimerMonster, speed)

def count_contract():#this function is to count the numbert of ghe contract
    global Stamp_List, g_contact,g_monster,g_intro,g_contact_valid
    m_x=g_monster.xcor()
    m_y=g_monster.ycor()
    if g_contact_valid==True:# counting contact onlyy when the game is noot gone
        for i in range(len(Stamp_List) - 1, len(Stamp_List) - 1 - g_snake_sz, -1):
            if (m_x-Stamp_List[i][0])**2+(m_y-Stamp_List[i][1])**2<=201:
                g_contact+=1
                g_status.clear()
                g_status.write(f"Motion:{g_keypressed}    Time:{g_time}    Contract:{g_contact}",
                           font=('arial', 15, 'bold'))
                break

def startGame(x, y):
    # to reject the mouseclick event and to clear the intro
    g_screen.onscreenclick(None)
    g_intro.clear()

    g_screen.onkey(partial(onArrowKeyPressed, KEY_UP), KEY_UP)  # if the keyboard input is up
    g_screen.onkey(partial(onArrowKeyPressed, KEY_DOWN), KEY_DOWN)  # if the keyboard input is down
    g_screen.onkey(partial(onArrowKeyPressed, KEY_LEFT), KEY_LEFT)  # if the keyboard input is left
    g_screen.onkey(partial(onArrowKeyPressed, KEY_RIGHT), KEY_RIGHT)  # if the keyboard input is right
    g_screen.onkey(partial(onArrowKeyPressed, KEY_SPACE), KEY_SPACE)  # if the keyboard input is blank

    g_screen.ontimer(onTimerSnake, 200)  # to run the snake
    g_screen.ontimer(onTimerMonster, 800)  # to run the monster

def set_random_monster():#this function is to set a random place of the monster
    a=random.randint(1,4)
    x=0
    y=0
    if a==1:
        x,y=random.randint(-130,-100),random.randint(-130,-100)
    if a==2:
        x,y=random.randint(-130,-100),random.randint(100,130)
    if a==3:
        x,y=random.randint(100,130),random.randint(-130,-100)
    if a==4:
        x,y=random.randint(100,130),random.randint(100,130)
    return x,y

if __name__ == "__main__":
    g_screen = configScreen()  # to set the screem
    g_intro, g_status = configurePlayArea()
    updateStatus()
    (x,y)=set_random_monster()
    g_monster = createTurtle(x,y, "purple", "black")  # to set the snake turtle object
    g_snake = createTurtle(0, 0, "red", "black")  # to set the monster turtle object
    SetFood()  # to place the foods
    g_screen.onscreenclick(startGame)  # click to start the game
    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
