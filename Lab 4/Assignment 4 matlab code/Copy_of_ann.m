path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/assignment5/';
addpath(genpath(path))

trainingSet = csvread('assignment5_train.csv', 0, 1, [0 1 29399 784]);
trainingSet = trainingSet/255;
validationSet = csvread('assignment5_train.csv', 29400, 1, [29400 1 33599 784]);
validationSet = validationSet/255;
targetTraining = csvread('assignment5_train.csv', 0, 0, [0 0 29399 0]);
targetValidation = csvread('assignment5_train.csv', 29400, 0, [29400 0 33599 0]);

IMAGE_SIZE = 784;
NUMBER_NEURONS_HL = 20;
NUMBER_NEURONS_SHL = 15;
NUMBER_NEURONS_OL = 10;
trainingSetLength = 29400;
validationSetLength = 4200;
testingSetLength = 8400;
LEARNING_RATE = 0.1;

binaryTarget = diag(ones(NUMBER_NEURONS_OL,1));

% I create the input layer.

inputLayerValues = zeros(1,IMAGE_SIZE);

% I create the first hidden layer.

hiddenLayerInputs = zeros(1,IMAGE_SIZE);
hiddenLayerWeights = (1+1).*rand(IMAGE_SIZE, NUMBER_NEURONS_HL) - 1;
hiddenLayerBias = (1+1).*rand(1,NUMBER_NEURONS_HL) - 1;
hiddenLayerNets = zeros(1,NUMBER_NEURONS_HL);
hiddenLayerOutputs = zeros(1,NUMBER_NEURONS_HL);
hiddenLayerError = zeros(1,NUMBER_NEURONS_HL);

% I create the second hidden layer.

secondHiddenLayerInputs = zeros(1,NUMBER_NEURONS_HL);
secondHiddenLayerWeights = (1+1).*rand(NUMBER_NEURONS_HL, NUMBER_NEURONS_SHL) - 1;
secondHiddenLayerBias = (1+1).*rand(1,NUMBER_NEURONS_SHL) - 1;
secondHiddenLayerNets = zeros(1,NUMBER_NEURONS_SHL);
secondHiddenLayerOutputs = zeros(1,NUMBER_NEURONS_SHL);
secondHiddenLayerError = zeros(1,NUMBER_NEURONS_SHL);

% I create the output layer.

outputLayerInputs = zeros(1,NUMBER_NEURONS_OL);
outputLayerWeights = (1+1).*rand(NUMBER_NEURONS_SHL, NUMBER_NEURONS_OL) - 1;
outputLayerBias = (1+1).*rand(1,NUMBER_NEURONS_OL) - 1;
outputLayerNets = zeros(1,NUMBER_NEURONS_OL);
outputLayerOutputs = zeros(1,NUMBER_NEURONS_OL);
outputLayerError = zeros(1,NUMBER_NEURONS_OL);

% I create the softmax layer.

softmaxLayerInputs = zeros(1,NUMBER_NEURONS_OL);
softmaxLayerOutputs = zeros(1,NUMBER_NEURONS_OL);

successes = 0;
counter = 0;

while successes/validationSetLength < 0.9
    
    counter = counter + 1;
    successes = 0;

    for training = 1:trainingSetLength
        inputLayerValues = trainingSet(training,:);
        hiddenLayerInputs = inputLayerValues;
        hiddenLayerNets = hiddenLayerInputs * hiddenLayerWeights + hiddenLayerBias;
        hiddenLayerOutputs = sigmoid(hiddenLayerNets);

        secondHiddenLayerInputs = hiddenLayerOutputs;
        secondHiddenLayerNets = secondHiddenLayerInputs * secondHiddenLayerWeights + secondHiddenLayerBias;
        secondHiddenLayerOutputs = sigmoid(secondHiddenLayerNets);

        outputLayerInputs = secondHiddenLayerOutputs;
        outputLayerNets = outputLayerInputs * outputLayerWeights + outputLayerBias;
%         outputLayerOutputs = sigmoid(outputLayerNets);
% 
% %         softmaxLayerInputs = outputLayerOutputs;
%         softmaxLayerOutputs = softmax(softmaxLayerInputs);
        softmaxLayerOutputs = softmax(outputLayerNets);
        [~,output] = max(softmaxLayerOutputs);
        output = output-1;
        %fprintf("Expected: %d, output: %d\n", targetTraining(training), output);

%         for idx = 1:NUMBER_NEURONS_OL
%             targ = binaryTarget(targetTraining(training)+1,idx);
%             outputLayerError(idx) = (targ - softmaxLayerOutputs(idx)) * softmaxLayerOutputs(idx) * (1 - softmaxLayerOutputs(idx));
%         end

        targ = binaryTarget(targetTraining(training)+1,:);
        outputLayerError = (targ - softmaxLayerOutputs);

%         for idx = 1:NUMBER_NEURONS_OL
%             outputLayerWeights(:, idx) = outputLayerWeights(:, idx) + LEARNING_RATE * outputLayerError(idx) * outputLayerInputs(idx);
%             outputLayerBias(idx) = outputLayerBias(idx) + LEARNING_RATE * outputLayerError(idx);
%         end
        outputLayerWeights = outputLayerWeights + LEARNING_RATE * outputLayerInputs' * outputLayerError;
        outputLayerBias = outputLayerBias + LEARNING_RATE * outputLayerError;

        
% 
%         for idx = 1:NUMBER_NEURONS_SHL
%             secondHiddenLayerError(idx) = (1 - secondHiddenLayerOutputs(idx)) * secondHiddenLayerOutputs(idx) * summation;
%         end


        secondHiddenLayerError = (1 - secondHiddenLayerOutputs) .* secondHiddenLayerOutputs .* (outputLayerError * transpose(outputLayerWeights));

%         for idx = 1:NUMBER_NEURONS_SHL
%             secondHiddenLayerWeights(:, idx) = secondHiddenLayerWeights(:, idx) + LEARNING_RATE * secondHiddenLayerError(idx) * secondHiddenLayerInputs(idx);
%             secondHiddenLayerBias(idx) = secondHiddenLayerBias(idx) + LEARNING_RATE * secondHiddenLayerError(idx);
%         end
        secondHiddenLayerWeights = secondHiddenLayerWeights + LEARNING_RATE * secondHiddenLayerInputs' * secondHiddenLayerError;
        secondHiddenLayerBias = secondHiddenLayerBias + LEARNING_RATE * secondHiddenLayerError;

        
%         summation = secondHiddenLayerError * transpose(secondHiddenLayerWeights);
% 
%         for idx = 1:NUMBER_NEURONS_HL
%             hiddenLayerError(idx) = (1 - hiddenLayerOutputs(idx)) * hiddenLayerOutputs(idx) * summation;
%         end

        hiddenLayerError = (1 - hiddenLayerOutputs) .* hiddenLayerOutputs .* (secondHiddenLayerError * transpose(secondHiddenLayerWeights));

% 
%         for idx = 1:NUMBER_NEURONS_HL
%             hiddenLayerWeights(:, idx) = hiddenLayerWeights(:, idx) + LEARNING_RATE * hiddenLayerError(idx) * hiddenLayerInputs(idx);
%             hiddenLayerBias(idx) = hiddenLayerBias(idx) + LEARNING_RATE * hiddenLayerError(idx);
%         end

        hiddenLayerWeights = hiddenLayerWeights + LEARNING_RATE * hiddenLayerInputs' * hiddenLayerError;
        hiddenLayerBias = hiddenLayerBias + LEARNING_RATE * hiddenLayerError;

    end
    % Validation set now.

    for validation = 1:validationSetLength
        inputLayerValues = validationSet(validation,:);
        hiddenLayerInputs = inputLayerValues;
        hiddenLayerNets = hiddenLayerInputs * hiddenLayerWeights + hiddenLayerBias;
%         for sig = 1:NUMBER_NEURONS_HL
%             hiddenLayerOutputs(sig) = sigmoid(hiddenLayerNets(sig));
%         end
        hiddenLayerOutputs = sigmoid(hiddenLayerNets);


        secondHiddenLayerInputs = hiddenLayerOutputs;
        secondHiddenLayerNets = secondHiddenLayerInputs * secondHiddenLayerWeights + secondHiddenLayerBias;
%         for sig = 1:NUMBER_NEURONS_SHL
%             secondHiddenLayerOutputs(sig) = sigmoid(secondHiddenLayerNets(sig));
%         end
        secondHiddenLayerOutputs = sigmoid(secondHiddenLayerNets);

        outputLayerInputs = secondHiddenLayerOutputs;
        outputLayerNets = outputLayerInputs * outputLayerWeights + outputLayerBias;
%         for sig = 1:NUMBER_NEURONS_OL
%             outputLayerOutputs(sig) = sigmoid(outputLayerNets(sig));
%         end

%         softmaxLayerInputs = outputLayerOutputs;
%         softmaxLayerOutputs = softmax(softmaxLayerInputs);

        softmaxLayerOutputs = softmax(outputLayerNets);
        [~,output] = max(softmaxLayerOutputs);
        output = output-1;

        if output == targetValidation(validation)
            successes = successes + 1;
        end
    end
    fprintf("Training round %d, Percentage round: %.2f\n", counter, (successes/validationSetLength)*100.0);
end

testingSet = csvread('assignment5_train.csv', 33600, 1, [33600 1 41999 784]);
testingSet = testingSet/255;
targetTesting = csvread('assignment5_train.csv', 33600, 0, [33600 0 41999 0]);

counter = 0;
successes = 0;

for testing = 1:testingSetLength
    inputLayerValues = testingSet(testing,:);
    hiddenLayerInputs = inputLayerValues;
    hiddenLayerNets = hiddenLayerInputs * hiddenLayerWeights + hiddenLayerBias;
    for sig = 1:NUMBER_NEURONS_HL
        hiddenLayerOutputs(sig) = sigmoid(hiddenLayerNets(sig));
    end

    secondHiddenLayerInputs = hiddenLayerOutputs;
    secondHiddenLayerNets = secondHiddenLayerInputs * secondHiddenLayerWeights + secondHiddenLayerBias;
    for sig = 1:NUMBER_NEURONS_SHL
        secondHiddenLayerOutputs(sig) = sigmoid(secondHiddenLayerNets(sig));
    end

    outputLayerInputs = secondHiddenLayerOutputs;
    outputLayerNets = outputLayerInputs * outputLayerWeights + outputLayerBias;
    for sig = 1:NUMBER_NEURONS_OL
        outputLayerOutputs(sig) = sigmoid(outputLayerNets(sig));
    end

    softmaxLayerInputs = outputLayerOutputs;
    softmaxLayerOutputs = softmax(softmaxLayerInputs);
    [~,output] = max(softmaxLayerOutputs);
    output = output-1;

    if output == targetTesting(testing)
        successes = successes + 1;
        %fprintf("Output: %d, Expected: %d, Percentage so far: %d\n", output, targetTesting(testing), successes/counter);
    end
end
fprintf("Testing, Percentage achieved: %.2f\n", (successes/testingSetLength)*100.0);



% Functions.

function output = sigmoid(net)
    net = -net;
    output = 1./(1+exp(net));
end

function output = softmax(input)
    output = exp(input);
    output = output / sum(output);
end