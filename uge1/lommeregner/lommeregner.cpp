import std;

static auto const ops = std::unordered_map<char, double(*)(double, double)>{
    {'+', +[](double a, double b) { return a + b; }},
    {'-', +[](double a, double b) { return a - b; }},
    {'*', +[](double a, double b) { return a * b; }},
    {'/', +[](double a, double b) { return a / b; }},
    {'^', +[](double a, double b) { return std::pow(a, b); }},
    {'v', +[](double a, double b) { return std::pow(b, 1.0 / a); }}
};

int main(int argc, char* argv[]) {
    std::println("Lommeregner, Gorking stil.");
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