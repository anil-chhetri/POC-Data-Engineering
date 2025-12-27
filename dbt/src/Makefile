# Variables
DBT = dbt # always assign, cannot be overriden
TARGET ?= dev_pg # lazy assignment, can be overriden
THREADS ?= 4
DEBUG ?= false
DBT_DEBUG = $(if $(filter true,$(DEBUG)),--debug,)

# Default target
run: test function
	$(DBT) run --target $(TARGET) --threads $(THREADS) $(DBT_DEBUG) --print

test:
	$(DBT) test --target $(TARGET) --threads $(THREADS) --quiet --print

function:
	$(DBT) build --select "resource_type:function" --target $(TARGET) --threads $(THREADS) $(DBT_DEBUG)

install:
	$(DBT) deps $(DBT_DEBUG)

compile:
	$(DBT) compile --target $(TARGET) $(DBT_DEBUG)

build:
	$(DBT) build --target $(TARGET) --threads $(THREADS) $(DBT_DEBUG)

docs: serve-docs
	$(DBT) docs generate $(DBT_DEBUG)

serve-docs:
	$(DBT) docs serve $(DBT_DEBUG)

clean:
	$(DBT) clean $(DBT_DEBUG)

.PHONY: run test install compile build docs serve-docs clean