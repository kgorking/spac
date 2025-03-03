#include <print>
#include <array>
#include <string_view>
#include <ranges>
#include <algorithm>
#include <random>
#include <iostream>

using namespace std::string_view_literals;

using code = std::array<int, 4>;

constexpr auto colour_codes = std::to_array({
	"\033[91m"sv, // rød
	"\033[92m"sv, // grøn
	"\033[93m"sv, // gul
	"\033[94m"sv, // blå
	"\033[95m"sv, // magenta
	"\033[96m"sv, // cyan
	});


int generate_random_colour() {
	return std::rand() % colour_codes.size();
}

code generate_code() {
	code out;
	std::ranges::generate_n(out.begin(), 4, generate_random_colour);
	return out;
}

void print_code(code const c) {
	std::println("{}* {}* {}* {}* \033[0m", colour_codes[c[0]], colour_codes[c[1]], colour_codes[c[2]], colour_codes[c[3]]);
}

code read_guess() {
	std::print("Lav et gæt: ");

	code out;
	std::cin >> out[0] >> out[1] >> out[2] >> out[3];
	return out;
}

void print_help() {
	std::println(R"(Mastermind!
	Tilladte farver er: {}R: rød, {}G :grøn, {}Y: gul, {}B: blå, {}M: magenta, {}C: cyan)",
	colour_codes[0], colour_codes[1], colour_codes[2], colour_codes[3], colour_codes[4], colour_codes[5]);
}

int main() {
	print_help();

	auto const c = generate_code();
	print_code(c);
}