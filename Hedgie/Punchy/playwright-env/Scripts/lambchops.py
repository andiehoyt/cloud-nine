from playwright.sync_api import sync_playwright
import csv

def main():
    with sync_playwright() as p:
        # Open the CSV file containing userids, passwords, and grades
        with open(r"C:\Users\alano\OneDrive\Documents\GitHub\cloud-nine\Hedgie\Punchy\playwright-env\Scripts\credentials.csv", mode='r') as file:
            reader = csv.DictReader(file)  # Assume the CSV has columns "userid", "password", and "grade"
            
            for row in reader:
                userid = row['userid']
                original_password = row['password']
                grade = row['grade']  # Get the grade from the CSV
                
                print(f"Attempting to log in with userid: {userid} and grade: {grade}")
                
                # Launch the browser
                browser = p.chromium.launch(headless=False)  # Set headless=True for headless browsing
                context = browser.new_context()
                page = context.new_page()

                try:
                    # Step 0: Logout of any active session
                    page.goto("https://mathspace.co/accounts/logout")
                    page.wait_for_load_state("networkidle")
                    print("Logged out of any active session.")

                    # Step 1: Log in with the original password
                    page.goto("https://mathspace.co/accounts/login/")  # Replace with actual login URL
                    page.fill("#id_username", userid)  # Replace with the actual username field selector
                    page.click("#submit-id-login")      # Replace with the next button selector after entering username

                    # Wait for the password page to load
                    page.wait_for_selector("#id_password")  # Replace with the password field selector
                    page.fill("#id_password", original_password)  # Attempt with the original password
                    page.click("#submit-id-login")  # Replace with the login button selector

                    # Wait for navigation after login
                    page.wait_for_load_state("networkidle")

                    # Check if we might still be on the login page
                    if page.is_visible("#id_password"):
                        print(f"Original password for {userid} may have failed; trying 'insecure'...")
                        page.fill("#id_password", "insecure")
                        page.click("#submit-id-login")
                        page.wait_for_load_state("networkidle")

                    # Step 1.1: Handle forced password change if present
                    if page.is_visible("input.block-tracking.input_r9ge0j[type='password']"):
                        print(f"Password change page detected for {userid}.")
                        password_fields = page.query_selector_all("input.block-tracking.input_r9ge0j[type='password']")
                        for field in password_fields:
                            field.fill('insecure')  # Fill each password field with the new password
                        page.click("button:has-text('Change password')")  # Click the change password button
                        page.wait_for_load_state("networkidle")

                    # Step 2: Continuously click "Continue" until we're on the student page or exceed max attempts
                    max_attempts = 10
                    attempts = 0
                    while page.url != "https://mathspace.co/student/onboarding/complete" and attempts < max_attempts:
                        if page.is_visible("button:has-text('Continue')"):
                            print("Clicking 'Continue' button...")
                            page.click("button:has-text('Continue')")
                            page.wait_for_load_state("networkidle")
                        else:
                            # If we don’t see the button, wait a bit in case it’s still loading
                            page.wait_for_timeout(2000)
                        attempts += 1

                    if page.url == "https://mathspace.co/student/onboarding/complete":
                        print("Successfully reached the student page.")
                    else:
                        print("Didn't reach the student page within the max attempts.")

                except Exception as e:
                    print(f"Error encountered with userid {userid}: {e}")

                finally:
                    # No prompt to press enter—just close the browser immediately
                    print(f"Review for {userid} is complete. Closing the browser...")
                    context.close()
                    browser.close()


if __name__ == "__main__":
    main()
