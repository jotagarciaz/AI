path = '/Users/jgarcia/Documents/Artificial Intelligence/Lab 4';
addpath(genpath(path))

% trainingSet = csvread('assignment5_train.csv', 0, 1, [0 1 3 784]); %testing purposes
% trainingSet = trainingSet/255;

trainingSet = csvread('assignment5_train.csv', 0, 1, [0 1 29399 784]);
trainingSet = trainingSet/255;
validationSet = csvread('assignment5_train.csv', 29400, 1, [29400 1 33599 784]);
validationSet = validationSet/255;
targetTraining = csvread('assignment5_train.csv', 0, 0, [0 0 29399 0]);
targetValidation = csvread('assignment5_train.csv', 29400, 0, [29400 0 33599 0]);
% target = csvread('assignment5_train.csv', 0, 0, [0 0 3 0]);

IMAGE_SIZE = 784;
NUMBER_NEURONS_HL = 20;
NUMBER_NEURONS_SHL = 25;
NUMBER_NEURONS_OL = 10;
trainingSetLength = 29400;
validationSetLength = 4200;
testingsetLength = 8400;
LEARNING_RATE = 0.1;
binaryTarget = diag(ones(NUMBER_NEURONS_OL,1));

% I create the input layer.

inputLayerInputs = zeros(1,IMAGE_SIZE);
inputLayerWeights = (1+1).*rand(IMAGE_SIZE, NUMBER_NEURONS_HL) - 1;
inputLayerBias = (1+1).*rand(1,NUMBER_NEURONS_HL) - 1;
inputLayerNets = zeros(1,NUMBER_NEURONS_HL);
inputLayerOutputs = zeros(1,NUMBER_NEURONS_HL);

% I create the first hidden layer.

hiddenLayerInputs = zeros(1,NUMBER_NEURONS_HL);
hiddenLayerWeights = (1+1).*rand(NUMBER_NEURONS_HL, NUMBER_NEURONS_OL) - 1;
hiddenLayerBias = (1+1).*rand(1,NUMBER_NEURONS_OL) - 1;
hiddenLayerNets = zeros(1,NUMBER_NEURONS_OL);
hiddenLayerOutputs = zeros(1,NUMBER_NEURONS_OL);
hiddenLayerError = zeros(1,NUMBER_NEURONS_HL);

% I create the output layer.

outputLayerInputs = zeros(1,NUMBER_NEURONS_OL);
outputLayerOutputs = zeros(1,NUMBER_NEURONS_OL);
outputLayerError = zeros(1,NUMBER_NEURONS_OL);

hits = 0;
counter = 0;

while hits/trainingSetLength < 0.8
    
    counter = counter + 1;
    fprintf("Training round %d, Percentage last round: %d \n", counter, hits/trainingSetLength);
    hits = 0;

    for training = 1:trainingSetLength
        inputLayerInputs = trainingSet(training,:);
        inputLayerNets = inputLayerInputs * inputLayerWeights + inputLayerBias;
        for sig = 1:NUMBER_NEURONS_HL
            inputLayerOutputs(sig) = sigmoid(inputLayerNets(sig));
        end

        hiddenLayerInputs = inputLayerOutputs;
        hiddenLayerNets = hiddenLayerInputs * hiddenLayerWeights + hiddenLayerBias;
        for sig = 1:NUMBER_NEURONS_OL
            hiddenLayerOutputs(sig) = sigmoid(hiddenLayerNets(sig));
        end

        outputLayerInputs = hiddenLayerOutputs;
        outputLayerOutputs = softmax(outputLayerInputs);
        [~,output] = max(outputLayerOutputs);
        output = output-1;
        %fprintf("Expected: %d, output: %d\n", targetTraining(training), output);

        for idx = 1:NUMBER_NEURONS_OL
            targ = binaryTarget(targetTraining(training)+1,idx);
            outputLayerError(idx) = (targ - outputLayerOutputs(idx)) * outputLayerOutputs(idx) * (1 - outputLayerOutputs(idx));
        end

        for idx = 1:NUMBER_NEURONS_OL
            hiddenLayerWeights(idx) = hiddenLayerWeights(idx) + LEARNING_RATE * outputLayerError(idx) * outputLayerInputs(idx);
        end
        
        summation = sum(outputLayerError * transpose(hiddenLayerWeights));

        for idx = 1:NUMBER_NEURONS_OL
            hiddenLayerError(idx) = (1 - hiddenLayerOutputs(idx)) * hiddenLayerOutputs(idx) * summation;
        end

        for idx = 1:NUMBER_NEURONS_HL
            inputLayerWeights(idx) = inputLayerWeights(idx) + LEARNING_RATE * hiddenLayerError(idx) * hiddenLayerInputs(idx);
        end
        if output == targetTraining(training)
            hits = hits + 1;
        end
    end
end

% Validation set now.

for validation = 1:validationSetLength
    inputLayerInputs = validationSet(validation,:);
    inputLayerNets = inputLayerInputs * inputLayerWeights + inputLayerBias;
    for sig = 1:NUMBER_NEURONS_HL
        inputLayerOutputs(sig) = sigmoid(inputLayerNets(sig));
    end

    hiddenLayerInputs = inputLayerOutputs;
    hiddenLayerNets = hiddenLayerInputs * hiddenLayerWeights + hiddenLayerBias;
    for sig = 1:NUMBER_NEURONS_OL
        hiddenLayerOutputs(sig) = sigmoid(hiddenLayerNets(sig));
    end

    outputLayerInputs = hiddenLayerOutputs;
    outputLayerOutputs = softmax(outputLayerInputs);
    [~,output] = max(outputLayerOutputs);
    output = output-1;

    if output == targetValidation(validation)
        hits = hits + 1;
    end
end

testingSet = csvread('assignment5_train.csv', 33600, 1, [33600 1 41999 784]);
testingSet = testingSet/255;
targetTesting = csvread('assignment5_train.csv', 0, 33600, [0 0 41999 0]);

counter = 0;
hits = 0;

for testing = 1:testingSetLength
    inputLayerInputs = testingSet(testing,:);
    inputLayerNets = inputLayerInputs * inputLayerWeights + inputLayerBias;
    for sig = 1:NUMBER_NEURONS_HL
        inputLayerOutputs(sig) = sigmoid(inputLayerNets(sig));
    end

    hiddenLayerInputs = inputLayerOutputs;
    hiddenLayerNets = hiddenLayerInputs * hiddenLayerWeights + hiddenLayerBias;
    for sig = 1:NUMBER_NEURONS_SHL
        hiddenLayerOutputs(sig) = sigmoid(hiddenLayerNets(sig));
    end

    outputLayerInputs = hiddenLayerOutputs;
    outputLayerOutputs = softmax(outputLayerInputs);
    [~,output] = max(outputLayerOutputs);
    output = output-1;

    if output == targetTesting(testing)
        hits = hits + 1;
        fprintf("Output: %d, Expected: %d, Percentage so far: %d\n", output, targetTesting(testing), hits/counter);
    end
end



% Functions.

function output = sigmoid(net)
    net = -net;
    output = 1/(1+exp(net));
end

function output = softmax(input)
    output = exp(input);
    output = output / sum(output);
end