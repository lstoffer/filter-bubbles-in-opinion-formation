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
    
    def update_opinion(self, crit_confidence):
        if len(self.following) == 0:
           return
        #other opinions are only taken into account if confidence is smaller than some critical value
        if self.confidence<crit_confidence:
            other_opinions = 0.0
            for v in self.following:
                other_opinions += self.trust[v.number] * v.opinion
            self.opinion = self.opinion*self.confidence + (1.0-self.confidence)*other_opinions
    
    def update_following(self, vertices):
        num_followed = 0
        # go through all vertices in a random order
        random_indices = [i for i in range(len(vertices))]
        r.shuffle(random_indices)
        for v in [vertices[i] for i in random_indices]:
            num_following = len(self.following)
            if v in self.following:
                # unfollow with probability p_unfollow
                if r.random() < self.p_unfollow(self.trust[v.number]):
                    self.following.remove(v)
                    del self.trust[v.number]
                    v.num_followers -= 1
            elif num_followed < self.max_follow:
                # follow with probability p_follow
                if r.random() < self.p_follow(abs(self.opinion - v.opinion)):
                    self.following.append(v)
                    self.trust[v.number] = 1.0 / max(num_following, 1.0)
                    num_followed += 1
                    v.num_followers += 1
    
    def update_trust(self):
        trust_sum = 0.0
        for v in self.following:
            self.trust[v.number] += self.trust[v.number]*(v.confidence - abs(self.opinion - v.opinion))
            trust_sum += self.trust[v.number]
        # normalize
        for v in self.following:
            self.trust[v.number] /= trust_sum
    
    def update_confidence(self, n, t, T):
        follower_percent = self.num_followers/n
        time_percent = T/(t+1)
        if follower_percent >= 0.3:
            self.confidence += 0.01
        # else:
        #     self.confidence = 0.9*self.confidence + 0.1*(self.num_followers/n - self.opinion_differences())
        # # make sure that confidence stays between 0.0 and 1.0
        # self.confidence = min(max(self.confidence, 0.0), 1.0)
        else:
            if self.opinion_differences() > 0.07:
                self.confidence = 0.9*self.confidence + 0.1*(self.num_followers/n - self.opinion_differences())
            else:
                self.confidence = self.confidence + 0.1*(self.num_followers/n - self.opinion_differences())
    
    def opinion_differences(self):
        # returns weighted average of opinion differences between self and the ones it's following
        opinion_difference = 0.0
        for v in self.following:
            opinion_difference += self.trust[v.number] * abs(self.opinion - v.opinion)
        return opinion_difference
