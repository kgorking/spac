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

// Count the number correct colours in wrong locations
export std::pair<int, int> compare_colors(code actual, code guess) {
	// Count the number of colours in 'actual'
	int hist_actual[6] = { 0,0,0,0,0,0 };
	for (int i : actual)
		hist_actual[i] += 1;


	std::array<bool, 4> wrong_locations{};
	std::array<bool, 4> correct_locations{};

	for (int i = 0; i < 4; i++) {
		// If the colour is not in the histogram, ignore it
		if (hist_actual[guess[i]] == 0)
			continue;

		if (guess[i] != actual[i]) {
			// The two colours are not equal.
			// If the guess colour exists in the histogram of the actual code,
			// count it as in the wrong location.
			wrong_locations[i] = hist_actual[guess[i]] > 0;
		}
		else {
			correct_locations[i] = true;
		}

		// Decrease the histogram count.
		hist_actual[guess[i]] -= 1;
	}

	// Return the number of correct locations and correct colours in wrong locations
	auto reduce = std::bind_back(std::ranges::fold_left, 0, std::plus{}); // why is there no std::ranges::reduce?
	int const num_correct_loc = reduce(correct_locations);
	int const num_wrong_loc = reduce(wrong_locations);
	return { num_correct_loc, num_wrong_loc };
}

// Convert a character into its colour-code index
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
