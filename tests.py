from bowling import (Player, Bowling, Frame,
        lets_bowl)

# Unit tests for Bowling Game

# bowler tests
class PlayerTest():
    player = Player("Stan")
    illegal = Frame([7,7], 1)
    strike = Frame([10], 1)    
    spare = Frame([7,3], 1)    
    normal = Frame([2,4], 2)    

    def test_init(self):
        assert self.player.name == "Stan"
        assert self.player.score == []
    
    def test_frame_error(self):
        try:
            self.player.bowl_frame(self.illegal) 
        except ValueError as e:
            pass    
        assert e is not None

    def test_score_strike(self):
        self.player.score[1] = self.strike
        self.player.score[2] = self.normal
        assert self.player.score_strike(self.strike) == 16
        
    def test_score_two_strikes(self):
        second_strike = Frame([10], 2)
        self.player.score[1] = self.strike
        self.player.score[2] = second_strike
        self.normal.number = 3
        self.player.score[3] = self.normal
        assert self.player.score_strike(self.strike) == 22

    def test_ninth_frame_strike(self):
        a_strike = Frame([10], 9)
        self.normal.number = 10
        self.player.score[9] = a_strike
        self.player.score[10] = self.normal
        
        assert self.player.score_strike(a_strike) == 16

    def test_score_spare(self):
        self.player.score[1] = self.spare
        self.player.score[2] = self.strike
        assert self.player.score_spare(self.spare) == 20
        self.player.score[2] = self.normal
        assert self.player.score_spare(self.spare) == 12

    def test_perfect_game(self):
        for i in xrange(9):
            self.player.score[i] = Frame([10], i)
        self.player.score[9] = Frame([10,10,10], 9)
        assert self.player.total_score(10) == 300

    def test_worst_game(self):
        for i in xrange(10):
            self.player.score[i] = Frame([0,0], i)
        assert self.player.total_score(10) == 0

    def test_average_game(self):
        # verifed using an online caluclator
        # http://bowlinggenius.com/
        self.player.score[0] = Frame([9,0], 0)
        self.player.score[1] = Frame([4,0], 1)
        self.player.score[2] = Frame([6,4], 2)
        self.player.score[3] = Frame([8,0], 3)
        self.player.score[4] = Frame([9,1], 4)
        self.player.score[5] = Frame([4,6], 5)
        self.player.score[6] = Frame([3,0], 6)
        self.player.score[7] = Frame([7,0], 7)
        self.player.score[8] = Frame([7,0], 8)
        self.player.score[9] = Frame([10,4,2], 9)
        assert self.player.total_score(10) == 99

class FrameTest():
    strike = Frame([10], 1)    
    spare = Frame([7,3], 1)    
    normal = Frame([2,4], 1)    
    illegal = Frame([7,7], 1)

    def test_strike(self):
        assert self.strike.strike()
        assert not self.strike.spare()
        assert not self.spare.strike()

    def test_spare(self):
        assert not self.spare.strike()
        assert not self.strike.spare()
        assert self.spare.spare()
        
    def test_normal(self):
        assert self.normal.score == 6
        assert self.normal.num_rolls == 2
        
    def test_invalid(self):
        last = Frame([10,10,10], 9)
        assert last.is_valid()
        last = Frame([8,2,10], 9)
        assert last.is_valid()
        last = Frame([8,5,10], 9)
        assert not last.is_valid()
        last = Frame([8,1,10], 9)
        assert not last.is_valid()
        last = Frame([10,1,10], 9)
        assert not last.is_valid()
        last = Frame([4,10,10], 9)
        assert not last.is_valid()
        last = Frame([0,10,10], 9)
        assert last.is_valid()
        last = Frame([5,6], 3)
        assert not last.is_valid()
        last = Frame([0,0], 3)
        assert last.is_valid()
        last = Frame([5,5], 3)
        assert last.is_valid()


# bowling tests
class BowlingTest():
    player = Player("Stan")
    game = Bowling([player])
    
    def test_init(self):
        assert self.game.frames == 10
        assert self.game.players[0] == self.player
    

# run tests:
BowlingTest().test_init()
PlayerTest().test_perfect_game()
PlayerTest().test_average_game()
PlayerTest().test_worst_game()
PlayerTest().test_score_spare()
PlayerTest().test_score_strike()
PlayerTest().test_score_two_strikes()
PlayerTest().test_ninth_frame_strike()
FrameTest().test_strike()
FrameTest().test_spare()
FrameTest().test_normal()
FrameTest().test_invalid()

# run the game
lets_bowl()
