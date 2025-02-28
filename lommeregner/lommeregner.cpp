#include <print>
#include <iostream>

void print_help() {
    std::println("syntax: num1 op num2, hvor 'op' er +-*/");
}

int main(int argc, char* argv[]) {
    double num1 = 0, num2 = 0;
    char op = '?';

    std::print("Angiv [tal] [+-*/] [tal]: ");
    std::cin >> num1;
    std::cin >> op;
    std::cin >> num2;

    switch (op) {
    case '+':
        std::println("{} + {} = {}", num1, num2, num1 + num2);
        break;

    case '-':
        std::println("{} - {} = {}", num1, num2, num1 - num2);
        break;

    case '*':
        std::println("{} * {} = {}", num1, num2, num1 * num2);
        break;

    case '/':
        if (num2 == 0) {
            std::println("Kan ikke dividere med nul");
            return 1;
        }
        std::println("{} / {} = {}", num1, num2, num1 / num2);
        break;

    default:
        std::println("Ukendt operation '{}'", op);
        return 1;
    }

    return 0;
}
