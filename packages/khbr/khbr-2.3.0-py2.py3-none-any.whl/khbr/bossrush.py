import time
#from gooey import Gooey, GooeyParser
import argparse
from khbr.KH2.KingdomHearts2 import KingdomHearts2
import random

supported_games = ["kh2"]

#@Gooey(program_name="Kingdom Hearts Boss Rush")
def main_ui():
    main()

class BossRush:
    def __init__(self, game):
        if game not in supported_games:
            raise Exception("Game not supported")
        self.game = self._get_game(game)
    def get_preset_routes(self):
        return {
            "Disney": ["Past Pete", "Pete OC II"],
            "Super Bosses": ["Data Marluxia", "Sephiroth", "Terra"],
        }
    def generate_route(self, x):
        # Todo there are things like shenzie + ed as different bosses or tifa (1) and tifa (2) to work out
        possible_bosses = self.game.get_valid_bosses()
        print(possible_bosses)
        if len(possible_bosses) < x:
            raise Exception("length is too long") # TODO you could make it reuse bosses but not super simple
        random.shuffle(possible_bosses)
        return possible_bosses[:x]
    def _get_game(self, game):
        if game == "kh2":
            return KingdomHearts2()
    def generate_mod(self, route, setboss=None):
        print("Creating route: \n\t{}".format("\n\t".join(route)))

def main(cli_args: list = []):
    #parser = GooeyParser()
    parser = argparse.ArgumentParser()
    
    main_options = parser.add_argument_group(
        "Main options",
        "main options"
    )

    generator = BossRush(game="kh2")

    main_options.add_argument("-route", choices=generator.get_preset_routes(), help="Which preset route to use")

    main_options.add_argument("-nrandom", help="If nonzero, generates a random route of N bosses")
    main_options.add_argument("-replace", help="(DEBUG) if nonempty, the same boss will be present at every location in the route")

    main_options.add_argument("-seed", help="Seed to use")

    # Parse and print the results
    if cli_args:
        args = parser.parse_args(cli_args)
    else:
        args = parser.parse_args()

    seed = args.seed or time.time()
    print("Using seed {}".format(seed))
    random.seed(seed)

    nrandom = int(args.nrandom)
    route = generator.generate_route(nrandom) if nrandom > 0 else args.route

    generator.generate_mod(route=route, setboss=args.replace)



'''
Program 0x34
Party NO_FRIEND
Bgm Default Default
AreaSettings 0 -1
	SetProgressFlag 0x816
	SetEvent "400" Type 66
	SetJump Type 2 World TT Area 0 Entrance 0 LocalSet 56 FadeType 16386
	SetPartyMenu 0

Change the progress flag to idk 0xFFF to make it so you can use stuff on newgame
remove the SetEvent to make it jump you right away

Interesting, if you go right to AX2 and Die, when you respawn your back at the AX2 fight. Hmmmmmmmmm how?


this jump will just skip to cutscenes that skip right to final credits (maybe due to wrong progress flags being set?)

This jump goes to the credits
SetJump Type 2 World ES Area 0 Entrance 0 LocalSet 69 FadeType 1

you can find the end program to modify the jump by checking the spawns for a boss, then outputting the MSN and the program number


this is actually the jump that shows battle report
SetJump Type 5 World ES Area 0 Entrance 0 LocalSet 0 FadeType 16385

"0x84A" is the flag that sets abilities


So the simplest POC
pick between X preset routes, or a random route of X bosses
(it randomly gives you X stuff)
it sets the ard scripts so the jumps are appropriate (don't forget the 1 for setjump type, so that retry puts you back in the same fight, )
boss levels need to be all set to 50
msns need to be modified to not give anything and retry back in same fight

it would be nice to make some hidden features that make testing boss rando easier

Then add stuff like a daily seed, a draft mode (aka import)
'''

if __name__ == "__main__":
    import sys
    if "cmd" in sys.argv:
        main()
    else:
        main_ui()
