# single player game:
MAX_PINS = 10
MAX_FRAMES = 10


class Frame():
    def __init__(self, rolls, number):
        self.number = number  # frame number (0-9)
        self.rolls = rolls  # list of the two rolls for the frame
        self.num_rolls = len(rolls)
        self.score = sum(rolls)
        self.last_frame = (number == MAX_FRAMES - 1)

    def strike(self):
        if self.last_frame:
            return (self.rolls[0] == MAX_PINS)
        return (len(self.rolls) == 1 and self.score == MAX_PINS)

    def spare(self):
        if self.last_frame:
            return (self.rolls[0] + self.rolls[1] == MAX_PINS)
        return (len(self.rolls) == 2 and self.score == MAX_PINS)

    def get_next_frame(self):
        return self.number + 1

    def is_valid(self):
        for roll in self.rolls:
            if 0 < roll > MAX_PINS:
                return False
        
        if not self.last_frame:
            if self.strike() and len(self.rolls) > 1:
                return False

        if self.last_frame:
            if (self.rolls[0] != MAX_PINS and self.rolls[0] + self.rolls[1] != MAX_PINS) and len(self.rolls) > 2:
                return False
            if(self.rolls[0] == MAX_PINS):
                if(self.rolls[1] < MAX_PINS):
                    if self.rolls[1] + self.rolls[2] > MAX_PINS:
                        return False
        if not self.strike() and not self.spare() and self.rolls[0] + self.rolls[1] > MAX_PINS:
            return False
        return True


class Player():
    def __init__(self, name):
        self.name = name
        self.score = {}

    def bowl_frame(self, frame_number):
        print "-------Frame: " + str(frame_number + 1) + " -------"
        print "First bowl: "
        first_bowl = input()
        if frame_number == MAX_FRAMES - 1:
            print "Second bowl: "
            second_bowl = input()
            if first_bowl + second_bowl >= MAX_PINS:
                print "Bonus bowl: "
                bonus_bowl = input()
                frame = Frame([first_bowl, second_bowl, bonus_bowl], frame_number)
            else:
                frame = Frame([first_bowl, second_bowl], frame_number)
        elif first_bowl == MAX_PINS:
            frame = Frame([first_bowl], frame_number)
        else:
            print "Second bowl: "
            second_bowl = input()
            frame = Frame([first_bowl, second_bowl], frame_number)

        if not frame.is_valid():
            raise ValueError("Invalid Frame.")

        self.score[frame_number] = frame

    def total_score(self, frame_number):
        total_score = 0
        for frame_number in xrange(frame_number):
            frame = self.score[frame_number]
            frame_score = frame.score

            if frame.strike():
                frame_score = self.score_strike(frame)
            elif frame.spare():
                frame_score = self.score_spare(frame)

            total_score += frame_score
        return total_score

    def score_strike(self, frame):
        next_frame = self.score.get(frame.get_next_frame(), None)

        if not next_frame:
            return frame.score

        elif not next_frame.last_frame:
            score = frame.score + next_frame.score
            if next_frame.strike():
                return score + self.score[next_frame.get_next_frame()].rolls[0]
            return score

        elif next_frame.last_frame:
            return frame.score + next_frame.rolls[0] + next_frame.rolls[1]

    def score_spare(self, frame):
        next_frame = self.score.get(frame.get_next_frame(), None)

        if not next_frame:
            return frame.score
        return frame.score + next_frame.rolls[0]


class Bowling():
    def __init__(self, players):
        self.players = players
        self.frames = MAX_FRAMES

    def play_game(self):
        self.rules()
        for frame in xrange(self.frames):
            for player in self.players:
                print player.name + "'s turn!"
                try:
                    player.bowl_frame(frame)
                except ValueError:
                    print "Invalid input. One more chance to input correctly."
                    player.bowl_frame(frame)
        for player in self.players:
            print player.name + " scored " + str(player.total_score(self.frames))

    def rules(self):
        print "-------------------------------------------------------------------------"
        print "Welcome to Bowling! Here's how it works"
        print "When your player name comes up, enter the number of pins you hit per turn.\n"
        print "Example: if you hit 7 on your first turn and two on your second,"
        print "you would type 7, hit enter then 2 and hit enter again.\n"
        print "Strikes are when you hit all 10 pins on the first turn!"
        print "You get bonus points for doing something so spectacular!\n"
        print "Spares are when you hit all 10 pins by the end of the second turn!" 
        print "Not as cool as a strike, but still worth some bonus points!\n"
        print "Note: you can only hit up to 10 pins total in your two turns."
        print "-------------------------------------------------------------------------\n\n"


def get_players():
    print "Number of bowlers: "
    num_bowl = input()
    players = []
    for i in range(num_bowl):
        print "Enter name for Player number: " + str(i + 1)
        players.append(Player(raw_input()))
    return players


def lets_bowl():
    Bowling(get_players()).play_game()
