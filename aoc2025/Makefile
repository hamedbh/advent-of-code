# Set UV_ENV_FILE to load .env from project root
export UV_ENV_FILE = ../.env

.PHONY: help python rust clean lint format setup-day readme rust-build

# Find all input data files and generate corresponding answer file paths
SOURCE_DATA_FILES=$(wildcard data/inputs/day*.txt)
# Generate Python answer file paths
PY_ANSWER_FILES_PART1=$(patsubst data/inputs/day%.txt,data/outputs/python/day%_part1.txt,$(SOURCE_DATA_FILES))
PY_ANSWER_FILES_PART2=$(patsubst data/inputs/day%.txt,data/outputs/python/day%_part2.txt,$(SOURCE_DATA_FILES))
PY_ANSWER_FILES=$(PY_ANSWER_FILES_PART1) $(PY_ANSWER_FILES_PART2)
# Find all Rust day source files and generate corresponding answer file paths
RUST_SOURCE_FILES=$(wildcard rust/src/day*.rs)
RUST_ANSWER_FILES_PART1=$(patsubst rust/src/day%.rs,data/outputs/rust/day%_part1.txt,$(RUST_SOURCE_FILES))
RUST_ANSWER_FILES_PART2=$(patsubst rust/src/day%.rs,data/outputs/rust/day%_part2.txt,$(RUST_SOURCE_FILES))
RUST_ANSWER_FILES=$(RUST_ANSWER_FILES_PART1) $(RUST_ANSWER_FILES_PART2)


## Run all Python solutions
python: $(PY_ANSWER_FILES) 

# Pattern rule to generate answer files from input data and Python scripts
data/outputs/python/day%_part1.txt data/outputs/python/day%_part2.txt: python/aoc2025/day%.py data/inputs/day%.txt
	@echo "Running day$*..."
	@uv run python3 -m aoc2025.day$*

## Run Python solution for specific day
py-day%: data/outputs/python/day%_part1.txt data/outputs/python/day%_part2.txt
	@:

## Test solution for specific day with example data
py-test-day%:
	@uv run python3 -m aoc2025.day$* --test

## Run all Rust solutions
rust: $(RUST_ANSWER_FILES)

# Pattern rule to generate answer files from Rust source
data/outputs/rust/day%_part1.txt data/outputs/rust/day%_part2.txt: rust/src/day%.rs data/inputs/day%.txt
	@echo "Running Rust day$*..."
	@cd rust && cargo run --quiet --release -- --day $(shell echo $* | sed 's/^0*//')

## Run Rust solution for specific day
rust-day%: data/outputs/rust/day%_part1.txt data/outputs/rust/day%_part2.txt
	@:

## Test Rust solution for specific day with example data
rust-test-day%:
	@cd rust && cargo run -- --day $(shell echo $* | sed 's/^0*//') --test

## Build Rust in release mode
rust-build:
	@cd rust && cargo build --release

## Set up files for a new day (usage: make setup-day DAY=05)
setup-day:
	@uv run python3 -m aoc2025.setup_day --day $(DAY)

## Generate README.md from solutions
readme:
	@uv run python3 -m aoc2025.generate_readme

## Run ruff linter
lint:
	@uv run ruff check .

## Format code with ruff
format:
	@uv run ruff format .

## Remove output files
clean:
	@rm -f data/outputs/*/*.txt data/example_outputs/*.txt

###############################################################################
# Self Documenting Commands                                                   #
###############################################################################

.DEFAULT_GOAL := help

# Inspired by
# <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
