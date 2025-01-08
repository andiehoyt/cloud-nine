from playwright.sync_api import sync_playwright
import csv

def main():
    with sync_playwright() as p:
        # Open the CSV file containing userids, passwords, and grades
        with open(r"C:\Users\alano\OneDrive\Documents\GitHub\cloud-nine\Hedgie\Punchy\playwright-env\Scripts\credentials.csv", mode='r') as file:
            reader = csv.DictReader(file)  # Assume the CSV has columns "userid", "password", and "grade"
            
            for row in reader:
                userid = row['userid']
                password = row['password']
                grade = row['grade']  # Get the grade from the CSV
                
                print(f"Attempting to log in with userid: {userid} and grade: {grade}")
                
                # Launch the browser
                browser = p.chromium.launch(headless=False)  # Set headless=True for headless browsing
                context = browser.new_context()
                page = context.new_page()

                try:
                    # Step 0: Logout any active session
                    page.goto("https://mathspace.co/accounts/logout")
                    page.wait_for_load_state("networkidle")  # Wait for the logout process to complete
                    print("Logged out of any active session.")

                    # Step 1: Log in to the website
                    page.goto("https://mathspace.co/accounts/login/")  # Replace with actual login URL
                    page.fill("#id_username", userid)  # Replace with actual username field selector
                    page.click("#submit-id-login")  # Replace with the next button selector after entering username

                    # Wait for the password page to load
                    page.wait_for_selector("#id_password")  # Replace with the password field selector
                    page.fill("#id_password", password)  # Replace with actual password field selector
                    page.click("#submit-id-login")  # Replace with the login button selector

                    # Wait for navigation after login
                    page.wait_for_load_state("networkidle")

                    # Handle password change page if present
                    if page.is_visible("input.block-tracking.input_r9ge0j[type='password']"):
                        print(f"Password change page detected for {userid}.")
                        password_fields = page.query_selector_all("input.block-tracking.input_r9ge0j[type='password']")
                        for field in password_fields:
                            field.fill('insecure')  # Fill the password fields with the new password
                        page.click("button:has-text('Change password')")  # Click the change password button
                        page.wait_for_load_state("networkidle")

                    # Step 2: Handle onboarding page
                    if page.is_visible("button:has-text('Continue')"):
                        page.click("button:has-text('Continue')")

                        # Check for additional onboarding page
                        if page.url == "https://mathspace.co/student/onboarding/grade":
                            print(f"Additional onboarding page detected for {userid}.")
                            # Dynamically select the grade button
                            grade_selector = f"button:has-text('{grade}')"  # Match button with text equal to grade
                            page.wait_for_selector(grade_selector, state="visible")
                            page.click(grade_selector)  # Click the grade button
                            page.wait_for_selector("button:has-text('Continue')", state="visible")  # Wait for the continue button
                            page.click("button:has-text('Continue')")

                except Exception as e:
                    print(f"Error encountered with userid {userid}: {e}")

                # Close the context and browser after each user login
                context.close()
                browser.close()

if __name__ == "__main__":
    main()
