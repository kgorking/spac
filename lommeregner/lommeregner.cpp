#include <print>
#include <iostream>

int main(int argc, char* argv[]) {
    double num1 = 0, num2 = 0;
    char op = '?';

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

    while (std::cin >> num1) {
        std::cin >> op;
        std::cin >> num2;

        switch (op) {
        case '+':
            std::println(" = {}", num1 + num2);
            break;

        case '-':
            std::println(" = {}", num1 - num2);
            break;

        case '*':
            std::println(" = {}", num1 * num2);
            break;

        case '/':
            if (num2 == 0) {
                std::println("Kan ikke dividere med nul");
                return 1;
            }
            std::println(" = {}", num1 / num2);
            break;

        case '^':
            std::println(" = {}", std::powl(num1, num2));
            break;

        case 'v':
            std::println(" = {}", std::powl(num2, 1.0 / num1));
            break;

        default:
            std::println("Ukendt operation '{}'", op);
            return 1;
        }
    }

    return 0;
}
