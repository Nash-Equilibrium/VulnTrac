#!/bin/bash

# 将当前目录设置为脚本所在目录
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 如果不存在，则创建vendor和build目录
mkdir -p "$DIR/vulnCore/vendor"
mkdir -p "$DIR/vulnCore/build"

# 克隆并构建一个tree-sitter语法的函数
build_grammar() {
    local repo_url=$1
    local repo_dir=$2
    local lang_name=$3

    # 如果目录不存在，则克隆仓库
    if [ ! -d "$DIR/vulnCore/vendor/$repo_dir" ]; then
        git clone $repo_url "$DIR/vulnCore/vendor/$repo_dir"
    fi

    # 进入仓库目录
    cd "$DIR/vulnCore/vendor/$repo_dir"
    
    # 编译共享库，检查 src 目录下的文件存在性
    if [ -f "src/scanner.c" ]; then
        gcc -o "$DIR/vulnCore/build/tree_sitter_${lang_name}.so" -shared -fPIC src/parser.c src/scanner.c
    else
        gcc -o "$DIR/vulnCore/build/tree_sitter_${lang_name}.so" -shared -fPIC src/parser.c
    fi
}

# 为多种语言构建语法库
build_grammar https://github.com/tree-sitter/tree-sitter-python tree-sitter-python python
build_grammar https://github.com/tree-sitter/tree-sitter-c tree-sitter-c c
build_grammar https://github.com/tree-sitter/tree-sitter-cpp tree-sitter-cpp cpp
build_grammar https://github.com/tree-sitter/tree-sitter-go tree-sitter-go go
build_grammar https://github.com/tree-sitter/tree-sitter-java tree-sitter-java java
build_grammar https://github.com/tree-sitter/tree-sitter-javascript tree-sitter-javascript javascript

echo "Tree-sitter语法库已编译并放置在/vulnCore/build目录中。"
