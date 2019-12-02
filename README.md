# Filter Bubbles in Opinion Formation
> * Group Name: Bubble Trouble
> * Group participants' names: Adrian Hartmann, Beat Nairz, Luc Stoffer, Leo Widmer
> * Project Title: Filter Bubbles in Opinion Formation

## General Introduction

Filter bubbles are a phenomenon where a website proposes users content based on past behaviour and preference, which can result in an isolation of the user from different content. Notably on Social Media platforms, users can be grouped according to their (e.g. political) opinion, and be in contact only with users of the same or similar opinion. Such filter bubbles can have socio-political impacts, such as influencing election outcomes.

We aim to study in a simple dynamic model the parameters that can lead to the formation of filter bubbles.


## The Model

We consider a weighted directed network of vertices. Many social media platforms, such as Instagram and Twitter, implement a directed "follower" relationship.

A vertex has an opinion and a confidence. The opinion is variable and influenced by other connected vertices, the confidence determines how easily the vertex is influenced.

Updating of vertex connections: 
> - To implement filter bubbles, the probability of a vertex to form a connection to a different vertex should be dependent on their respective opinions. If the opinions are further apart, this probability should diminish. This is a simplification of a social media platform proposing only users to follow, who share common interests.
> - The probability of a vertex to sever a connection should be higher if the connection weight is small.
> - The weight of connections should increase if vertices have a similar opinion, and decrease, if their opinions are further apart. This is motivated by the fact that common interests tend to have the effect of strengthening a social bond.

Opinion evolution (similar to the approach in Hegselmann and Krause):
> - The opinion of a vertex should be influenced by the vertices it has a connection to.
> - The vertex should adhere to his opinion with his confidence, and change it with a certain susceptibility to the weighted mean of the vertices it has a connection to.


## Fundamental Questions

How do the parameters above influence the formation of filter bubbles?
> - What is the effect of different probabilities to form and sever a connection?
> - How does the vertex confidence change the result?

Are there critical opinion differences for which the opinion evolution behaviour changes qualitatively?
> - Can we "forcibly" impose filter bubbles?


## Expected Results

We expect that the probability to form a connection will have a large impact on filter bubble formation. If the probability falls rapidly with opinion-difference, it is unlikely that a vertex is influenced by vertices with a different opinion, and a bubble forms.

If the probability to sever a connection is small, a vertex might be influenced by vertices who's opinion is very different. This might reduce the forming of filter bubbles.

If the vertex confidence is higher, the opinion change is smaller, and the effect of other vertices' opinions diminishes.

We expect that we can artificially create filter bubbles if opinion differences are large enough.

As the model is similar to the one in Hegselmann and Krause, we expect that opinion bubbles converge to a single opinion after enough steps.


## References 

Hegselmann, R.; Krause, U., JASS 5, 3, 2002, Opinion Dynamics and Bounded Confidence

Laguna, M. F. et al. , Research Article, 2004, Minorities in a Model for Opinion Formation

Holme, P.; Newman, M., Nonequilibrium phase transition in the coevolution of networks and opinions, arXiv:physics/0603023v3


## Research Methods

Agent-based modeling with discrete uniform time steps.

