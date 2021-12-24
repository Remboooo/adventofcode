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
    return std::accumulate(std::cbegin(container), std::cend(container), T());
}

template<class T>
void transform_inplace(T& container, auto function) {
    std::transform(std::cbegin(container), std::cend(container), std::begin(container), function);
}

template<class U>
std::vector<U> transform(auto& container, auto function) {
    std::vector<U> result(container.size(), U());
    std::transform(std::cbegin(container), std::cend(container), std::begin(result), function);
    return result;
}

template<class T>
bool contains(const auto& container, const T& value) {
    return std::find(std::cbegin(container), std::cend(container), value) != std::cend(container);
}

template<class T>
long index_of(const auto& container, const T& value) {
    auto cbegin = std::cbegin(container);
    auto i = std::find(cbegin, std::cend(container), value);
    if (i != std::cend(container)) return long(i - cbegin);
    return -1L;
}

template<class T>
void sort(T& container) {
    std::sort(std::begin(container), std::end(container));
}

template<class T>
void rsort(T& container) {
    std::sort(std::rbegin(container), std::rend(container));
}

template<class T>
bool next_permutation(T& container) {
    return std::next_permutation(std::begin(container), std::end(container));
}

// this would be ridiculously faster as a view rather than a copy. can't be arsed atm.
template<class T>
std::vector<std::vector<T>> transposed(const std::vector<std::vector<T>>& s) {
    std::vector<std::vector<T>> result(s[0].size(), std::vector<T>(s.size(), T()));

    for (unsigned i = 0; i < s.size(); ++i) {
        for (unsigned j = 0; j < s[i].size(); ++j) {
            result.at(j)[i] = s[i][j];
        }
    }

    return result;
}

template<class T>
std::pair<T, T> ordered(std::pair<T, T> unordered) {
    if (unordered.first > unordered.second) {
        return std::make_pair(unordered.second, unordered.first);
    } else {
        return unordered;
    }
}

template <typename L, typename R> void append(L& lhs, R const& rhs) {
    lhs.insert(std::end(lhs), std::cbegin(rhs), std::cend(rhs));
}

template <typename T> T appended(std::initializer_list<const T /* can't make this &, dunno why */> lists ) {
    T result;
    for (auto& list : lists) result.insert(std::end(result), std::cbegin(list), std::cend(list));
    return result;
}

template <class T, class A = std::allocator<T> >
class inf_vec;

template <class T, class A = std::allocator<T> >
void swap(inf_vec<T,A>& v1, inf_vec<T,A>& v2) { swap(v1.vec, v2.vec); }

template<class T>
bool in(T& v, std::initializer_list<T> vs) {
    for (auto& c : vs) {
        if (v == c) return true;
    }
    return false;
}

template<class T>
void pad2d(std::vector<std::vector<T>>& vec, size_t width, T val) {
    size_t row_width = 0;
    for (auto& row : vec) {
        row_width = row.size();
        row.insert(row.cbegin(), val);
        row.push_back(val);
    }
    for (size_t s = 0; s < width; ++s) {
        vec.insert(vec.cbegin(), std::vector<T>(row_width+2, val));
        vec.push_back(std::vector<T>(row_width+2, val));
    }
}

template <class T, class A>
class inf_vec {
public:
    typedef typename std::vector<T, A> underlying;
    typedef typename underlying::allocator_type allocator_type;
    typedef typename underlying::value_type value_type;
    typedef typename underlying::reference reference;
    typedef typename underlying::const_reference const_reference;
    typedef typename underlying::difference_type difference_type;
    typedef typename underlying::size_type size_type;
    typedef typename underlying::iterator iterator;
    typedef typename underlying::const_iterator const_iterator;
    typedef typename underlying::reverse_iterator reverse_iterator;
    typedef typename underlying::const_reverse_iterator const_reverse_iterator;

    inf_vec() = default;
    inf_vec(const std::vector<T, A>& other) : vec(other) {}
    ~inf_vec() = default;

    inf_vec& operator=(const underlying& other) { vec = other; return *this; }
    bool operator==(const inf_vec& other) const { return vec == other.vec; }
    bool operator!=(const inf_vec& other) const { return vec != other.vec; }
    bool operator<(const inf_vec& other) const { return vec < other.vec; }
    bool operator>(const inf_vec& other) const { return vec > other.vec; }
    bool operator<=(const inf_vec& other) const { return vec <= other.vec; }
    bool operator>=(const inf_vec& other) const { return vec >= other.vec; }

    operator std::vector<T, A>&() { return vec; }

    iterator begin() { return vec.begin(); }
    const_iterator begin() const { return vec.begin(); }
    const_iterator cbegin() const { return vec.cbegin(); }
    iterator end() { return vec.end(); }
    const_iterator end() const { return vec.end(); }
    const_iterator cend() const { return vec.cend(); }
    reverse_iterator rbegin() { return vec.rbegin(); }
    const_reverse_iterator rbegin() const {return vec.rbegin(); }
    const_reverse_iterator crbegin() const { return vec.crbegin(); }
    reverse_iterator rend() { return vec.rend(); }
    const_reverse_iterator rend() const { return vec.rend(); }
    const_reverse_iterator crend() const { return vec.crend(); }

    reference front() { return vec.front(); }
    const_reference front() const { return vec.front(); }
    reference back() { return vec.back(); }
    const_reference back() const { return vec.back(); }
    template<class ...Args>
    void emplace_front(Args&&... args) { return vec.emplace_front(args...); }
    template<class ...Args>
    void emplace_back(Args&&... args) { return vec.emplace_back(args...); }
    void push_front(const T& v) { return vec.push_front(v); }
    void push_front(T&& v) { return vec.push_front(v); }
    void push_back(const T& v) { return vec.push_back(v); }
    void push_back(T&& v) { return vec.push_back(v); }
    void pop_front() { return vec.pop_front(); }
    void pop_back() { return vec.pop_back(); }
    reference operator[](size_type s) { return at(s); }
    const_reference operator[](size_type s) const { return at(s); }
    reference at(size_type s) {
        while (size() <= s) {

        }
        return vec.at(s);
    }
    const_reference at(size_type s) const { return vec.at(s); }

    template<class ...Args>
    iterator emplace(const_iterator i, Args&&... a) { return vec.emplace(i, a...); }
    iterator insert(const_iterator i, const T& v) { return vec.insert(i, v); }
    iterator insert(const_iterator i, T&& v) { return vec.insert(i, v); }
    iterator insert(const_iterator i, size_type s, T& v) { return vec.insert(i, s, v); }
    template<class iter>
    iterator insert(const_iterator i, iter i2, iter i3) { return vec.insert(i, i2, i3); }
    iterator insert(const_iterator i, std::initializer_list<T> il) { return vec.insert(i, il); }
    iterator erase(const_iterator i) { return vec.erase(i); }
    iterator erase(const_iterator i, const_iterator i2) { return vec.erase(i, i2); }
    void clear() { vec.clear(); }
    template<class iter>
    void assign(iter i, iter i2) { vec.assign(i, i2); }
    void assign(std::initializer_list<T> l) { vec.assign(l); }
    void assign(size_type s, const T& v) { vec.assign(s, v); }

    void swap(inf_vec& other) { vec.swap(other); }
    size_type size() const { return vec.size(); }
    size_type max_size() const { return vec.max_size(); }
    [[nodiscard]] bool empty() const { return vec.empty(); }

    A get_allocator() const { return vec.get_allocator(); }
private:
    underlying vec;

    friend void swap<T, A>(inf_vec<T,A>& v1, inf_vec<T,A>& v2);
};

#endif //AOC2021_CONTAINERS_H
