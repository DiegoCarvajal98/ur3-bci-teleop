%% ROS node Matlab
rosinit

global sess
global trial
global ss
global extr
global df
global classif
global experiment

if exist('first_run','var') == 0
    sess = eegtoolkit.util.Session;
    sess.loadAll(3); 
    first_run = 1;
end

% Load filter
load filters/epocfilter;

% Configure preprocessing methods
ss = eegtoolkit.preprocessing.SampleSelection;
ss.sampleRange = [64,640]; % Specify the sample range to be used for each Trial
ss.channels = 6:9; % Specify the channel(s) to be used

df = eegtoolkit.preprocessing.DigitalFilter; % Apply a filter to the raw data
df.filt = Hbp; % Hbp is a filter built with "filterbuilder" matlab function

% Configure CCA extraction method
sti_f = [12,10,8.57,7.5,6.66];
extr = eegtoolkit.featextraction.CCA(sti_f,1:4,128,4);
extr.allFeatures = 1;

% Configure the classifier
classif = eegtoolkit.classification.LIBSVM;

% Load classification model
load("model.mat");

service = rossvcserver('/bci_prediction','roscpp_tutorials/TwoInts', ...
    @matlabServiceCallback,'DataFormat','struct');
client = rossvcclient('/bci_prediction','DataFormat','struct');

req = rosmessage(client);
req.A = int64(2);
req.B = int64(0);
%disp("Debug 0")

if(isServerAvailable(client))
    [~,connectionStatustext] = waitForServer(client);
end

trial = eegtoolkit.util.Trial([],0,0,0,0,0);

function resp = matlabServiceCallback(~,req,resp)
    global sess
    global trial
    global ss
    global df
    global extr
    global classif
    global experiment
    
    % Get one random trial from the dataset according to the subject
    % "intention" selected above
    object = req.A;

    % Get each label trials
    label_1 = [];
    label_2 = [];
    label_3 = [];
    label_4 = [];
    label_5 = [];

    % Group the trials according to its labels
    for i = 1:1375
        tr = sess.trials{1,i}.label;
        if tr == 1
            label_1 = [label_1 i];
        elseif tr == 2
            label_2 = [label_2 i];
        elseif tr == 3
            label_3 = [label_3 i];
        elseif tr == 4
            label_4 = [label_4 i];
        elseif tr == 5
            label_5 = [label_5 i];
        end
    end

    if object == 1 || 2 || 4
        x = randi([1 275]);
    elseif object == 3
        x = randi([1 330]);
    elseif object == 5
        x = randi([1 220]);
    end
    %fprintf("Debug 2 \n")
    if object == int64(1)
        trial.signal = sess.trials{1,label_1(x)}.signal;
        trial.label = sess.trials{1,label_1(x)}.label;
        trial.samplingRate = sess.trials{1,label_1(x)}.samplingRate;
        trial.subjectid = sess.trials{1,label_1(x)}.subjectid;
        trial.sessionid = sess.trials{1,label_1(x)}.sessionid;
        trial.type = sess.trials{1,label_1(x)}.type;
    elseif object == int64(2)
        %fprintf("Debug 2.1 \n")
        trial.signal = sess.trials{1,label_2(x)}.signal;
        trial.label = sess.trials{1,label_2(x)}.label;
        trial.samplingRate = sess.trials{1,label_2(x)}.samplingRate;
        trial.subjectid = sess.trials{1,label_2(x)}.subjectid;
        trial.sessionid = sess.trials{1,label_2(x)}.sessionid;
        trial.type = sess.trials{1,label_2(x)}.type;
        %fprintf("Debug 2.2 \n")
    elseif object == int64(3)
        trial.signal = sess.trials{1,label_3(x)}.signal;
        trial.label = sess.trials{1,label_3(x)}.label;
        trial.samplingRate = sess.trials{1,label_3(x)}.samplingRate;
        trial.subjectid = sess.trials{1,label_3(x)}.subjectid;
        trial.sessionid = sess.trials{1,label_3(x)}.sessionid;
        trial.type = sess.trials{1,label_3(x)}.type;
    elseif object == int64(4)
        trial.signal = sess.trials{1,label_4(x)}.signal;
        trial.label = sess.trials{1,label_4(x)}.label;
        trial.samplingRate = sess.trials{1,label_4(x)}.samplingRate;
        trial.subjectid = sess.trials{1,label_4(x)}.subjectid;
        trial.sessionid = sess.trials{1,label_4(x)}.sessionid;
        trial.type = sess.trials{1,label_4(x)}.type;
    elseif object == int64(5)
        trial.signal = sess.trials{1,label_5(x)}.signal;
        trial.label = sess.trials{1,label_5(x)}.label;
        trial.samplingRate = sess.trials{1,label_5(x)}.samplingRate;
        trial.subjectid = sess.trials{1,label_5(x)}.subjectid;
        trial.sessionid = sess.trials{1,label_5(x)}.sessionid;
        trial.type = sess.trials{1,label_5(x)}.type;
    end
    %fprintf("Debug 3 \n")

    % Preprocess
    ppTrial = ss.process(trial);    % Sample selection
    ppTrial = df.process(ppTrial);  % Digital filter
    
    % Feature extraction
    extr.trials = ppTrial;
    extr.extract;
    classif.instanceSet = extr.getInstances;
    %fprintf("Debug 4 \n")
    [out,~,~] = experiment.classification.classifyInstance(classif.instanceSet);
    
    %fprintf("server return \n")

%   Debug code start
%     out = req.A;
%   Debug code finish

    switch out
        case 1
            resp.Sum = int64(1);
        case 2
            resp.Sum = int64(2);
        case 3
            resp.Sum = int64(3);
        case 4
            resp.Sum = int64(4);
        case 5
            resp.Sum = int64(5);
    end
end