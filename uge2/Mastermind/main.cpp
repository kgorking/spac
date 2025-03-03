#include <print>
#include <array>
#include <string_view>
#include <ranges>
#include <algorithm>
#include <random>

using namespace std::string_view_literals;

constexpr auto colour_codes = std::to_array({
	"\033[91m"sv, // rød
	"\033[92m"sv, // grøn
	"\033[93m"sv, // gul
	"\033[94m"sv, // blå
	"\033[95m"sv, // magenta
	"\033[96m"sv, // cyan
	});

enum Colour {
	Red, Green, Yellow, Blue, Magenta, Cyan
};

std::array<int,4> generate_code() {
	std::array<int, 4> out;
	std::ranges::generate_n(out.begin(), 4, [] { return std::rand() % (1+Cyan); });
	return out;
}

int main() {
	for (int i = 0; i < 10; i++)
		std::println("{}", generate_code());

	std::println("\033[91m test");
}