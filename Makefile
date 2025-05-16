COMPOSE = docker-compose
MODULE_NAME = photrain
ADDONS_DIR = addons
MODULE_PATH = $(ADDONS_DIR)/$(MODULE_NAME)
MODULE_ZIP = $(MODULE_NAME).zip

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make start             - Start Odoo containers"
	@echo "  make stop              - Stop Odoo containers"
	@echo "  make restart           - Restart Odoo containers"
	@echo "  make logs              - Show container logs"
	@echo "  make ps                - Show container status"
	@echo "  make shell             - Open shell in Odoo container"
	@echo "  make clean             - Remove all containers and volumes"
	@echo "  make reset             - Remove all containers and volumes, then start fresh"
	@echo "  make reset-db          - Reset just the database (keeps code and configuration)"
	@echo "  make clean-modules     - Remove all installed modules but keep database structure"
	@echo "  make export            - Export the module as a zip file"
	@echo "  make update-module     - Update module in Odoo (requires curl)"
	@echo "  make install-module    - Install module in Odoo (requires curl)"
	@echo "  make db-backup         - Backup the database"
	@echo "  make structure         - Create the standard module structure"
	@echo "  make lint              - Run pylint on Python files"
	@echo "  make reset-all         - Complete system reset (use with caution)"

.PHONY: start stop restart logs ps shell clean reset
start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

shell:
	$(COMPOSE) exec web bash

clean:
	$(COMPOSE) down -v

reset: clean
	$(COMPOSE) up -d

.PHONY: export update-module install-module
export:
	@mkdir -p dist
	@echo "Creating zip file for module $(MODULE_NAME)..."
	@cd $(ADDONS_DIR) && zip -r ../dist/$(MODULE_ZIP) $(MODULE_NAME)
	@echo "Module exported to dist/$(MODULE_ZIP)"

update-module:
	@echo "Updating module $(MODULE_NAME) in Odoo..."
	@curl -s -X POST \
		-H "Content-Type: application/json" \
		-d '{"jsonrpc": "2.0", "method": "call", "params": {"module": "$(MODULE_NAME)"}}' \
		http://localhost:8069/web/dataset/call_kw/ir.module.module/button_immediate_upgrade
	@echo "Module update request sent. Check Odoo logs for confirmation."

install-module:
	@echo "Installing module $(MODULE_NAME) in Odoo..."
	@curl -s -X POST \
		-H "Content-Type: application/json" \
		-d '{"jsonrpc": "2.0", "method": "call", "params": {"module": "$(MODULE_NAME)"}}' \
		http://localhost:8069/web/dataset/call_kw/ir.module.module/button_immediate_install
	@echo "Module installation request sent. Check Odoo logs for confirmation."

.PHONY: db-backup
db-backup:
	@mkdir -p backups
	@echo "Creating database backup..."
	@$(COMPOSE) exec -T db pg_dump -U odoo postgres > backups/postgres_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup saved to backups/postgres_$(shell date +%Y%m%d_%H%M%S).sql"

.PHONY: structure
structure:
	@echo "Creating standard module structure..."
	@mkdir -p $(MODULE_PATH)/models
	@mkdir -p $(MODULE_PATH)/views
	@mkdir -p $(MODULE_PATH)/security
	@mkdir -p $(MODULE_PATH)/static/description
	@mkdir -p $(MODULE_PATH)/data

	@echo "# -*- coding: utf-8 -*-\nfrom . import models" > $(MODULE_PATH)/__init__.py
	@echo "# -*- coding: utf-8 -*-\nfrom . import models" > $(MODULE_PATH)/models/__init__.py

	@echo "# -*- coding: utf-8 -*-\nfrom odoo import models, fields, api" > $(MODULE_PATH)/models/models.py

	@echo "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink" > $(MODULE_PATH)/security/ir.model.access.csv

	@echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<odoo>\n    <!-- Views will go here -->\n</odoo>" > $(MODULE_PATH)/views/views.xml

	@echo "# -*- coding: utf-8 -*-\n{\n    'name': \"$(MODULE_NAME)\",\n    'summary': \"Summary of the module\",\n    'description': \"\"\"Description of the module\"\"\",\n    'author': \"Your Company\",\n    'website': \"https://www.yourcompany.com\",\n    'category': 'Uncategorized',\n    'version': '1.0',\n    'depends': ['base'],\n    'data': [\n        'security/ir.model.access.csv',\n        'views/views.xml',\n    ],\n    'demo': [],\n    'installable': True,\n    'application': True,\n    'auto_install': False,\n}" > $(MODULE_PATH)/__manifest__.py

	@echo "Module structure created at $(MODULE_PATH)"

.PHONY: reset-db clean-modules reset-all

reset-db:
	@echo "Resetting database only..."
	@$(COMPOSE) stop db
	@$(COMPOSE) rm -f db
	@docker volume rm -f photrain_odoo-db-data
	@$(COMPOSE) up -d db
	@echo "Database has been reset. You will need to create a new database in Odoo."

clean-modules:
	@echo "Cleaning installed modules (keeping database structure)..."
	@echo "This requires an existing database connection"
	@$(COMPOSE) exec -T db psql -U odoo postgres -c "DELETE FROM ir_module_module WHERE state = 'installed' AND name != 'base';"
	@$(COMPOSE) exec -T db psql -U odoo postgres -c "DELETE FROM ir_model_data WHERE model = 'ir.module.module' AND res_id NOT IN (SELECT id FROM ir_module_module);"
	@$(COMPOSE) restart web
	@echo "Modules cleaned. Base module is preserved."

reset-all:
	@echo "Performing complete system reset (containers, volumes, networks)..."
	@$(COMPOSE) down -v --remove-orphans
	@docker system prune -f --volumes
	@echo "System completely reset. Rebuild with 'make start'."
