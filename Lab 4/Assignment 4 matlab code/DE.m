 path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
 addpath(genpath(path))

 
 functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved

 %example: functions = 10;
 %example: functions = [2 4 9];
 %functions=[3 5 10];
 numF = size(functions,2);
 nTimes = 1; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 100; % Adjust this to your algorithm
 pr=0.5; % probability of recombination
 F=0.5;
 
 for i = 1:numF

    fitfun = functions(i); %fitfun is the function that we are solving

    fprintf('\n-----  Function %d started  -----\n\n', fitfun);
    arraySol = zeros(1,nTimes); 
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
         while(objetiveValue < bestSolutionFitness && currentEval < maxEval)

              
              % Your algorithm goes here
              
              mutants=population;
              offspring=population;
              %mutation
              for indexElementToMutate=1:populationSize
                  individuals=randi([1,populationSize],3,1);
                  
                  mutants(indexElementToMutate,:)=population(individuals(1),:)+F*(population(individuals(2),:)-population(individuals(3),:));
              end
              
              % recombination
              % generar un random para cada j
               for z=1:populationSize
                   for j=1:dimension
                        randomValue=rand;

                        if(randomValue<pr)
                            offspring(z,j)=mutants(z,j);
                           
                        end      
                   end
               end
              
               %que los valores no sobrepasen el upper o lower
               offspringFitness = calculateFitnessPopulation_2005(fitfun, offspring, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
              
              % selection
              for z=1:populationSize
                    if offspringFitness(z)<populationFitness(z)
                        population(z,:)=offspring(z,:);
                        populationFitness(z)=offspringFitness(z);
                    end
               end
              
              % recalculate
              
%               populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
%             
%               bestSolutionFitness = min(populationFitness);
                 currentEval = currentEval + populationSize;
              
              % Your algorithm goes here
              
%               if bestSolutionFitness<globalFitness
%                   globalFitness=bestSolutionFitness;
%                   fprintf('Global fitness: %d, generation: %d \n', globalFitness,g);
%               end 
              g=g+1;
         end

         % best individual
         bestSolutionFitness = min(populationFitness);
         fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
          %fprintf('%d\n', bestSolutionFitness);
          arraySol(t) = bestSolutionFitness;
    end
    fprintf('%d\n', mean(arraySol));
end
