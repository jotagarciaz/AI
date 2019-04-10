 path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
 addpath(genpath(path))

 
 functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
 %example: functions = 10;
 %example: functions = [2 4 9];
 %functions=[3 5 10];
 numF = size(functions,2);
 nTimes = 20; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 700; % Adjust this to your algorithm
 pr=0.8; % probability of recombination
 F=1.25;
 
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

         while(objetiveValue < bestSolutionFitness && currentEval < maxEval)

              
              % Your algorithm goes here
              
              mutants=population;
              offspring=population;
              %mutation
              for indexElementToMutate=1:populationSize
                  individual1 = int8( 1 + (populationSize-1).* rand);
                  individual2=int8(1+(populationSize-1).*rand);
                  individual3=int8(1+(populationSize-1).*rand);
                  
                  while (individual1 == individual2 || individual1 == individual3 || individual2==individual3)
                    individual1 = int8( 1 + (populationSize-1).* rand);
                    individual2=int8(1+(populationSize-1).*rand);
                    individual3=int8(1+(populationSize-1).*rand);
                  end
                  
                  
                  aux=population(individual1)+F*(population(individual2)-population(individual3));
                  mutants(indexElementToMutate)=aux;
              end
              
              % recombination
               for z=1:populationSize
                    randomValue=rand;
                    if(randomValue<pr)
                        offspring(z)=mutants(z);
                    end
               end
              
               offspringFitness = calculateFitnessPopulation_2005(fitfun, offspring, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
              
              % selection
              for z=1:populationSize
                    if offspringFitness(z)<populationFitness(z)
                        population(z)=offspring(z);
                    end
               end
              
              % recalculate
              
              populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            
              bestSolutionFitness = min(populationFitness);
              currentEval = currentEval + populationSize;
              % Your algorithm goes here
              
         end

         % best individual
         bestSolutionFitness = min(populationFitness);
         %fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
          fprintf('%d\n', bestSolutionFitness);
     end

end
