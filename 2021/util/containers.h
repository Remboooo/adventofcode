#ifndef AOC2021_CONTAINERS_H
#define AOC2021_CONTAINERS_H


// Remove stuff in a container if it matches a predicate
void remove_if(auto& container, auto predicate) {
    container.erase(
            std::remove_if(
                    std::begin(container), std::end(container), predicate
            ),
            std::end(container)
    );
}

// Keep only stuff in a container if it matches a predicate
void keep_if(auto& container, auto predicate) {
    remove_if(container, [predicate](auto v){return !predicate(v);});
}

// Keep only stuff in a container if it matches a predicate
template<class T>
std::vector<T> copy_if(const std::vector<T>& container, auto predicate) {
    std::vector<T> result{};
    std::copy_if(std::cbegin(container), std::cend(container), std::back_inserter(result), predicate);
    return result;
}

// Keep only stuff in a container if it matches a predicate
template<class T>
std::vector<T&> copy_ref_if(std::vector<T>& container, auto predicate) {
    std::vector<T&> result{};
    std::copy_if(std::cbegin(container), std::cend(container), std::begin(result), predicate);
    return result;
}

// Count stuff in a container that matches a predicate
unsigned long long count_if(auto& container, auto predicate) {
    return std::count_if(std::cbegin(container), std::cend(container), predicate);
}

bool all_match(const auto& container, auto predicate) {
    return std::all_of(std::cbegin(container), std::cend(container), predicate);
}

bool any_match(const auto& container, auto predicate) {
    return std::any_of(std::cbegin(container), std::cend(container), predicate);
}

template<class T>
T accumulate(const auto& container, T initial, auto binary_op) {
    return std::accumulate(std::cbegin(container), std::cend(container), initial, binary_op);
}

template<class T>
T accumulate(const auto& container) {
    return std::accumulate(std::cbegin(container), std::cend(container));
}

template<class T>
bool contains(const auto& container, const T& value) {
    return std::find(std::cbegin(container), std::cend(container), value) != std::cend(container);
}

// this would be ridiculously faster as a view rather than a copy. can't be arsed atm.
template<class T>
std::vector<std::vector<T>> transposed(const std::vector<std::vector<T>>& s) {
    std::vector<std::vector<T>> result(s[0].size(), std::vector<T>());

    for (unsigned i = 0; i < s.size(); ++i) {
        for (unsigned j = 0; j < s[i].size(); ++j) {
            result.at(j).push_back(s[i][j]);
        }
    }

    return result;
}

#endif //AOC2021_CONTAINERS_H
