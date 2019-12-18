#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
#include <cstdint>
#include <unordered_map>

typedef std::tuple<uint8_t, long> cache_key_t;

struct cache_key_hash : public std::unary_function<cache_key_t, std::size_t> {
    std::size_t operator()(const cache_key_t& k) const{
        return std::get<0>(k) | (std::get<1>(k) << 8);
    }
};

struct cache_key_equal : public std::binary_function<cache_key_t, cache_key_t, bool> {
    bool operator()(const cache_key_t& v0, const cache_key_t& v1) const {
        return (std::get<0>(v0) == std::get<0>(v1) && std::get<1>(v0) == std::get<1>(v1));
    }
};

class FFT {
public:
    FFT(std::vector<uint8_t>& input_digits, long sequence_length)
    : input_digits(input_digits), sequence_length(sequence_length) {

    }

    uint8_t get_digit(uint8_t round, long position) {
        if (round == 0) {
            return uint8_t(input_digits[position % input_digits.size()] % 10);
        }

        const auto key = std::make_tuple(round, position);
        auto found = sum_cache.find(key);
        if (found != sum_cache.end()) {
            return uint8_t(std::abs(found->second) % 10);
        } else {
            auto found_prev = sum_cache.find(std::make_tuple(round, position-1));
            long sum;
            if (found_prev != sum_cache.end()) {
                // Fast path: we have the sum of a previous position; the only deltas with this position are the
                // boundaries of the series of 1s and -1s.
                sum = found_prev->second;
                for (long x = position; x < sequence_length; x += 4 * (position + 1)) {
                    sum -= get_digit(uint8_t(round - 1), x - 1);
                    if (x + position < sequence_length) {
                        sum += get_digit(uint8_t(round - 1), x + position);
                    }
                }

                for (long x = 2 + 3 * position; x < sequence_length; x += 4 * (position + 1)) {
                    sum += get_digit(uint8_t(round - 1), x - 1);
                    if (x + position < sequence_length) {
                        sum -= get_digit(uint8_t(round - 1), x + position);
                    }
                }
            } else {
                // Slow path: sum all the relevant digits from a previous round
                sum = 0;
                for (long x = position; x < sequence_length; x += 4 * (position + 1)) {
                    for (long dx = 0; dx <= position; ++dx) {
                        if (x + dx < sequence_length) {
                            sum += get_digit(uint8_t(round - 1), x + dx);
                        }
                    }
                }

                for (long x = 2 + 3 * position; x < sequence_length; x += 4 * (position + 1)) {
                    for (long dx = 0; dx < (position + 1); ++dx) {
                        if (x + dx < sequence_length) {
                            sum -= get_digit(uint8_t(round - 1), x + dx);
                        }
                    }
                }
            }

            sum_cache[key] = sum;
            if (sum_cache.size() % 10000 == 0)
                std::cout << "r" << int(round) << "p" << position << " = " << sum << "; s=" << sum_cache.size()
                          << std::endl;
            return uint8_t(std::abs(sum) % 10);
        }
    }

private:
    std::vector<uint8_t>& input_digits;
    long sequence_length;

    std::unordered_map<cache_key_t, long, cache_key_hash, cache_key_equal> sum_cache;

};


int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Need input digits file as argument" << std::endl;
        return -1;
    }
    std::cout << argv[1] << std::endl;
    std::ifstream infile(argv[1]);
    if (infile.fail()) {
        std::cerr << "Could not open file" << std::endl;
        return -1;
    }

    std::vector<uint8_t> input_digits;

    char c;
    while (infile.get(c)) {
        if (c < '0' || c > '9')
            break;

        input_digits.push_back((uint8_t)(c - '0'));
    }

    std::cout << "Input size: " << input_digits.size() << std::endl;

    FFT fft(input_digits, 10000 * input_digits.size());

    long message_offset = 0;
    for (int i = 0; i < 7; ++i) {
        message_offset = message_offset * 10 + input_digits[i];
    }
    std::cout << "Message offset: " << message_offset << std::endl;

    std::vector<uint8_t> message;
    
    for (long i = 0; i < 8; ++i) {
        const auto digit = fft.get_digit(100, message_offset + i);
        std::cout << "Pos " << i << ": " << int(digit) << std::endl;
        message.push_back(digit);
    }

    std::cout << std::endl << "Message: ";

    for (const auto& digit : message) {
        std::cout << int(digit);
    }

    std::cout << std::endl;

    return 0;
}