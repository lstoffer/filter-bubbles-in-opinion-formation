import random as r

class Vertex:
    def __init__(self, number, opinion, confidence, p_follow, p_unfollow, max_follow):
        self.number = number
        self.opinion = opinion
        self.confidence = confidence
        self.p_follow = p_follow
        self.p_unfollow = p_unfollow
        self.max_follow = max_follow # maximum number of vertices it can add to following in one timestep
        self.num_followers = 0
        self.following = [] # list of individuals this vertex follows
        self.trust = {} # maps for all following from v.number to "trust in v"-value
        
    def follow(self, v):
        self.following.append(v)
        self.trust[v.number] = 1.0 - 0.5*(self.opinion - v.opinion)**2
        v.num_followers += 1
        
    def unfollow(self, v):
        self.following.remove(v)
        del self.trust[v.number]
        v.num_followers -= 1
    
    def update_opinion(self):
        if len(self.following) == 0:
           return
        other_opinions = 0.0
        for v in self.following:
            other_opinions += self.trust[v.number] * v.opinion
        self.opinion = self.opinion*self.confidence + (1.0-self.confidence)*other_opinions
    
    def update_following(self, vertices):
        num_followed = 0
        # go through all vertices in a random order
        random_indices = [i for i in range(len(vertices))]
        r.shuffle(random_indices)
        k = len(self.following)
        for v in [vertices[i] for i in random_indices]:
            num_following = len(self.following)
            if v in self.following:
                # unfollow with probability p_unfollow
                if r.random() < self.p_unfollow(self.trust[v.number]*k):
                    self.unfollow(v)
                    
            elif num_followed < self.max_follow:
                # follow with probability p_follow
                if r.random() < self.p_follow(abs(self.opinion - v.opinion)):
                    self.follow(v)
                    num_followed += 1
    
    def update_trust(self):
        trust_sum = 0.0
        for v in self.following:
            self.trust[v.number] += self.trust[v.number]*(v.confidence - abs(self.opinion - v.opinion))
            #self.trust[v.number] = 0.5*(v.confidence+1)*(self.trust[v.number] + (1. - abs(self.opinion - v.opinion)))
            trust_sum += self.trust[v.number]
        # normalize
        for v in self.following:
            self.trust[v.number] /= trust_sum
    
    def update_confidence(self, n):
        #self.confidence = 0.9*self.confidence + 0.1*(self.num_followers/n - self.opinion_differences())
        # make sure that confidence stays between 0.0 and 1.0
        
        #self.confidence = min(max(self.confidence, 0.0), 1.0)
        
        self.confidence = 0.2*max(1. - 2*self.opinion_differences() - 0.1*r.random(), 0)
    
    def opinion_differences(self):
        # returns weighted average of opinion differences between self and the ones it's following
        opinion_difference = 0.0
        for v in self.following:
            opinion_difference += self.trust[v.number] * abs(self.opinion - v.opinion)
        return opinion_difference
