#include <print>
#include <array>
#include <ranges>
#include <algorithm>
#include <iostream>
#include <optional>
#define NOMINMAX
#include <Windows.h>

// Alias for a color combination to guess
using code = std::array<int, 4>;

// Console color commands
constexpr auto colour_codes = std::to_array({
	"\033[91m", // rød
	"\033[92m", // grøn
	"\033[93m", // gul
	"\033[94m", // blå
	"\033[95m", // magenta
	"\033[96m", // cyan
	});


int generate_random_colour() {
	return std::rand() % colour_codes.size();
}

code generate_code() {
	code out;
	std::ranges::generate_n(out.begin(), 4, generate_random_colour);
	return out;
}

// Print the users guess, as colour coded balls
void print_code(code const c) {
	std::print("{}* {}* {}* {}* \033[0m", colour_codes[c[0]], colour_codes[c[1]], colour_codes[c[2]], colour_codes[c[3]]);
}

// Count the number of equal locations in the guess
int compare_locations(code actual, code guess) {
	int equal = 0;
	for (int i = 0; i < 4; i++)
		equal += actual[i] == guess[i];
	return equal;
}

int compare_colors(code actual, code guess) {
	// Count the number of colours in the guess
	int hist_guess[6] = { 0,0,0,0,0,0 };
	for (int i : actual)
		hist_guess[i] += 1;

	// Count it, if a guess is wrong, but the colour is present in the actual value
	int equal = 0;
	for (int i = 0; i < 4; i++) {
		if (guess[i] != actual[i] && hist_guess[guess[i]] > 0)
			equal += 1;
	}
	return equal;
}

// Convert a character into its colour-code index
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

// Read the users guess from the console
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

// Check if a code is valid
bool valid(code const c) {
	return !std::ranges::contains(c, -1);
}

void print_help() {
	std::println("Mastermind!\n"
		"Gæt de 4 farver i den rigtige rækkefølge.\n"
		"	Tilladte farver er: {}R: rød, {}G :grøn, {}Y: gul, {}B: blå, {}M: magenta, {}C: cyan\033[0m\n"
		"Du får en \033[91mrød\033[0m pind for hver korrect placeret farve.\n"
		"Du får en \033[30m\033[107mhvid\033[0m pind for hver korrekt farve der er placeret forkert.\n"
		"Du har 12 forsøg.\n",
		colour_codes[0], colour_codes[1], colour_codes[2], colour_codes[3], colour_codes[4], colour_codes[5]);
}

int main() {
	// Set the console code-page, so nordic character aren't garbled.
	SetConsoleOutputCP(1252);
	print_help();

	// Generate the colours to guess
	auto const c = generate_code();
	std::print("Gæt den hemmelig kode på 4 farver: ");

	int num_guesses = 1;
	while (num_guesses <= 12) {
		std::optional<code> const guess = read_guess();

		if (guess) {
			if (!valid(*guess)) {
				// Invalid colours are a hard exit, because it messes up
				// my formatting otherwise.
				std::print("Ugyldig farve fundet!");
				exit(1);
			}

			// Print the number of guesses made
			std::print("{:2}  ", num_guesses);
			print_code(guess.value());
			
			// Print the red sticks for each correct location
			std::print("\033[91m");
			int const locs = compare_locations(c, *guess);
			std::print("{}", std::string(locs, '|'));

			// Print the white sticks for each wrong location, but correct colour
			std::print("\033[37m");
			int const cols = compare_colors(c, *guess);
			std::print("{}", std::string(cols, '|'));

			// Fill out the remaing space if needed
			if (locs + cols < 4)
				std::print("{}", std::string(4 - (locs + cols), ' '));

			std::print("   \033[0m");
			num_guesses += 1;

			if (4 == locs) {
				std::println("Du gættede rigtigt i {} forsøg!", num_guesses);
				break;
			}
		}
	}

	if (num_guesses > 12) {
		std::println("Du gættede ikke den rigtige kombination i tide :(");
	}
}