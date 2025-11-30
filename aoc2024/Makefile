# Set UV_ENV_FILE to load .env from project root
export UV_ENV_FILE = ../.env

# Find all input data files and generate corresponding answer file paths
SOURCE_DATA_FILES=$(wildcard data/inputs/day*.txt)
ANSWER_FILES=$(patsubst data/inputs/day%.txt,data/outputs/day%_part1.txt data/outputs/day%_part2.txt,$(SOURCE_DATA_FILES))

.PHONY: help python clean lint format setup-day

python: $(ANSWER_FILES) ## Run all Python solutions

# Pattern rule to generate answer files from input data and Python scripts
data/outputs/day%_part1.txt data/outputs/day%_part2.txt: aoc2024/day%.py data/inputs/day%.txt
	@echo "Running day$*..."
	@uv run python3 -m aoc2024.day$*

## Run solution for specific day
day%: 
	@$(MAKE) data/outputs/day$*_part1.txt data/outputs/day$*_part2.txt

## Test solution for specific day with example data
test-day%: 
	@uv run python3 -m aoc2024.day$* --test

## Set up files for a new day (usage: make setup-day DAY=05)
setup-day:
	@uv run python3 -m aoc2024.setup_day --day $(DAY)

## Run ruff linter
lint:
	@uv run ruff check .

## Format code with ruff
format: 
	@uv run ruff format .

## Remove output files
clean: 
	@rm -f data/outputs/*.txt data/example_outputs/*.txt

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
