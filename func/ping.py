t = 0:0.5:40;

T = [ ...
89.5 88.8 87.4 86.5 85.4 84.4 83.3 82.4 81.3 80.4 ...
79.4 78.4 77.6 76.6 75.8 74.9 74 73.1 72.2 71.3 ...
70.6 69.8 68.9 67.9 66.9 66.5 65.8 65.1 64.6 64 ...
63.1 62.3 61.6 60.8 60.4 59.4 58.8 58.5 58 57.6 ...
57 56.2 55.1 54.5 54 53.7 53.3 53 52.4 52.1 ...
51.6 51.3 50.9 50.4 50.1 49.3 49 48.3 48 47.6 ...
47.1 46.7 46.4 45.9 45.6 45.2 44.8 44.3 44 43.8 ...
43.5 43.1 42.8 42.5 42.1 42 41.6 41.2 41 40.8 40.5 ...
];

TA = mean([ ...
22 22 22 22 22 22 22 22 22 22 ...
21.5 21.5 21.5 21.5 21.5 21.5 21.5 21.5 21.5 21.5 ...
22.5 22.5 22.5 22.5 22.5 22.5 22.5 22.5 22.5 22.5 ...
22.5 23 23 23 23 23 23 23 23 23 ...
23 23.5 23.5 23.5 23.5 23.5 23.5 23.5 23.5 23.5 ...
23.5 24 24 24 24 24 24 24 24 24 ...
24 24 24 24 24 24 24 24 24 24 ...
24 24 24 24 24 24 24 24 24 24 24 ...
]);

T0 = T(1);

%metoda 1
coef = polyfit(t, log(T - TA), 1);
K = abs(coef(1));
tau1 = 1 / K;
disp(['Tau1 (metoda 1) = ', num2str(tau1)])

%metoda 2
target = TA + 0.37*(T0 - TA);
[~, idx] = min(abs(T - target));
tau2 = t(idx);
disp(['Tau2 (metoda 2) = ', num2str(tau2)])

%metoda 3
dT0 = (T(2) - T(1)) / (t(2) - t(1));
tau3 = (T0 - TA) / (-dT0);
disp(['Tau3 (metoda 3) = ', num2str(tau3)])

%metoda 4
T10 = T(t == 10);
tau4 = -10 / log( (T10 - TA) / (T0 - TA) );
disp(['Tau4 (metoda 4) = ', num2str(tau4)])

t_sim = linspace(0,150,1000);

T1 = TA + (T0 - TA)*exp(-t_sim/tau1);
T2 = TA + (T0 - TA)*exp(-t_sim/tau2);
T3 = TA + (T0 - TA)*exp(-t_sim/tau3);
T4 = TA + (T0 - TA)*exp(-t_sim/tau4);

figure; hold on; grid on;
plot(t, T, 'ko', 'DisplayName','Date experiment');
plot(t_sim, T1, 'r', 'LineWidth',2,'DisplayName','Metoda 1');
plot(t_sim, T2, 'g', 'LineWidth',2,'DisplayName','Metoda 2');
plot(t_sim, T3, 'b', 'LineWidth',2,'DisplayName','Metoda 3');
plot(t_sim, T4, 'm', 'LineWidth',2,'DisplayName','Metoda 4');
xlabel('Timp [min]');
ylabel('Temperatura [°C]');
legend;
