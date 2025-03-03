#include <print>
#include <array>
#include <string_view>
#include <ranges>
#include <algorithm>
#include <random>
#include <iostream>
#include <optional>
#include <Windows.h>

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
	std::print("{}* {}* {}* {}* \033[0m", colour_codes[c[0]], colour_codes[c[1]], colour_codes[c[2]], colour_codes[c[3]]);
}

int compare_locations(code actual, code guess) {
	int equal = 0;
	for (int i = 0; i < 4; i++)
		equal += actual[i] == guess[i];
	return equal;
}

int compare_colors(code actual, code guess) {
	int hist_guess[6] = { 0,0,0,0,0,0 };
	for (int i : actual)
		hist_guess[i] += 1;

	int equal = 0;
	for (int i = 0; i < 4; i++) {
		if (guess[i] != actual[i] && hist_guess[guess[i]] > 0)
			equal += 1;
	}
	return equal;
}

char char_to_index(char c) {
	switch (c) {
	case 'r': case 'R': return 0;
	case 'g': case 'G': return 1;
	case 'y': case 'Y': return 2;
	case 'b': case 'B': return 3;
	case 'm': case 'M': return 4;
	case 'c': case 'C': return 5;
	default:
		return -1;
	}
}

std::optional<code> read_guess() {
	code out = { 0,0,0,0 };
	std::cin >> (char&)out[0] >> (char&)out[1] >> (char&)out[2] >> (char&)out[3];
	for (int& i : out) {
		int index = char_to_index(i);
		if (i == -1) {
			i = 0;
			std::println("Ugyldig farve");
			return {};
		}

		i = index;
	}

	// TODO check
	return out;
}

void print_help() {
	std::println(R"(Mastermind!
	Gæt de 4 farver i den rigtige rækkefølge.
		Tilladte farver er: {}R: rød, {}G :grøn, {}Y: gul, {}B: blå, {}M: magenta, {}C: cyan
	Du får en rød pind for hver korrect placeret farve.
	"Du får en hvid pind for hver korrekt farve der er placeret forkert.)",
	colour_codes[0], colour_codes[1], colour_codes[2], colour_codes[3], colour_codes[4], colour_codes[5]);
}

int main() {
	SetConsoleOutputCP(1252);
	print_help();

	std::print("\033[0m");
	auto const c = generate_code();
	std::print("Gæt den hemmelig kode på 4 farver: ");

	int num_guesses = 1;
	while (num_guesses <= 12) {
		std::optional<code> const guess = read_guess();

		if (guess) {
			print_code(guess.value());

			if (4 == compare_locations(c, *guess)) {
				std::println("Du gættede rigtigt!");
				break;
			}
			
			std::print("\033[91m");
			int const locs = compare_locations(c, *guess);
			std::print("{:4}", std::string(locs, '|'));

			std::print(" \033[37m");
			int const cols = compare_colors(c, *guess);
			std::print("{:4}", std::string(cols, '|'));

			std::print("   \033[0m");
			num_guesses += 1;
		}
	}
}