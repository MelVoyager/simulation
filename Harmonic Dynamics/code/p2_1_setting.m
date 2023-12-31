% Initial conditions
y0 = [0; 10];

% Time span
tspan = [0, 30];

% friction coefficient
gamma = 6;

% Solve the ODE
ode_fun = @(t, y) p2_1_oscillator(t, y, gamma);
[t,y] = ode45(ode_fun, tspan, y0);

% Plot the results
plot(t, y(:,1));
xlabel('Time t');
ylabel('Position x');
title('Position x vs Time t');

% Computed frequency
omega0 = 3;
zeta = gamma / (2 * sqrt(omega0^2));
omega_d_computed = omega0 * sqrt(1 - zeta^2);

fprintf('Computed damped frequency (omega_d_computed) = %f\n', omega_d_computed);

% Find the peaks from the simulated data
[pks, locs] = findpeaks(y(:,1), 'MinPeakDistance', 10);

% Calculate the average period between peaks
if length(locs) > 1
    average_period = mean(diff(t(locs)));
    omega_d_simulated = 2 * pi / average_period;
else
    omega_d_simulated = NaN;
end

fprintf('Simulated damped frequency (omega_d_simulated) = %f\n', omega_d_simulated);