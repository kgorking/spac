#include <print>
#include <iostream>
#include <unordered_map>

double add(double a, double b) { return a + b; }
double sub(double a, double b) { return a - b; }
double mul(double a, double b) { return a * b; }
double div(double a, double b) { return a / b; }
double power(double a, double b) { return std::powl(a, b); }
double sqrt(double a, double b) { return std::powl(b, 1.0 / a); }

static auto const ops = std::unordered_map<char, double(*)(double, double)>{
    {'+', add},
    {'-', sub},
    {'*', mul},
    {'x', mul},
    {'/', div},
    {'^', power},
    {'v', sqrt},
};

int main(int argc, char* argv[]) {
    std::println(R"(
Lommeregner, Gorking stil.
  3 + 5 = 8
  3 - 5 = -2
  3 * 5 = 15
  3 / 5 = 0.6
  10 ^ 3 = 1000
  3 v 1000 = ~10
)");
    std::println("Angiv [tal] [+-*/^v] [tal]:");

    double num1 = 0, num2 = 0;
    char op = '?';

    while (std::cin >> num1 >> op >> num2) {
        if (!ops.contains(op)) {
            std::println("Ukendt operation '{}'", op);
            return 1;
        }

        std::println(" = {}", ops.at(op)(num1, num2));
    }

    return 0;
}
