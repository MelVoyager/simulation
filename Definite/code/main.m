
function main
    % 初始条件 [x1_0, x1'_0, x2_0, x2'_0]
    init = [0, 0, 1, 1];  

    % 参数：质量m1, m2，阻尼系数c，弹簧常数k1, k2
    m1 = 500;  % 示例值
    m2 = 50;   % 示例值
    c = 200;   % 示例值
    k1 = 20000;  % 示例值
    k2 = 200000;  % 示例值

    % 时间范围
    tspan = [0 10]; 

    % 使用ode45求解
    [t, sol] = ode45(@(t, y) odefunc(t, y, m1, m2, c, k1, k2), tspan, init);

    % 绘图
    figure;
    plot(t, sol(:, 1), 'r', t, sol(:, 3), 'b');
    legend('x1', 'x2');
    xlabel('Time');
    ylabel('Displacement');
    title('Displacement vs. Time for a Damped Oscillator System with External Force');
end

function dydt = odefunc(t, y, m1, m2, c, k1, k2)
    % y = [x1; x1'; x2; x2']
    dydt = zeros(4, 1);
    dydt(1) = y(2);
    dydt(2) = (-c*(y(2) - y(4)) - k1*(y(1) - y(3)))/m1;
    dydt(3) = y(4);
    dydt(4) = (c*(y(2) - y(4)) + k1*(y(1) - y(3)) - k2*y(3) + 1000 * cos(2 * pi * 10.555 * t))/m2;
end
