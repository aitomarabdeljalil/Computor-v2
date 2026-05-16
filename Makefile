PYTHON := python3

# Directories
CODE_DIR := computorv2
TESTS_DIR := tests

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: all clean help run

# Main targets
all: help

run:
	@echo "$(BLUE)🚀 Running the Application...$(NC)"
	$(PYTHON) -m $(CODE_DIR)
	@echo "$(GREEN)✅ Application run complete!$(NC)"

# Clean up temporary files
clean:
	@echo "$(RED)🧹 Cleaning up generated files...$(NC)"
	@rm -rf $(CODE_DIR)/__pycache__/
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"


# Help message (lists available commands)
help:
	@echo "$(GREEN)🎓 ComputorV2 - Available targets:"
	@echo "$(YELLOW)🚀 Application:$(NC)"
	@echo "  make run		- Run the application"
	@echo "$(YELLOW)🧹 Cleanup:$(NC)"
	@echo "  make clean		- Clean temporary files"
	@echo "$(GREEN)✅ Use 'make <target>' to execute a specific task.$(NC)"