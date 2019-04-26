 path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
 addpath(genpath(path))

 %
 functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
 %example: functions = 1;
 %example: functions = [2 4 9];
 numF = size(functions,2);
 nTimes = 20; % Number of times in which a function is going to be solved
 dimension = 30; % Dimension of the problem
 populationSize = 200; % Adjust this to your algorithm
 Vmax=25;
 social = 1;
 cognitive = 0.0005;
 
 weight=-0.75;
 
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


         
         currentEval = currentEval + populationSize;
 
         % Algorithm loop
         generaciones=1;
         
         
              VX=population;
              pBest=VX; 
              pBest_fitness=calculateFitnessPopulation_2005(fitfun, pBest, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better);

              VV= -Vmax+(Vmax-(-Vmax)).*rand(populationSize,dimension);
              
          bestSolutionFitness=min(pBest_fitness);
          globalFitness=bestSolutionFitness; 
          
          
          g=VX(1,:);
         
             
         while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
                       
              % Your algorithm goes here
              %initialize particles
              
             
              %movement of particles
              
              for z=1:populationSize
                  for j=1:dimension
                    VV(z,j) = weight*VV(z,j) + social*(g(j)-VX(z,j))*rand +cognitive*(pBest(z,j)-VX(z,j))*rand;
                    if VV(z,j) >Vmax
                        VV(z,j)=Vmax;
                    elseif  VV(z,j) <(-Vmax)
                        VV(z,j)=-Vmax;
                    end
                  end
              end
              
              VX = VX+VV;
              
              for z=1:populationSize
                  for j=1:dimension
                      if VX(z,j)>upper
                          VX(z,j)=upper;
                      elseif VX(z,j)<lower
                          VX(z,j)=lower;
                      end
                  end
              end
              
              xFitness = calculateFitnessPopulation_2005(fitfun, VX, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)

             for z=1:populationSize
                     if xFitness(z)<pBest_fitness(z)
                         pBest_fitness(z)=xFitness(z);
                         if pBest_fitness(z)<bestSolutionFitness
                               g=VX(z,:);
                               
                         end
                     end
             end
    

             
              bestSolutionFitness=min(pBest_fitness);
      
              currentEval = currentEval + populationSize;
              
              if bestSolutionFitness<globalFitness
                  globalFitness=bestSolutionFitness;
              end
              % Your algorithm goes here
              
               
%                   if bestSolutionFitness<globalFitness
%                        globalFitness=bestSolutionFitness;
%                        fprintf('Global fitness: %d, generation: %d \n', globalFitness,generaciones);
%                   end 
                  generaciones=generaciones+1;
          end

         % best individual
         bestSolutionFitness = globalFitness;
         fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
         arraySol(t) = bestSolutionFitness;
    end
    fprintf('%d\n', mean(arraySol));
end
