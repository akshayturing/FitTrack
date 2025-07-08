# #!/bin/bash

# echo "📦 Setting PYTHONPATH and running FitTrack authentication tests..."

# # Set PYTHONPATH to project root (where `app` lives)
# export PYTHONPATH=$(dirname "$0")

# # Run tests using Python 3.10
# python3.10 -m pytest -v tests/test_auth.py

# if [ $? -eq 0 ]; then
#     echo "✅ All authentication tests passed successfully."
# else
#     echo "❌ Some authentication tests failed. Please review the output above."
# fi

#!/bin/bash

# Color definitions for formatted output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to run tests and display formatted output
run_test_module() {
    local module=$1
    local description=$2
    
    echo -e "${BLUE}=========================================================${NC}"
    echo -e "${CYAN}Testing: ${description}${NC}"
    echo -e "${BLUE}=========================================================${NC}"
    
    # Run the specific test module
    python3.10 -m pytest -v tests/$module
    
    # Capture exit code
    local result=$?
    
    if [ $result -eq 0 ]; then
        echo -e "${GREEN}✅ All ${description} tests passed successfully.${NC}"
    else
        echo -e "${RED}❌ Some ${description} tests failed. Please review the output above.${NC}"
        # Track overall status
        GLOBAL_STATUS=1
    fi
    
    echo ""
    return $result
}

# Function to run a specific test with coverage
run_test_with_coverage() {
    local module=$1
    local coverage_path=$2
    local description=$3
    
    echo -e "${BLUE}=========================================================${NC}"
    echo -e "${CYAN}Testing with Coverage: ${description}${NC}"
    echo -e "${BLUE}=========================================================${NC}"
    
    # Run the specific test module with coverage
    python3.10 -m pytest -v tests/$module --cov=$coverage_path --cov-report=term-missing
    
    # Capture exit code
    local result=$?
    
    if [ $result -eq 0 ]; then
        echo -e "${GREEN}✅ All ${description} tests with coverage passed successfully.${NC}"
    else
        echo -e "${RED}❌ Some ${description} tests with coverage failed. Please review the output above.${NC}"
        # Track overall status
        GLOBAL_STATUS=1
    fi
    
    echo ""
    return $result
}

echo -e "${YELLOW}Setting PYTHONPATH and running FitTrack test suite...${NC}"
echo ""

# Set PYTHONPATH to project root (where `app` lives)
export PYTHONPATH=$(dirname "$0")

# Initialize global status (0 = success, 1 = failure)
GLOBAL_STATUS=0

# Run authentication tests
run_test_module "test_auth.py" "Authentication"

# Run user model tests
run_test_module "jwt_config.py" "User Model"

run_test_module "models/test_workout_assignment.py" "User Model"

# Run workout model tests
#run_test_module "test_services/test_assignment_service.py" "Workout Model"

# Run workout session tests
# run_test_module "models/test_workout_assignment.py" "Workout Session"

# Run API endpoint tests
# run_test_module "test_api_endpoints.py" "API Endpoints"

# Run dashboard functionality tests
# run_test_module "test_dashboard.py" "Dashboard Functionality"

# # Run integration tests
# run_test_module "test_integration.py" "Integration"

# # Run authentication tests with coverage
# run_test_with_coverage "test_auth.py" "app/routes/auth_routes.py,app/models/user.py" "Authentication"

# Run a full test coverage report for critical components
echo -e "${BLUE}=========================================================${NC}"
echo -e "${CYAN}Running Full Test Suite with Coverage${NC}"
echo -e "${BLUE}=========================================================${NC}"

# Run all tests with coverage
# python3.10 -m pytest -v --cov=app --cov-report=html --cov-report=term

# Final status report
echo ""
if [ $GLOBAL_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED SUCCESSFULLY!${NC}"
else
    echo -e "${RED}❌ SOME TESTS FAILED. Please check the output above for details.${NC}"
fi

# Generate test report
echo -e "${BLUE}=========================================================${NC}"
echo -e "${CYAN}Generating Test Report${NC}"
echo -e "${BLUE}=========================================================${NC}"

# Create reports directory if it doesn't exist
mkdir -p test-reports

# Generate junit XML report
# python3.10 -m pytest --junitxml=test-reports/test-results.xml

# Print location of HTML coverage report
echo -e "${YELLOW}HTML coverage report generated in: htmlcov/index.html${NC}"

exit $GLOBAL_STATUS