%% Clasificación de señales

if exist('first_run','var') == 0
    sess = eegtoolkit.util.Session;
    sess.loadAll(3); 
    first_run = 1;
end

load filters/epocfilter;

ss = eegtoolkit.preprocessing.SampleSelection;
ss.sampleRange = [64,640]; % Specify the sample range to be used for each Trial
ss.channels = 6:9; % Specify the channel(s) to be used

df = eegtoolkit.preprocessing.DigitalFilter; % Apply a filter to the raw data
df.filt = Hbp; % Hbp is a filter built with "filterbuilder" matlab function

sti_f = [12,10,8.57,7.5,6.66];
extr = eegtoolkit.featextraction.CCA(sti_f,1:4,128,4);
extr.allFeatures = 1;

%Configure the classifier
classif = eegtoolkit.classification.LIBSVM;

fprintf("Selecciones uno de los objetos:\n" + ...
    "1. Cilindro\n" + ...
    "2. Esfera\n" + ...
    "3. Cubo\n")
object = input("Objeto: ");

% Get each label trials
label_1 = [];
label_2 = [];
label_3 = [];
label_4 = [];
label_5 = [];

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

if object == 1
    trial = eegtoolkit.util.Trial(sess.trials{1,label_1(x)}.signal, ...
        sess.trials{1,label_1(x)}.label,sess.trials{1,label_1(x)}.samplingRate, ...
        sess.trials{1,label_1(x)}.subjectid,sess.trials{1,label_1(x)}.sessionid, ...
        sess.trials{1,label_1(x)}.type);
elseif object == 2
    trial = eegtoolkit.util.Trial(sess.trials{1,label_2(x)}.signal, ...
        sess.trials{1,label_2(x)}.label,sess.trials{1,label_2(x)}.samplingRate, ...
        sess.trials{1,label_2(x)}.subjectid,sess.trials{1,label_2(x)}.sessionid, ...
        sess.trials{1,label_2(x)}.type);
elseif object == 3
    trial = eegtoolkit.util.Trial(sess.trials{1,label_3(x)}.signal, ...
        sess.trials{1,label_3(x)}.label,sess.trials{1,label_3(x)}.samplingRate, ...
        sess.trials{1,label_3(x)}.subjectid,sess.trials{1,label_3(x)}.sessionid, ...
        sess.trials{1,label_3(x)}.type);
elseif object == 4
    trial = eegtoolkit.util.Trial(sess.trials{1,label_4(x)}.signal, ...
        sess.trials{1,label_4(x)}.label,sess.trials{1,label_4(x)}.samplingRate, ...
        sess.trials{1,label_4(x)}.subjectid,sess.trials{1,label_4(x)}.sessionid, ...
        sess.trials{1,label_4(x)}.type);
elseif object == 5
    trial = eegtoolkit.util.Trial(sess.trials{1,label_5(x)}.signal, ...
        sess.trials{1,label_5(x)}.label,sess.trials{1,label_5(x)}.samplingRate, ...
        sess.trials{1,label_5(x)}.subjectid,sess.trials{1,label_5(x)}.sessionid, ...
        sess.trials{1,label_5(x)}.type);
end

% Preprocess
ppTrial = ss.process(trial);    % Sample selection
ppTrial = df.process(ppTrial);  % Digital filter

% Feature extraction
extr.trials = ppTrial;
extr.extract;
classif.instanceSet = extr.getInstances;

% Load classification model
load("model.mat");
[outputLabels, outputScores, outputRanking] = experiment.classification.classifyInstance(classif.instanceSet)