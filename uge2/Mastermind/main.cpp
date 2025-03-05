import std;
import colourprint;
import colourcode;

#define NOMINMAX
#include <Windows.h>

void print_help() {
	cp_println("Mastermind!\nGæt de 4 farver i den rigtige rækkefølge.");
	cp_print("   Tilladte farver er: ", Red, "R: rød, ", Green, "G :grøn, ", Yellow, "Y: gul, ", Blue, "B: blå, ", Magenta, "M: magenta, ", Cyan, "C: cyan\n");
	cp_println(
		"Du får en ", Red, "rød", Default, " pind for hver korrect placeret farve.\n"
		"Du får en ", WhiteBg, "hvid", Default, " pind for hver korrekt farve der er placeret forkert.\n"
		"Du har 12 forsøg.\n");
}

// Read the users guess from the console
auto read_guess() -> std::optional<code> {
	// Save current cursor position
	std::print("\x1b[s");

	// Read the users guess
	std::string s;
	std::cin >> s;

	// Check for exit/quit
	if (s == "exit" || s == "quit")
		exit(0);

	// Parse the code and return it if it's valid
	if (auto const code = code_from_string(s); code.has_value()) {
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
	auto const combo_to_guess = generate_code();
	cp_print("Gæt den hemmelige kode på 4 farver: ");
	//cp_print_code(combo_to_guess);

	int num_guesses = 1;
	while (num_guesses <= 12) {
		std::optional<code> const guess = read_guess();

		if (!guess)
			continue;

		// Print the number of guesses made and the entered colour code
		cp_print(std::format("{:2}  ", num_guesses));
		auto const& c = *guess;
		cp_print_code(c);
			
		// Print the red sticks for each correct location
		// and print the white sticks for each wrong location, but correct colour
		auto const [locs, cols] = compare_colors(combo_to_guess, c);
		cp_print(Colour::Red, std::string(locs, '|'));
		cp_print(Colour::Default, std::string(cols, '|'));

		// Fill out the remaining space if needed
		if (locs + cols < 4)
			cp_print(std::string(4 - (locs + cols), ' '));

		cp_print("   ");
		num_guesses += 1;

		// Check for win-condition
		if (4 == locs) {
			cp_print(Colour::Green, "\nDu gættede rigtigt i ", num_guesses, " forsøg!");
			break;
		}
	}

	if (num_guesses > 12) {
		cp_println(Colour::Red, "\nDu gættede ikke den rigtige kombination i tide :(");
		cp_print("Den korrekt kode var ");
		cp_print_code(combo_to_guess);
	}
}