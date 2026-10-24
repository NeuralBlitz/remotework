/**
 * Mito Core - C++ Extensions
 * High-performance native implementations
 */

#ifndef MITO_CORE_H
#define MITO_CORE_H

#include <string>
#include <vector>
#include <memory>

namespace mito {

class Tokenizer {
public:
    Tokenizer(const std::string& vocab_path);
    std::vector<int> encode(const std::string& text);
    std::string decode(const std::vector<int>& tokens);
    size_t vocab_size() const;
    
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

class Embedding {
public:
    Embedding(size_t dim);
    void set_vector(const std::vector<float>& vec);
    std::vector<float> get_vector() const;
    float cosine_similarity(const Embedding& other) const;
    size_t dimension() const { return dim_; }
    
private:
    size_t dim_;
    std::vector<float> data_;
};

class Tensor {
public:
    Tensor(const std::vector<int>& shape);
    void* data();
    const std::vector<int>& shape() const { return shape_; }
    size_t size() const;
    
private:
    std::vector<int> shape_;
    std::vector<float> data_;
};

class Model {
public:
    virtual ~Model() = default;
    virtual std::vector<float> forward(const std::vector<int>& input) = 0;
    virtual void load(const std::string& path) = 0;
};

} // namespace mito

#endif // MITO_CORE_H
