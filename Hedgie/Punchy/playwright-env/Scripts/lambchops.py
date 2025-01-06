from playwright.sync_api import sync_playwright
import random

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for headless browsing
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Log in to the website
        page.goto("https://mathspace.co/accounts/login/")  # Replace with actual login URL
        page.fill("#id_username", "u5050grade7t5s")  # Replace with actual username field selector and value
        page.click("#submit-id-login")  # Replace with the next button selector after entering username

        # Wait for the password page to load
        page.wait_for_selector("#id_password")  # Replace with the password field selector
        page.fill("#id_password", "insecure")  # Replace with actual password field selector and value
        page.click("#submit-id-login")  # Replace with the login button selector

        # Wait for navigation after login
        page.wait_for_load_state("networkidle")

        # Handle password change page if present
        if page.is_visible("input.block-tracking.input_r9ge0j[type='password']"):
            print("Password change page detected.")
            password_fields = page.query_selector_all("input.block-tracking.input_r9ge0j[type='password']")
            for field in password_fields:
                field.fill("insecure")  # Fill the password fields with "insecure"
            page.click("button.css-du7gh0[aria-label='Change password']")  # Click the change password button
            page.wait_for_load_state("networkidle")

        # Step 2: Handle onboarding page
        page.wait_for_selector("button.css-mbw08h[aria-label='Continue']")  # Selector for the onboarding continue button
        page.click("button.css-mbw08h[aria-label='Continue']")

         # Check for additional onboarding page
        if page.url == "https://mathspace.co/student/onboarding/grade":
            print("Additional onboarding page detected.")
            page.wait_for_selector("div.css-1d50abg", state="visible")  # Selector for grade selection button
            page.click("div.css-1d50abg")  # Click the Grade 7 button
            page.wait_for_selector("button.css-mbw08h[aria-label='Continue']", state="visible")  # Wait for the continue button
            page.click("button.css-mbw08h[aria-label='Continue']")



        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()
