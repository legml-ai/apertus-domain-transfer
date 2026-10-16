.PHONY: run build verify

IMAGE := legml-track1b

# Judges run this from the project root (delegated) or from track_1b/.
# Without LLM_* credentials in .env it re-scores the committed judgements and verifies them against results.json.
# With credentials it also judges any response without a cached judgement.
run: build
	docker run --rm $(if $(wildcard .env),--env-file .env,) \
		-e LLM_NAME -e LLM_BASE_URL -e LLM_API_KEY -e HF_TOKEN \
		-v $(CURDIR)/results:/app/results $(IMAGE) $(ARGS)

build:
	docker build -t $(IMAGE) .

# Offline check without network: recompute scores from the committed judgements only.
verify: build
	docker run --rm -v $(CURDIR)/results:/app/results $(IMAGE) --offline
