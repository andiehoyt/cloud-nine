import csv
import random
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Add cookies and headers to the context
        context = browser.new_context(
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "X-CSRFToken": "1Xb9iH4SvDhfBU9AMYG3WRnpsvMHWNia",  # Optional if CSRF token is required in headers
            }
        )

        # Add cookies
        context.add_cookies([
            {
                "name": "sessionid",
                "value": "omg2hbl4xf87xb6ja57qx7yojb60svva",
                "domain": "mathspace.co",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "csrftoken",
                "value": "1Xb9iH4SvDhfBU9AMYG3WRnpsvMHWNia",
                "domain": "mathspace.co",
                "path": "/",
                "secure": True
            },
            {
                "name": "cf_clearance",
                "value": "BN0WNLwcsH9IZ.b3BsuKEjibyvyDrejjdSUez94wB.Y-1736199442-1.2.1.1-WfthXqao1iKVJBDEdm6tX74194UNdl0xw_oz4gZGswkvj5oh_bONsKl7xZLoWzQ1V._r5LYWDpgKQlybyy.gYF1_pJ2QNlMGnuGe.wOfWxgX5iD89.0lwCIHbO8OrDPAy4K6rTg5DesFVmhrdTjn4eG.4MMvRNX7zEx8JYPTZseHcfidVynSznLrHurhdH_h_hhDM.pxj_YQbHwA1mgIPoKRWI0J84QRLbvKGBpuUu.eZOncqt.Jcg8r3eX4e6.C1HUzEawKsXGHfPGBDv3EIcAXasT9WAP6dctffQ9kIbHSDJHUK5NA3l_tqCdauPJUuQ5jlemo6mawhRBcxjfu19Oddk9IPeVSRWXbRIfiS44Diq_HkrOb857bYypvsx2pzRef1D78HeFwbEvFGM8hBw",
                "domain": "mathspace.co",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "has_logged_in",
                "value": "true",
                "domain": "mathspace.co",
                "path": "/",
            },
            {
                "name": "selected_class_id",
                "value": "334889",
                "domain": "mathspace.co",
                "path": "/",
            }
        ])

        # Navigate to the admin dashboard or any authenticated page
        page = context.new_page()
        page.goto("https://mathspace.co/impersonate/stop")
        page.goto("https://mathspace.co/debug/skill-set-check-in/curriculum/LanternCurriculum-15")

        page.wait_for_load_state("networkidle")  # Wait until no network requests are in progress
# Example: Verify successful navigation
        if not page.is_visible("input[placeholder='Outcome IDs']"):
            print("Failed to load the page. Exiting.")
            browser.close()
            return

        print("Logged in and ready to process data.")

       # Correctly open and process the CSV file
        csv_path = r"C:\Users\alano\OneDrive\Documents\GitHub\cloud-nine\Hedgie\Punchy\playwright-env\Scripts\data.csv"
        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)  # Initialize CSV reader
            for row in reader:  # Process rows inside the open block
                outcome_ids = row["Outcome IDs"]
                student_id = row["User ID"]
                percent_correct = float(row["Percent Correct"])

                # Example: Log details (replace with actual logic)
                print(f"Processing Outcome IDs: {outcome_ids}, User ID: {student_id}, Percent Correct: {percent_correct}")

                # Perform your Playwright actions here
                page.fill("input[placeholder='Outcome IDs']", outcome_ids)
                page.locator("button:has-text('Validate')").nth(0).click()
                page.wait_for_selector("button:has-text('Fetch Question Previews')")
                page.fill("input[placeholder='Student ID']", student_id)
                # Click the second "Validate" button (for Student ID)
                page.locator("button:has-text('Validate')").nth(1).click()

                page.click("button:has-text('Start Check-In')")
                print(f"Navigated to check-in page for {student_id}")

                # Step 3: Start Check-In
                page.click("button:has-text('Start Check-In')")
                page.wait_for_load_state("networkidle")


                # Step 5: Add to Local Storage
                page.evaluate("""() => {
                    localStorage.setItem('__lantern:devMode', 'true');
                }""")
                page.reload()
                #page.wait_for_selector("button[aria-label='✗']")  # Wait for Incorrect button to appear

                # Step 6: Answer Questions Based on Probability
                while True:
                    # Handle Continue button
                    try:
                        if page.is_visible("button.css-19p41nw") or page.is_visible("button:has-text('Continue')"):
                            print("Continue button detected. Skipping question.")
                            page.locator("button.css-19p41nw:has-text('Continue')").click()
                            page.wait_for_load_state("networkidle")
                            continue
                    except Exception as e:
                        print(f"Error handling Continue button: {e}")

                    # Handle Back to Dashboard button
                    if page.is_visible("button[aria-label='Back to dashboard']"):
                        print(f"Finished check-in for {student_id}")
                        print(f"Dashboard URL: {page.url}")
                        page.click("button[aria-label='Back to dashboard']")
                        break

                    # Capture Current Question Text
                    try:
                        current_question = page.locator("div.css-4lpqgf-makeBodyComponent.e2zo9vh0").text_content()
                    except Exception as e:
                        print(f"Error capturing current question: {e}")
                        continue

                    # Decide Correct or Incorrect Answer
                    random_value = random.random()  # Generates a value between 0 and 1
                    print(f"Random Value: {random_value}, Percent Correct: {percent_correct}")

                    if random_value < percent_correct:
                        print(f"Answering Correct for {student_id}")
                        locator = page.locator("button[aria-label='✓']")
                    else:
                        print(f"Answering Incorrect for {student_id}")
                        locator = page.locator("button[aria-label='✗']")

                    try:
                        # Attempt to click the chosen button
                        locator.click()

                        # Wait for the question number to change
                        page.wait_for_function(
                            f"""() => {{
                                const element = document.querySelector('div.css-4lpqgf-makeBodyComponent.e2zo9vh0');
                                return element && element.textContent !== '{current_question}';
                            }}""",
                            timeout=100  # Adjust timeout as needed
                        )
                    except Exception as e:
                        print(f"Error interacting with button or waiting for the next question: {e}")
                        continue

        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()