 %path = 'C:\Users\mlz02\Documents\MATLAB\DE LIBRARY';
 %addpath(genpath(path))

 functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
 %example: functions = 1;
 %example: functions = [2 4 9];
 numF = size(functions,2);
 nTimes = 20; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 10; % Adjust this to your algorithm
 Vmax=1;
 cognitive = 0.01;
 social = 0.2;
 
 
 for i = 1:numF

    fitfun = functions(i); %fitfun is the function that we are solving

    fprintf('\n-----  Function %d started  -----\n\n', fitfun);

    for t = 1:nTimes

         maxEval = 10000*dimension; % maximum number of evaluation
         [value, upper,lower,objetiveValue, o, A, M, a, alpha, b] = getInformation_2005(fitfun, dimension);

         currentEval = 0;

         % Start generating the initial population

         population = zeros(populationSize, dimension);

         for j =1:populationSize

             population(j,:) = lower + (upper-lower).*rand(1,dimension);

         end

         populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
         bestSolutionFitness = min(populationFitness);
         currentEval = currentEval + populationSize;

         % Algorithm loop
         g=1;
         globalFitness=bestSolutionFitness;
         
          VX=zeros(populationSize);
              pBest=zeros(populationSize);
              vGradient=zeros(populationSize,2);
              xFitness=0;
              
              for z=1:populationSize
                index=randi([1,populationSize]);
                VX(z) = population(index);
                V=gradient(VX,randi([-Vmax, Vmax]));
                pBest(z)=populationFitness(index);
              end
         while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
                       
              % Your algorithm goes here
              %initialize particles
              
           
              
              %movement of particles
              for z=1:populationSize
                VX(z) = VX(z)+V(z);
               
              end
              
              pBest = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b);
              [pBestFitness,gid] = min(populationFitness);
              
              %Adjust Velocity
              V= V + cognitive*rand().*(pBest-VX) +social*rand().*(gid-VX);
              
              %Position adjustment
              VX=VX+V;
              
              pBest = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
              populationFitness=pBest;
              bestSolutionFitness = min(populationFitness);
              currentEval = currentEval + populationSize;
              
              % Your algorithm goes here
              
               
              
                if bestSolutionFitness<globalFitness
                     globalFitness=bestSolutionFitness;
                     fprintf('Global fitness: %d, generation: %d \n', globalFitness,g);
                end 
                g=g+1;
         end

         % best individual
         bestSolutionFitness = min(populationFitness);
         fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);

     end

end
