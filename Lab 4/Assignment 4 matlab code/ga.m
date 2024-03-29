 path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
 addpath(genpath(path))

 %
 functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
 %example: functions = 1;
 %example: functions = [4 5 6 7 8 9 10];
 numF = size(functions,2);
 nTimes = 20; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 150; % Adjust this to your algorithm
 delta = 0.12;
 pM = 0.14;
 alphaVariable = 0.45; %0.1; %ajustar un poco el alpha, aumentarlo

 %el fitness no sirve para la selecci�n
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
               keepIndividuals=int16(populationSize/10);
               selectOneForSecondBest=idx(2);
               secondBestParentIndex=selectOneForSecondBest(1);
             
               probabilityOfSelection = zeros(1,populationSize);

               for z=keepIndividuals:populationSize
                 probabilityOfSelection(z) = populationFitness(idx(z))/sum(populationFitness);
               end
               

              % Crossover 
             
              for z=keepIndividuals:populationSize
                   
                     % roulette wheel corregir para que escoja entre rangos
                     % no toda la suma
                     
                     
                        pRoulette=rand;
                        element=0;
                        e=1;
                        while element<pRoulette && e<=populationSize
                            aux=element+probabilityOfSelection(e);
%                              element=aux;
%                              e=e+1;
                             if aux<pRoulette
                                 element=aux;
                                 e=e+1;
                             else
                                 break;
                             end
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
                         while p==e
                             p=idx(randi([1,keepIndividuals],1,1));
                         end
                        
                     for r=1:dimension 
                         IMax = max(population(p,r),population(e,r));
                         IMin = min(population(p,r),population(e,r));
                         I= IMax-IMin;
                         randomV = (IMin-I*alphaVariable)+((IMax+I*alphaVariable)-(IMin-I*alphaVariable)).*rand;
                         population(idx(z),r)=randomV;
                         if randomV > upper
                                population(idx(z),r) = upper;
                         elseif randomV < lower
                                population(idx(z),r) = lower;   
                         end
                         
                         
                     end
                    
              end
              
              %no mutar los padres y no sustituir sino mejoran
              
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
              %-keepIndividuals; % a cambiar por los que cambio no por toda la poblaci�n
              % Your algorithm goes here
              
%                 if bestSolutionFitness<globalFitness
%                      globalFitness=bestSolutionFitness;
%                      fprintf('Global fitness: %d, generation: %d \n', globalFitness,g);
%                 end 
%                g=g+1;
                 
         end

         % best individual
         bestSolutionFitness = min(populationFitness);
         fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
          %fprintf('%d\n', bestSolutionFitness);
          arraySol(t) = bestSolutionFitness;
    end
    fprintf('%d\n', mean(arraySol));
end
