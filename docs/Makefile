################################################################################
#                        pyATS Makefile
#
# Author:
#   pyats-support-ext@cisco.com
#
# Support:
#   pyats-support-ext@cisco.com
#
# Version:
#   v1.0
#
# Date:
#   December 2020
#
# About This File:
#   This script will build the documentation of the pyATS package which could
#   be served locally via make serve
#
# Requirements:
#	1. Please install dependencies via the make install_build_deps command first
################################################################################

# You can set these variables from the command line.
PKG_NAME 	  = pyATS
SPHINXOPTS    = 
SPHINXBUILD   = sphinx-build
SOURCEDIR	  = .
BUILDDIR      = $(shell pwd)/__build__/documentation
CLEAN_DIR	  = $(shell pwd)/__build__
HOSTNAME	  = localhost
VERSION	      = v`python -c "from pyats import info; print(info.__version__)"`

# Dependencies for building documentation
DEPENDENCIES = robotframework "Sphinx==3.5.4" sphinxcontrib-napoleon \
			   sphinxcontrib-mockautodoc sphinx-rtd-theme \
			   #sphinxcontrib_robotframework

# User-friendly check for sphinx-build
# ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
# $(error The '$(SPHINXBUILD)' command was not found. Please install all required dependecies via make install_build_deps)
# endif

.PHONY: help install_build_deps docs serve html clean

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "docs:            	Build Sphinx documentation for this package"
	@echo "clean: 			Remove generated documentation"
	@echo "install_build_deps: 	Install build dependecies for docs"
	@echo ""
	@echo "     --- default Sphinx targets ---"
	@echo ""
	@echo "html:       		to make standalone HTML files"
	@echo "serve:      		to start a web server to serve generated html files"

install_build_deps:
	@echo "Installing build dependecies into your environment"
	@pip install $(DEPENDENCIES)
	@echo ""
	@echo "Done"

clean:
	rm -rf $(CLEAN_DIR)

serve:
	@echo "point your browser to http://$(HOSTNAME):8000"
	@cd $(BUILDDIR)/html && python -m http.server || echo Error: run \'make \
	docs\' before using \'make serve\'

docs: html
	@echo ""
	@echo "The $(PKG_NAME) documentation is located in $(BUILDDIR)."
	@echo "Use make serve to view the docs on your browser."
	@echo ""

html:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	python -m robot.libdoc pyats.robot.pyATSRobot $(BUILDDIR)/html/robot.html
	@echo ""
	@echo "Completed building docs for preview."
	@echo ""
	@echo "Done."
	@echo ""
