export module colourprint;
import std;

//
// Contains functions to do coloured output to the console
//

// The supported colours
export enum Colour {
	Red,
	Green,
	Yellow,
	Blue,
	Magenta,
	Cyan,
	Default,
	WhiteBg,
	Max
};

// Alias for a color combination to guess
export using code = std::array<Colour, 4>;


// Console color commands
constexpr auto colour_codes = std::to_array({
	"\033[91m", // rød
	"\033[92m", // grøn
	"\033[93m", // gul
	"\033[94m", // blå
	"\033[95m", // magenta
	"\033[96m", // cyan
	"\033[0m",  // default
	"\033[107m", // hvid baggrund
	});

// Change the text colour
void print_one(Colour clr) {
	std::print("{}", colour_codes[clr]);
}

// Print whatever
void print_one(auto other) {
	std::print("{}", other);
}

// Print a bunch of arguments by sending each to 'print_one'*'
// Text colour is set to default before and after printing
export void cp_print(auto&& ...args) {
	print_one(Colour::Default);
	(print_one(args), ...);
	print_one(Colour::Default);
}

// Print a bunch of arguments by sending each to 'print_one'
// Prints a newline at end.
// Text colour is set to default before and after printing
export void cp_println(auto&& ...args) {
	print_one(Colour::Default);
	(print_one(args), ...);
	print_one(Colour::Default);
	std::println();
}

// Print a colour code with colours
export void cp_print_code(code const c) {
	cp_print(c[0], "* ", c[1], "* ", c[2], "* ", c[3], "* ");
}