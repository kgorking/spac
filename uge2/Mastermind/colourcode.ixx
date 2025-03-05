export module colourcode;
import std;
import colourprint;

//
// Contains code to manage colour codes
//

export code generate_code() {
	auto generate_random_colour = []() { return Colour(std::rand() % Colour::Default); };

	code out;
	std::ranges::generate_n(out.begin(), 4, generate_random_colour);
	return out;
}

// Count the correct colours and wrong locations
export std::pair<int, int> compare_colors(code actual, code guess) {
	// Count the number of colours in 'actual'
	int hist_actual[6] = { 0,0,0,0,0,0 };
	for (int i : actual)
		hist_actual[i] += 1;

	int correct_locations = 0;
	int wrong_locations = 0;

	// Count correct locations first
	// This is needed fx. when comparing guess RRRR to actual CRCR
	// If not separated, it would return 1 correct location and 1 wrong location,
	// when it should return 2 correct locations
	for (int i = 0; i < 4; i++) {
		// If the colour is not in the histogram, ignore it
		if (hist_actual[guess[i]] == 0)
			continue;

		if (guess[i] == actual[i] && (hist_actual[guess[i]] > 0)) {
			correct_locations += 1;

			// Decrease the histogram count.
			hist_actual[guess[i]] -= 1;
		}
	}

	// Count wrong locations last
	for (int i = 0; i < 4; i++) {
		// If the colour is not in the histogram, ignore it
		if (hist_actual[guess[i]] == 0)
			continue;

		// The two colours are not equal.
		// If the guess colour exists in the histogram of the actual code,
		// count it as in the wrong location.
		if (guess[i] != actual[i] && (hist_actual[guess[i]] > 0)) {
			wrong_locations += 1;

			// Decrease the histogram count.
			hist_actual[guess[i]] -= 1;
		}
	}

	return { correct_locations, wrong_locations };
}

// Convert a character into its colour
Colour char_to_color(char c) {
	switch (c) {
	case 'r': case 'R': return Colour::Red;
	case 'g': case 'G': return Colour::Green;
	case 'y': case 'Y': return Colour::Yellow;
	case 'b': case 'B': return Colour::Blue;
	case 'm': case 'M': return Colour::Magenta;
	case 'c': case 'C': return Colour::Cyan;
	default:
		return Colour::Default;
	}
}

export std::expected<code, int> code_from_string(std::string_view sv) {
	if (sv.size() != 4) {
		return std::unexpected(0);
	}

	code out;
	std::ranges::fill(out, Colour::Default);

	for (int i = 0; i < 4; i++) {
		Colour const clr = char_to_color(sv[i]);
		if (clr == Colour::Default) {
			return std::unexpected(1);
		}

		out[i] = clr;
	}

	return out;
}
