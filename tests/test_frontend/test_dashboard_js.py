import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import url_for

# Skip these tests if selenium is not installed
pytest.importorskip("selenium")

@pytest.fixture
def chrome_driver():
    """Setup Chrome driver for Selenium tests."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.mark.selenium
def test_dashboard_loads_workouts(app, chrome_driver, init_database, monkeypatch):
    """Test that the dashboard loads workouts and displays them correctly."""
    # Mock the login for selenium
    def mock_is_authenticated():
        return True
        
    def mock_current_user():
        return init_database['users']['test_user']
    
    with app.test_request_context():
        dashboard_url = url_for('dashboard.workout_dashboard')
        # Start a Flask server for testing
        from multiprocessing import Process
        from app import create_app
        
        # Monkeypatch the current_user and is_authenticated properties
        # (This is specific to your auth implementation, may need adjustments)
        monkeypatch.setattr('flask_login.utils._get_user', mock_current_user)
        monkeypatch.setattr('flask_login.utils.current_user.is_authenticated', 
                           mock_is_authenticated)
        
        def run_server():
            test_app = create_app('testing')
            test_app.config['TESTING'] = True
            test_app.run(port=5000)
        
        server = Process(target=run_server)
        server.start()
        time.sleep(1)  # Wait for server to start
        
        try:
            # Navigate to the dashboard page
            chrome_driver.get('http://localhost:5000' + dashboard_url)
            
            # Wait for workout cards to load
            wait = WebDriverWait(chrome_driver, 10)
            workout_cards = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "workout-card"))
            )
            
            # Verify we have the correct number of workout cards
            assert len(workout_cards) == 2
            
            # Check that workout names are displayed
            page_content = chrome_driver.page_source
            assert "Beginner Strength Training" in page_content
            assert "HIIT Cardio Blast" in page_content
            
            # Test the search functionality
            search_input = chrome_driver.find_element(By.ID, "searchWorkouts")
            search_input.send_keys("HIIT")
            time.sleep(1)  # Wait for filter to apply
            
            # After filtering, we should only see one card
            workout_cards = chrome_driver.find_elements(By.CLASS_NAME, "workout-card")
            assert len(workout_cards) == 1
            assert "HIIT Cardio Blast" in workout_cards[0].text
            
            # Clear the filter and check that both cards appear again
            search_input.clear()
            time.sleep(1)  # Wait for filter to clear
            workout_cards = chrome_driver.find_elements(By.CLASS_NAME, "workout-card")
            assert len(workout_cards) == 2
            
            # Test the focus area filter
            focus_filter = chrome_driver.find_element(By.ID, "filterFocusArea")
            from selenium.webdriver.support.ui import Select
            Select(focus_filter).select_by_value("strength")
            time.sleep(1)  # Wait for filter to apply
            
            # We should only see strength workouts
            workout_cards = chrome_driver.find_elements(By.CLASS_NAME, "workout-card")
            assert len(workout_cards) == 1
            assert "Beginner Strength Training" in workout_cards[0].text
            
        finally:
            server.terminate()
            server.join()

@pytest.mark.selenium
def test_dashboard_empty_state(app, chrome_driver, monkeypatch):
    """Test that the dashboard shows appropriate state when no workouts are available."""
    # Create a user with no workouts
    from app import db
    from app.models.user import User
    
    with app.app_context():
        empty_user = User(username='emptyuser', email='empty@example.com')
        empty_user.set_password('password')
        db.session.add(empty_user)
        db.session.commit()
    
    # Mock the login for selenium
    def mock_is_authenticated():
        return True
        
    def mock_current_user():
        return empty_user
    
    with app.test_request_context():
        dashboard_url = url_for('dashboard.workout_dashboard')
        
        # Mock Flask-Login functions
        monkeypatch.setattr('flask_login.utils._get_user', mock_current_user)
        monkeypatch.setattr('flask_login.utils.current_user.is_authenticated', 
                           mock_is_authenticated)
        
        # Start a Flask server for testing
        from multiprocessing import Process
        from app import create_app
        
        def run_server():
            test_app = create_app('testing')
            test_app.config['TESTING'] = True
            test_app.run(port=5000)
        
        server = Process(target=run_server)
        server.start()
        time.sleep(1)  # Wait for server to start
        
        try:
            # Navigate to the dashboard page
            chrome_driver.get('http://localhost:5000' + dashboard_url)
            
            # Wait for the empty state message
            wait = WebDriverWait(chrome_driver, 10)
            empty_state = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "no-workouts"))
            )
            
            # Verify the empty state message
            assert "No Workouts Found" in empty_state.text
            assert "Contact your trainer" in empty_state.text
            
        finally:
            server.terminate()
            server.join()