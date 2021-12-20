#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

typedef std::pair<unsigned, bool> field;
typedef std::vector<std::vector<field>> card;

std::vector<card> read_cards(std::ifstream &infile) {
    std::vector<card> cards{};
    std::string line;
    card current_card{};
    while (true) {
        std::getline(infile, line);
        if (line.empty() || infile.eof()) {
            if (!current_card.empty()) cards.push_back(current_card);
            current_card.clear();
            if (infile.eof()) break;
        } else {
            current_card.push_back(string_split<field>(line, " +", [](auto& v){ return std::make_pair(stou(v), false);}));
        }
    }
    return cards;
}

void mark(std::vector<card>& cards, unsigned number) {
    for (auto& card : cards) {
        for (auto& line : card) {
            for (auto& field : line) {
                if (field.first == number) {
                    field.second = true;
                }
            }
        }
    }
}

bool is_winning_card(const card& c) {
    for (auto& row : c) {
        if (all_match(row, [](const field& f){return f.second;})) return true;
    }
    for (auto& row : transposed(c)) {
        if (all_match(row, [](const field& f){return f.second;})) return true;
    }
    return false;
}

std::vector<card> get_winning_cards(const std::vector<card>& cards) {
    return copy_if(cards, &is_winning_card);
}

void process_file(std::ifstream& infile) {
    std::string line;

    std::getline(infile, line);
    auto draw_order = string_split<unsigned>(line, ",", stou);

    std::vector<card> cards = read_cards(infile);

    dbg(std::cout << draw_order << std::endl);
    dbg(std::cout << cards << std::endl);

    for (unsigned draw : draw_order) {
        dbg(std::cout << "Draw " << draw << std::endl);
        mark(cards, draw);
        auto winning_cards = get_winning_cards(cards);

        if (winning_cards.size() == cards.size()) {
            if (winning_cards.size() > 1) {
                std::cout << "Multiple winning cards" << std::endl;
            } else {
                auto &card = winning_cards.at(0);
                std::cout << "Winning card:" << std::endl << card << std::endl;
                int unmarked_sum = accumulate(card, 0, [](int v, const auto &row) {
                    return v + accumulate(row, 0, [](int v, const field &f) {
                        return v + (f.second ? 0 : f.first);
                    });
                });
                std::cout << "Unmarked sum: " << unmarked_sum << std::endl;
                std::cout << "Answer: " << (draw * unmarked_sum) << std::endl;
                return;
            }
        } else {
            remove_if(cards, [&](auto& c){return contains(winning_cards, c);});
            dbg(std::cout << "Remaining cards: " << cards.size() << std::endl);
        }
    }
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
