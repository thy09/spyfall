#! encoding=utf-8

# Creation Date: 2017-10-20 09:42:05
# Created By: Heyi Tang

import json
import random
class SpyFall:
    def __init__(self, fname):
        data = json.load(open(fname))
        self.names = data.get("names",{})
        self.roles = {}
        for name in self.names.keys():
            roles = data.get("roles",{}).get(name,[])
            if len(roles) < 2:
                self.names.pop(name)
                continue
            self.roles[name] = roles
        self.scenes = []
        for key,val in self.names.items():
            self.scenes.append("%s:%s" % (key, val))
        self.games = {}
        if len(self.roles) < 3:
            print "Error Handle"
            return

    def gen_id(self):
        upper = 1000000
        lower = 1000
        id = random.randint(lower, upper)
        while str(id) in self.games:
            id = random.randint(lower, upper)
        return id

    def create(self, player_count, upper, lower = 0):
        game = {}
        game["upper"] = upper
        game["lower"] = lower
        game["spy_count"] = random.randint(lower, upper)
        game["count"] = player_count
        loc = random.choice(self.roles.keys())
        game["loc"] = "%s:%s" % (loc, self.names[loc])
        players = [u"Spy:间谍"] * game["spy_count"]
        remain = player_count - game["spy_count"]
        roles = self.roles[loc]
        while remain >= len(roles):
            players += roles
            remain -= len(roles)
        if remain > 0:
            players += random.sample(roles, remain)
        random.shuffle(players)
        game["players"] = players
        game["roles"] = roles
        game["scenes"] = self.scenes
        game["id"] = self.gen_id()
        self.games[str(game["id"])] = game
        return game["id"]

    def game(self, id):
        return self.games.get(str(id))

    def print_game(self, id):
        game = self.games.get(str(id))
        for k,v in game.items():
            print k
            if k == "roles":
                for role in v:
                    print role
            elif k == "players":
                for i, player in enumerate(v):
                    print i, player
            else:
                print v

if __name__ == "__main__":
    spyfall = SpyFall("words.json")
    ids = [spyfall.create(5,1,1), spyfall.create(9,2), spyfall.create(15,3,1)]
    for id in ids:
        spyfall.print_game(id)
