import std;
import colourprint;
import combination;

#define NOMINMAX
#include <Windows.h>

void print_help() {
	cp_println("Mastermind!\nGæt de 4 farver i den rigtige rækkefølge.");
	cp_print("Farverne er RGUBMC: ", Red, "(R)ød, ", Green, "(G)røn, ", Yellow, "G(u)l, ", Blue, "(B)lå, ", Magenta, "(M)agenta, ", Cyan, "(C)yan\n");
	cp_println(
		"Du får en ", Black, RedBg, "Rød ", Default, " pind for hver korrect farve der er placeret korrekt.\n"
		"Du får en ", Black, WhiteBg, "Hvid", Default, " pind for hver korrekt farve der er placeret forkert.\n"
		"Du har 12 forsøg.\n");
}

// Read the users guess from the console
auto read_guess() -> std::optional<combi> {
	// Save current cursor position
	std::print("\x1b[s");

	// Read the users guess
	std::string s;
	std::cin >> s;

	// Check for exit/quit
	if (s == "exit" || s == "quit")
		exit(0);

	// Parse the code and return it if it's valid
	if (auto const code = combination_from_string(s); code.has_value()) {
		return *code;
	}
	else {
		// Print error message
		switch (code.error()) {
			case 0:  cp_print(Colour::Red, "Angiv 4 farver"); break;
			case 1:  cp_print(Colour::Red, "Ugyldig farve."); break;
			default: cp_print(Colour::Red, "Ukendt fejl."); break;
		}

		// Restore previous cursor position and delete user input
		std::print("\x1b[u\x1b[0K");

		return {};
	}
}

int main() {
	// Set the console code-page, so Nordic characters aren't garbled.
	SetConsoleOutputCP(1252);

	// Use current time as seed for random generator
	std::srand(static_cast<unsigned>(std::time(0)));

	// Print help message about how to play
	print_help();

	// Generate the colour to guess
	auto const combo_to_guess = generate_color_combination();
	cp_print("Gæt den hemmelige kode på 4 farver: ");
	//cp_print_combi(combo_to_guess); // debug, prints the generated code to guess
	cp_println();

	// Set up guess counter and print initial guess.
	// It is printed here for formatting reasons.
	int num_guesses = 1;
	cp_print(std::format("{:2}  ", num_guesses));

	while (num_guesses <= 12) {
		// Save current cursor position
		std::print("\x1b[s");

		// Read the players guess
		std::optional<combi> const guess = read_guess();

		// Restore previous cursor position and delete user input
		std::print("\x1b[u\x1b[0K");

		if (!guess)
			continue;

		// Print the entered colour code
		auto const& c = *guess;
		cp_print_combi(c);

		cp_print("  ");

		// Print the red sticks for each correct location
		// and print the white sticks for each wrong location, but correct colour
		auto const [locs, cols] = compare_combinations(combo_to_guess, c);
		cp_print(Colour::Red, std::string(locs, '|'));
		cp_print(Colour::Default, std::string(cols, '|'));

		// Fill out the remaining space if needed
		if (locs + cols < 4)
			cp_print(std::string(4 - (locs + cols), ' '));

		cp_println();

		// Check for win-condition
		if (4 == locs) {
			cp_print(Colour::Green, "\nDu gættede rigtigt i ", num_guesses, " forsøg!");
			break;
		}

		// Increase guess count after checking for win condition
		num_guesses += 1;

		// Print the number of guesses made,
		// and clear any potential error messages
		cp_print(std::format("{:2}  \x1b[0K", num_guesses));
	}

	// Print lose message and correct combination
	if (num_guesses > 12) {
		cp_print(Colour::Red, "\nDu gættede ikke den rigtige kombination ");
		cp_print_combi(combo_to_guess);
		cp_println(Colour::Red, " i tide :(");
	}
}