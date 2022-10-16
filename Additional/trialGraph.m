function [] = trialGraph(sess,nSubject,nSession,nTrial)
tSubject = 1375/11;
tSession = tSubject/5;

% disp("Gráfico de señal original")
% nSubject = input("Ingrese el número del sujeto (1-11):\n");
% nSession = input("Ingrese el número de la sesión (1-5):\n");
% nTrial = input("Ingrese el número de la prueba (1-25):\n");       

sTrial = tSubject*(nSubject-1)+tSession*(nSession-1)+nTrial;

signal = sess.trials{sTrial}.signal(6:9,:);

signal= signal-4200;
Tm = 1/sess.trials{sTrial}.samplingRate;
t = 0:Tm:sess.trials{sTrial}.duration-Tm;

ofst = (1:size(signal,1))*50 + 25;                               % iOffsetg Vector
EEGp = bsxfun(@plus, signal', ofst)';                                  % Add iOffsetg To Each Row
figure(1)
subplot(2,2,1);
plot(t, EEGp)                                                       % Plot EEG
ChC = ["P7","O1","O2","P8"];
yt = ofst;                                                   % Y-Yick Positions
set(gca, 'YTick',yt, 'YTickLabel',ChC(1:end))
title('Señal original')
end