% Load the data. Call this once outside of the script so you dont have to
% load the data again and again. Make sure the dataset is included in your
% Matlab path

if exist('first_run','var') == 0
    sess = eegtoolkit.util.Session;
    sess.loadAll(3); 
    first_run = 1;
end

disp("Gráfico de señal original")
nSubject = input("Ingrese el número del sujeto (1-11):\n");
nSession = input("Ingrese el número de la sesión (1-5):\n");
nTrial = input("Ingrese el número de la prueba (1-25):\n");

trialGraph(sess,nSubject,nSession,nTrial);

%Load a filter from the samples
load filters/epocfilter;
% 7 = O1
% 8 = O2

% Stimulus frequencies for generating the CCA reference signals
sti_f = [12,10,8.57,7.5,6.66];

% CCA feat extraction method
extr = eegtoolkit.featextraction.CCA(sti_f,1:4,128,4);
extr.allFeatures = 1;

refer = eegtoolkit.preprocessing.Rereferencing;
%Subtract the mean from the signal
refer.meanSignal = 1;

ss = eegtoolkit.preprocessing.SampleSelection;
ss.sampleRange = [64,640]; % Specify the sample range to be used for each Trial
ss.channels = 6:9; % Specify the channel(s) to be used

df = eegtoolkit.preprocessing.DigitalFilter; % Apply a filter to the raw data
df.filt = Hbp; % Hbp is a filter built with "filterbuilder" matlab function

%Configure the classifier
classif = eegtoolkit.classification.LIBSVM;

%Set the Experimenter wrapper class
experiment = eegtoolkit.experiment.Experimenter;
experiment.session = sess;
experiment.nSubject = nSubject;
experiment.nSession = nSession;
experiment.nTrial = nTrial;
% Add the preprocessing steps (order is taken into account)
experiment.preprocessing = {ss,df};
experiment.featextraction = extr;
experiment.classification = classif;
experiment.evalMethod = experiment.EVAL_METHOD_LOSO; % specify that you want a "leave one subject out" (default is LOOCV)
experiment.run();
for i=1:length(experiment.results)
    accuracies(i) = experiment.results{i}.getAccuracy();
end

accuracies'

figure(1)
subplot(2,2,4)
plot(1:11,accuracies)
title('Precisión del clasificador para cada sujetos')

%mean accuracy for all subjects
fprintf('mean acc = %f\n', mean(accuracies));
%get the configuration used (for reporting)
% experiment.getExperimentInfo
% experiment.getTime