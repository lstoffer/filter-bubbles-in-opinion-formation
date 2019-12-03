%%%% Unterschiede zu Python Code: %%%%
%    -kein max_follow
%    -keine zufällige ordnung der follows
%%%%

%%% Variables %%%
n = 100; % number of vertices (individuals)
T = 100; % number of timesteps

% less filter bubbles for bf -> 0 and bu -> infinity
bu = 20;
bf = 30;

p_follow = @(opinion_distance) exp(-bf*opinion_distance);
p_unfollow = @(trust) exp(-bu*trust);
trust_stability = 0.99;
confidence_mean = 0.9;
confidence_std = 0.1;

%%% Initialize Model Data %%%

vertices = zeros(2,n);
%Labels for rows
OPINION = 1;
CONFIDENCE = 2;
%initialize
distribution = truncate(makedist('normal','mu',0.9,'sigma',0.1),0,1);
vertices(CONFIDENCE,:) = random(distribution,1,n);
vertices(OPINION,:) = rand(1,n);
%Adajcency Matrix for trust/following (trust zero implies not followed)
%          To    
%      --------->
%     |
% From|
%     |
%     v
following = zeros(n,n); %ones(n,n)*1/n;

%Opinion change results:
results = zeros(T,n);

%%%%%%%%%%%%%%%%%%
%%% Simulation %%%
%%%%%%%%%%%%%%%%%%

debug = 0;
for i=1:T
   %Output for runtime
   if ~mod(i,5)
       fprintf('Time elapsed: %i \n',i);    
   end
   results(i,:) = vertices(OPINION,:); 
   %%% update Opinion %%%
   
   
   %same as pyhton code
   other_opinions = following * vertices(OPINION,:)';
   for j = 1:n
        if other_opinions(j) ~= 0
            vertices(OPINION,j) = vertices(OPINION,j)*vertices(CONFIDENCE,j)+ ...
                (1-vertices(CONFIDENCE,j))*other_opinions(j);
        end
   end
   
   %%% update following  %%%
   
   
   probability = rand(n,n);
   %unfollow:
   %remove unfollowed entries
   following = following .* (probability > p_unfollow(following));
   %Mask
   non_following = (following == 0);
   %
   opinion_diff = abs(repmat(vertices(OPINION,:),n,1)-vertices(OPINION,:)');
   %add new followed entries
   following = following + 1./max(1,sum(~non_following,2)).*non_following.* ...
       (probability < p_follow(opinion_diff));
   
   
   %%% trust update %%%
   %Mask for all following entries
   are_following = (following ~= 0);
   %
   opinion_diff = abs(repmat(vertices(OPINION,:),n,1)-vertices(OPINION,:)');
   %update trust-values
   following = following + (1.0-trust_stability)*( repmat(vertices(CONFIDENCE,:),n,1) - opinion_diff);
   %kick out non-followed guys stuff
   following = following .* ~diag(ones(1,n)) .*are_following;
   %normalize rows
   following = following ./ max(0.01,sum(following,2));
   
   
end

t = 1:T;
plot(t,results)
