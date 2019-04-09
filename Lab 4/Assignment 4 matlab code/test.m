 path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
 addpath(genpath(path))

 %
 functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
 %example: functions = 2;
 %example: functions = [2 4 9];
 numF = size(functions,2);
 nTimes = 20; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 40; % Adjust this to your algorithm

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

              selectOneForBest = find(populationFitness==bestSolutionFitness);
              bestParentIndex = selectOneForBest(1);
              [out,idx]=sort(populationFitness);
              val=out(2);
              selectOneForSecondBest=idx(2);
              secondBestParentIndex=selectOneForSecondBest(1);
               
              
              % Crossover 
              for z=1:populationSize
                  if (z ~= bestParentIndex) && (z~=secondBestParentIndex)
                    startIndex =int8( 1 + (dimension-2).*rand); 
                    finishIndex =int8( startIndex + (dimension-startIndex).*rand);
                    aux = population(bestParentIndex,startIndex:finishIndex);
                    crossover = population(secondBestParentIndex,:);
                    counter=1;
                    for s=startIndex:finishIndex
                        crossover(s)=aux(counter);
                        counter=counter+1;
                    end
                    population(z,:) = crossover;
                  end
              end
              
              %mutation
              
              indexElementToMutate=int8(bestParentIndex); 
              while(indexElementToMutate == bestParentIndex || indexElementToMutate==secondBestParentIndex)
                  indexElementToMutate=int8(1 + (populationSize-1) .* rand);
              end
              random_index1 = int8( 1 + (dimension-1) .* rand);
              random_index2 = int8(1 + (dimension-1) .* rand);
              aux=population(indexElementToMutate,random_index2);
              population(indexElementToMutate,random_index2)=population(indexElementToMutate,random_index1);
              population(indexElementToMutate,random_index1)=aux;
             
              
              % recalculate
              
              populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
              bestSolutionFitness = min(populationFitness);
              currentEval = currentEval + populationSize;
              % Your algorithm goes here
              
         end

         % best individual
         bestSolutionFitness = min(populationFitness);
         fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);

     end

end
