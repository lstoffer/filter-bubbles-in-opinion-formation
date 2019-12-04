import random as r

#   _____ _                          _____                      _              _ _ _   
#  / ____| |                        |  __ \                    | |            | (_) |  
# | |    | | __ _ ___ ___   ______  | |  | | ___    _ __   ___ | |_    ___  __| |_| |_ 
# | |    | |/ _` / __/ __| |______| | |  | |/ _ \  | '_ \ / _ \| __|  / _ \/ _` | | __|
# | |____| | (_| \__ \__ \          | |__| | (_) | | | | | (_) | |_  |  __/ (_| | | |_ 
#  \_____|_|\__,_|___/___/          |_____/ \___/  |_| |_|\___/ \__|  \___|\__,_|_|\__|

class Vertex:
    def __init__(self, number, opinion, confidence, p_follow, p_unfollow, max_follow, trust_stability):
        self.number = number
        self.opinion = opinion
        self.confidence = confidence
        self.p_follow = p_follow
        self.p_unfollow = p_unfollow
        self.max_follow = max_follow # maximum number of vertices it can add to following in one timestep
        self.trust_stability = trust_stability
        self.following = [] # list of agents this vertex follows
        self.trust = {} # maps for all following from v.number to "trust in v"-value
    
    def update_opinion(self):
        if len(self.following) == 0:
           return
        other_opinions = 0.0
        for v in self.following:
            other_opinions += self.trust[v.number] * v.opinion
        self.opinion = self.opinion*self.confidence + (1.0-self.confidence)*other_opinions
    
    def update_following(self, vertices):
        # unfollow
        for v in self.following:
            # unfollow with probability p_unfollow
            if r.random() < self.p_unfollow(self.trust[v.number]):
                self.following.remove(v)
                del self.trust[v.number]
        
        # follow
        num_followed = 0
        # go through all vertices in a random order
        random_indices = [i for i in range(len(vertices))]
        r.shuffle(random_indices)
        for v in [vertices[i] for i in random_indices]:
            num_following = len(self.following)
            if num_followed >= self.max_follow: break
            # follow with probability p_follow
            if v not in self.following and \
                r.random() < self.p_follow(abs(self.opinion - v.opinion)):
                self.following.append(v)
                self.trust[v.number] = 1.0 / max(num_following, 1.0)
                num_followed += 1
    
    def update_trust(self):
        trust_sum = 0.0
        for v in self.following:
            self.trust[v.number] += (1.0-self.trust_stability)*(v.confidence - abs(self.opinion - v.opinion))
            trust_sum += self.trust[v.number]
        # normalize
        for v in self.following:
            self.trust[v.number] /= trust_sum
