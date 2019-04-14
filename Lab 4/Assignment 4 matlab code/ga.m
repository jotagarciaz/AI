 path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
 addpath(genpath(path))

 %functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
 %example: functions = 1;
 %example: 
 functions = [4 5 6 7 8 9 10];
 numF = size(functions,2);
 nTimes = 20; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 20; % Adjust this to your algorithm
 delta = 0.15;
 pM = 0.1;
 alphaVariable = 0.25; %0.1;

 %el fitness no sirve para la selección
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

               selectOneForBest = find(populationFitness==bestSolutionFitness);
               bestParentIndex = selectOneForBest(1);
               [~,idx]=sort(populationFitness);
               keepIndividuals=int8(populationSize/4);
               selectOneForSecondBest=idx(2);
               secondBestParentIndex=selectOneForSecondBest(1);
             
               probabilityOfSelection = zeros(1,populationSize);

               for z=keepIndividuals:populationSize
                 probabilityOfSelection(z) = populationFitness(idx(z))/sum(populationFitness);
               end
              % Crossover 
             
              for z=keepIndividuals:populationSize
                   
                     % roulette wheel
                     
                     
                        pRoulette=rand;
                        element=0;
                        e=1;
                        while element<pRoulette && e<=populationSize
                            element=element+probabilityOfSelection(e);
                            e=e+1;
                        end
                        e=e-1;
                
%                      pRoulette=rand;
%                      element=0;
%                      e2=1;
%                      while element<pRoulette || e2<=populationSize
%                          element=element+probabilityOfSelection(e2);
%                          e2=e2+1;
%                      end
%                      e2=e2-1;
                        p=idx(randi([1,keepIndividuals],1,1));
                     for r=1:dimension
                         IMax = max(population(p,r),population(e,r));
                         IMin = min(population(p,r),population(e,r));
                         I= IMax-IMin;
                         randomV = (IMin-I*alphaVariable)+((IMax+I*alphaVariable)-(IMin-I*alphaVariable)).*rand;
                         population(idx(z),r)=randomV;
                         
                     end
                    
              end
              
              %mutation
              for z=keepIndividuals:populationSize
                  randomP = rand;
                  if randomP < pM
                      if z ~= bestParentIndex && z ~= secondBestParentIndex
                          for r=1:dimension
                              population(idx(z),r) = population(idx(z),r) + sqrt(delta)*randn(1);
                          end
                      end
                  end
              end
%               indexElementToMutate=int8(bestParentIndex); 
%               while(indexElementToMutate == bestParentIndex ||  indexElementToMutate==secondBestParentIndex)
%                   indexElementToMutate=int8(1 + (populationSize-1) .* rand);
%               end
%               random_index1 = int8( 1 + (dimension-1) .* rand);
%               random_index2 = int8(1 + (dimension-1) .* rand);
%               aux=population(indexElementToMutate,random_index2);
%               population(indexElementToMutate,random_index2)=population(indexElementToMutate,random_index1);
%               population(indexElementToMutate,random_index1)=aux;
%              
              
              % recalculate
              if bestSolutionFitness<populationFitness 
                  fprintf('new best fitness%d\n', bestSolutionFitness);
              end
              
              populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
              bestSolutionFitness = min(populationFitness);
              currentEval = currentEval + populationSize;
              % Your algorithm goes here
              
%                if bestSolutionFitness<globalFitness
%                     globalFitness=bestSolutionFitness;
%                     fprintf('Global fitness: %d, generation: %d \n', globalFitness,g);
%                end 
%               g=g+1;
%                
         end

         % best individual
         bestSolutionFitness = min(populationFitness);
         fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
          %fprintf('%d\n', bestSolutionFitness);
          arraySol(t) = bestSolutionFitness;
    end
    fprintf('%d\n', mean(arraySol));
end
